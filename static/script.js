async function api(path, method = 'GET') {
  const res = await fetch(path, { method });
  return res.json();
}

async function refresh() {
  const s = await api('/api/status');
  document.getElementById('status').innerText = `Running: ${s.running}\nSession: ${s.session_code || '-'}\nNodes: ${s.node_count}`;
}

document.getElementById('start').addEventListener('click', async () => {
  const r = await api('/api/start', 'POST');
  if (r.started) appendLog('Host started'); else appendLog('Start failed: ' + (r.reason||'unknown'));
  setTimeout(refresh, 500);
});

document.getElementById('stop').addEventListener('click', async () => {
  const r = await api('/api/stop', 'POST');
  if (r.stopped) appendLog('Host stopped'); else appendLog('Stop failed: ' + (r.reason||'unknown'));
  setTimeout(refresh, 500);
});

function appendLog(msg) {
  const el = document.getElementById('log');
  el.textContent = `${new Date().toLocaleTimeString()}: ${msg}\n` + el.textContent;
}

refresh();
