# HiveMind - Distributed Audio Synchronization System

HiveMind is a Python-driven, local-first distributed audio synchronization system that turns nearby devices into a single time-locked sound network without external speakers.

## Overview

One device acts as a **host** (time authority), while other devices join as **nodes** using a code-based handshake. All devices play perfectly time-aligned audio using local clock synchronization, forming a distributed sound system.

## ✨ Key Features

### Core Features
- **Perfect Sync**: <50ms audio synchronization across devices
- **Code-Based Joining**: Simple session codes (e.g., "HM-1234") for easy connection
- **Low Latency**: Scheduled playback with 300ms lookahead
- **System Audio**: Capture and share all system audio output
- **Adaptive Correction**: Automatic drift correction maintains sync over time

### Advanced Features (New!)
- **🎵 Opus Compression**: Reduce bandwidth usage by up to 10x
- **🌐 Web Dashboard**: Beautiful real-time monitoring interface
- **🔊 Volume Control**: Per-node volume balancing and master volume
- **⚡ Latency Calibration**: Automatic latency measurement and compensation
- **🎚️ Quality Presets**: Low, Medium, High, and Ultra quality settings

## Architecture

```
          ┌────────────┐
          │   HOST     │
          │ (Python)   │
          │ Time Master│
          └─────┬──────┘
                │
      ┌─────────┼─────────┐
      │         │         │
┌─────▼─────┐ ┌─▼──────┐ ┌─▼──────┐
│ NODE A    │ │ NODE B │ │ NODE C │
│ (Client)  │ │        │ │        │
│ Audio Sync│ │ Audio  │ │ Audio  │
└───────────┘ └────────┘ └────────┘
```

## Installation

```bash
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- Windows (for system audio capture via WASAPI)
- Local network connection

## Quick Start

### Start Host

```bash
python host_main.py
```

**With options:**
```bash
python host_main.py --port 7878 --web-port 5000
```

The host will display:
- Session code (e.g., "HM-1234")
- Network port
- Web dashboard URL (http://localhost:5000)

### Join as Node

```bash
python node_main.py
```

**With options:**
```bash
python node_main.py --session-code HM-1234 --host localhost --volume 0.8
```

### Access Web Dashboard

Open your browser to:
```
http://localhost:5000
```

Features:
- Real-time node monitoring
- Audio statistics
- Connection status
- Beautiful glassmorphism UI

## Command-Line Options

### Host Options

```bash
python host_main.py [OPTIONS]

Options:
  --port PORT              Network port (default: 7878)
  --no-compression         Disable Opus compression
  --no-web                 Disable web dashboard
  --web-port PORT          Web dashboard port (default: 5000)
```

### Node Options

```bash
python node_main.py [OPTIONS]

Options:
  --session-code CODE      Session code to join
  --host ADDRESS           Host address (default: localhost)
  --port PORT              Host port (default: 7878)
  --volume LEVEL           Initial volume 0.0-1.0 (default: 1.0)
```

## How It Works

1. **Time Synchronization**: Nodes sync their clocks with the host using an NTP-like protocol
2. **Audio Scheduling**: Audio chunks are sent with future playback timestamps
3. **Scheduled Playback**: Each node plays audio at the exact scheduled time (adjusted for clock offset)
4. **Drift Correction**: Periodic re-sync and adaptive playback speed maintain perfect alignment
5. **Compression**: Opus codec reduces bandwidth while maintaining quality

## Project Structure

```
hivemind/
├── common/
│   ├── device_id.py           # Device identity system
│   ├── protocol.py            # Network protocol
│   ├── crypto.py              # Session security
│   ├── audio_codec.py         # Opus compression (NEW)
│   ├── volume_control.py      # Volume management (NEW)
│   └── latency_calibration.py # Latency measurement (NEW)
├── host/
│   ├── session_manager.py     # Session management
│   ├── clock_sync.py          # Time sync service
│   ├── audio_scheduler.py     # Audio scheduling
│   ├── audio_capture.py       # System audio capture
│   ├── network_server.py      # TCP server
│   └── web_dashboard.py       # Web interface (NEW)
├── node/
│   ├── client.py              # Main client
│   ├── time_sync_client.py    # Time sync client
│   ├── buffer_manager.py      # Audio buffering
│   └── playback_engine.py     # Audio playback
├── config.py                  # Configuration
└── quality_settings.py        # Quality presets (NEW)

