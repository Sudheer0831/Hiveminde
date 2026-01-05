from flask import Flask, render_template, jsonify, request
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

from host_main import HiveMindHostEnhanced
from hivemind.common.protocol import Protocol
from werkzeug.utils import secure_filename
import os
import time

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')

# _host_state holds: host, thread, loop
_host_state = {"host": None, "thread": None, "loop": None}
_host_state.update({"demo_event": None, "demo_future": None})


def _run_host(host: HiveMindHostEnhanced):
    # Run host.start() inside its own asyncio event loop on a dedicated thread.
    loop = asyncio.new_event_loop()
    _host_state["loop"] = loop
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(host.start())
    except Exception:
        pass
    finally:
        try:
            loop.run_until_complete(loop.shutdown_asyncgens())
        except Exception:
            pass
        _host_state["loop"] = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status')
def status():
    host = _host_state.get("host")
    return jsonify({
        "running": bool(host and host.running),
        "session_code": host.session_manager.session_code if host else None,
        "node_count": len(host.session_manager.nodes) if host else 0,
    })


@app.route('/api/session/create', methods=['POST'])
def create_session():
    host = _host_state.get("host")
    if not host:
        return jsonify({"ok": False, "reason": "host not running"}), 400

    code = host.session_manager.generate_session_code()
    return jsonify({"ok": True, "session_code": code})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_DIR, filename)


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"ok": False, "reason": "no file"}), 400
    f = request.files['file']
    filename = secure_filename(f.filename)
    path = os.path.join(UPLOAD_DIR, filename)
    f.save(path)
    url = f"/uploads/{filename}"
    return jsonify({"ok": True, "url": url})


@app.route('/api/schedule', methods=['POST'])
def schedule():
    data = request.get_json() or {}
    track_url = data.get('track_url')
    delay = float(data.get('delay', 3.0))
    if not track_url:
        return jsonify({"ok": False, "reason": "no track_url"}), 400

    start_at = time.time() + max(0.5, delay)

    host = _host_state.get("host")
    if not host:
        return jsonify({"ok": False, "reason": "host not running"}), 400

    host.session_manager.add_scheduled_track(track_url, start_at)

    # Broadcast schedule to nodes
    msg = Protocol.create_schedule_message(track_url=track_url, start_at=start_at)
    try:
        # schedule broadcast on host loop
        loop = _host_state.get("loop")
        if loop:
            asyncio.run_coroutine_threadsafe(host.network_server.broadcast(msg), loop)
        else:
            # best-effort
            asyncio.get_event_loop().create_task(host.network_server.broadcast(msg))
    except Exception:
        pass

    return jsonify({"ok": True, "start_at": start_at})


@app.route('/api/demo/start', methods=['POST'])
def demo_start():
    data = request.get_json() or {}
    duration = float(data.get('duration', 5.0))
    chunk_ms = int(data.get('chunk_ms', 20))

    host = _host_state.get("host")
    loop = _host_state.get("loop")
    if not host or not loop:
        return jsonify({"ok": False, "reason": "host not running"}), 400

    if _host_state.get('demo_future') is not None:
        return jsonify({"ok": False, "reason": "demo already running"}), 400

    async def _demo_generator(host_app, duration_s, chunk_ms, stop_event: asyncio.Event):
        sr = host_app.codec_manager.sample_rate
        channels = host_app.codec_manager.channels
        codec = host_app.codec_manager
        import math, time
        start = time.time()
        freq = 440.0
        while (time.time() - start) < duration_s and not stop_event.is_set():
            frame_count = int(sr * (chunk_ms / 1000.0))
            pcm = bytearray()
            for n in range(frame_count):
                t = n / sr
                val = int(0.5 * 32767.0 * math.sin(2.0 * math.pi * freq * t))
                pcm.extend(int(val).to_bytes(2, 'little', signed=True))

            encoded, _ = codec.encode(bytes(pcm))
            msg = Protocol.create_audio_chunk(play_at=time.time() + 0.2, sample_rate=sr, channels=channels, audio_data=encoded)
            try:
                await host_app.network_server.broadcast(msg)
            except Exception:
                pass
            await asyncio.sleep(chunk_ms / 1000.0)

    # create stop event on host loop
    fut_event = asyncio.run_coroutine_threadsafe(asyncio.Event(), loop)
    stop_event = fut_event.result()

    # schedule generator
    future = asyncio.run_coroutine_threadsafe(_demo_generator(host, duration, chunk_ms, stop_event), loop)
    _host_state['demo_event'] = stop_event
    _host_state['demo_future'] = future

    return jsonify({"ok": True})


@app.route('/api/demo/stop', methods=['POST'])
def demo_stop():
    loop = _host_state.get('loop')
    stop_event = _host_state.get('demo_event')
    future = _host_state.get('demo_future')
    if not loop or not stop_event or not future:
        return jsonify({"ok": False, "reason": "demo not running"}), 400

    try:
        # set the event on the host loop
        asyncio.run_coroutine_threadsafe(stop_event.set(), loop).result(timeout=2)
    except Exception:
        pass

    # clear stored refs
    _host_state['demo_event'] = None
    _host_state['demo_future'] = None
    return jsonify({"ok": True})


@app.route('/api/start', methods=['POST'])
def start():
    if _host_state.get("host") and _host_state["host"].running:
        return jsonify({"started": False, "reason": "already running"}), 400

    host = HiveMindHostEnhanced(enable_web_dashboard=False)
    _host_state["host"] = host
    t = threading.Thread(target=_run_host, args=(host,), daemon=True)
    _host_state["thread"] = t
    t.start()
    return jsonify({"started": True})


@app.route('/api/stop', methods=['POST'])
def stop():
    host = _host_state.get("host")
    loop = _host_state.get("loop")
    if not host or not host.running or loop is None:
        return jsonify({"stopped": False, "reason": "not running"}), 400

    # Schedule the host.stop coroutine on the host's event loop and wait for it
    try:
        fut = asyncio.run_coroutine_threadsafe(host.stop(), loop)
        fut.result(timeout=10)
    except Exception as e:
        return jsonify({"stopped": False, "reason": str(e)}), 500

    return jsonify({"stopped": True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
