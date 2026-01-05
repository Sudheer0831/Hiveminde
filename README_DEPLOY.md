Deployment & Architecture
=========================

Overview
--------
This repository now includes a small Flask-based web dashboard (`app.py`) which exposes a UI under `/` and JSON endpoints to start/stop and query the HiveMinde host. The original host logic is kept in `host_main.py`; lightweight `hivemind` stubs provide local imports for now.

Vercel
------
- `pyproject.toml` declares `app = "app:app"` for Vercel to detect the Flask entrypoint.
- `requirements.txt` lists runtime dependencies (`flask`, `flask-cors`, `opuslib`, `gunicorn`).

Backend architecture
--------------------
- `app.py`: Flask dashboard and control API. Starts the host in a dedicated thread with its own asyncio event loop. Uses `asyncio.run_coroutine_threadsafe` to call `host.stop()` on that loop for clean shutdown.
- `host_main.py`: Async `HiveMindHostEnhanced` implementing the host lifecycle, audio capture, scheduling and message handling. Current networking/audio modules are stubbed under `hivemind/` and should be replaced by real implementations.

Next steps to production
------------------------
1. Replace stubbed networking (`hivemind/host/network_server.py`) with a real asyncio-based server (e.g., `websockets` or `aiohttp`).
2. Integrate Opus audio encode/decode with `opuslib` for compressed audio transport.
3. Add authentication and TLS for network communication.
4. Add unit tests and integration tests for host start/stop and message flows.

Deploying to Vercel
-------------------
Option A — trigger redeploy from git (recommended):

```bash
git commit --allow-empty -m "chore: trigger Vercel redeploy" && git push origin main
```

Option B — re-import the repo in the Vercel UI and redeploy the `main` branch.

If Vercel still fails to detect the Flask entrypoint, add an explicit `[tool.vercel]` `app` entry in `pyproject.toml` (already present) or add an `index.py` that imports and exposes `app`.