tests/                         # Unit tests
host_main.py                   # Enhanced host entry point
node_main.py                   # Enhanced node entry point
```

## Configuration

Edit `hivemind/config.py` to customize:

```python
SAMPLE_RATE = 48000           # Audio sample rate
CHANNELS = 2                  # Stereo
CHUNK_DURATION_MS = 50        # Chunk size
LOOKAHEAD_MS = 300            # Playback lookahead
SYNC_INTERVAL_S = 2.0         # Time sync interval
DEFAULT_PORT = 7878           # Network port
```

## Quality Presets

Choose from 4 quality levels:

| Preset | Sample Rate | Bitrate | Lookahead | Use Case |
|--------|-------------|---------|-----------|----------|
| Low | 24kHz | 64kbps | 400ms | Slow networks |
| Medium | 48kHz | 128kbps | 300ms | Balanced (default) |
| High | 48kHz | 256kbps | 250ms | Fast networks |
| Ultra | 96kHz | 512kbps | 200ms | Maximum quality |

## Web Dashboard Features

- **Real-time Monitoring**: Live node status and statistics
- **Audio Visualizer**: Animated waveform display
- **Session Info**: Session code, uptime, node count
- **Node Details**: Per-node latency, sync count, connection time
- **Auto-refresh**: Updates every 2 seconds

## Advanced Features

### Opus Compression

Reduces bandwidth by up to 10x while maintaining excellent audio quality:

```python
# Automatically enabled by default
# Disable with: python host_main.py --no-compression
```

### Volume Control

Per-node volume adjustment and automatic balancing:

```python
from hivemind.common.volume_control import VolumeController

volume = VolumeController()
volume.set_master_volume(0.8)
volume.set_node_volume(device_id, 0.5)
```

### Latency Calibration

Automatic latency measurement for perfect sync:

```python
from hivemind.common.latency_calibration import LatencyCalibrator

calibrator = LatencyCalibrator()
latency_ms = calibrator.calibrate(device_id)
```

## Testing

Run unit tests:

```bash
python -m pytest tests/ -v
```

## Troubleshooting

**No audio on nodes?**
- Check that the host has audio playing
- Verify the host can capture system audio (may need "Stereo Mix" enabled on Windows)
- Check firewall settings for port 7878

**Audio out of sync?**
- Check network latency (should be <50ms on LAN)
- Verify time sync quality in logs (should be "excellent" or "good")
- Try increasing lookahead: edit `LOOKAHEAD_MS` in config.py

**Web dashboard not loading?**
- Check that port 5000 is not in use
- Try a different port: `python host_main.py --web-port 8080`

## Performance

- **Latency**: ~300-400ms end-to-end
- **Sync Accuracy**: <50ms between nodes
- **Bandwidth**: 
  - Uncompressed: ~1.5 Mbps per node
  - Opus (128kbps): ~128 kbps per node
- **CPU Usage**: Low (~5-10% per node)

## Future Enhancements

- ⏳ Bluetooth transport layer
- ⏳ Cross-platform support (Linux/macOS)
- ⏳ Mobile app (Android/iOS)
- ⏳ Video synchronization
- ⏳ Mesh networking
- ⏳ Cloud relay for internet-based sessions

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## Credits

Built with:
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Audio I/O
- [opuslib](https://github.com/OnBeep/opuslib) - Opus codec
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [NumPy](https://numpy.org/) - Audio processing

---

**HiveMind** - Turn any devices into a synchronized sound system 🎵
