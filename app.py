from flask import Flask, render_template, jsonify, request
import threading
import asyncio

from host_main import HiveMindHostEnhanced

app = Flask(__name__, static_folder='static', template_folder='templates')

_host_state = {"host": None, "thread": None}


def _run_host(host: HiveMindHostEnhanced):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(host.start())
    except Exception:
        pass


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
    if not host or not host.running:
        return jsonify({"stopped": False, "reason": "not running"}), 400

    # Best-effort stop: flip running flag. Proper shutdown should be performed in same event loop.
    host.running = False
    return jsonify({"stopped": True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
