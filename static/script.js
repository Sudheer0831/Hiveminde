async function api(path, method = 'GET') {
  const opts = { method };
  if (method === 'POST' && arguments.length > 2) opts.body = arguments[2];
  const res = await fetch(path, opts);
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

// Session create
document.getElementById('create-session').addEventListener('click', async () => {
  const r = await api('/api/session/create', 'POST');
  if (r.ok) {
    document.getElementById('session-code').innerText = r.session_code;
    appendLog('Session created: ' + r.session_code);
  } else {
    appendLog('Create session failed: ' + (r.reason||'unknown'));
  }
});

// Upload form
document.getElementById('upload-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = document.getElementById('file').files[0];
  if (!f) return appendLog('No file selected');
  const fd = new FormData();
  fd.append('file', f);
  const r = await api('/api/upload', 'POST', fd);
  if (r.ok) {
    document.getElementById('uploaded-url').innerText = r.url;
    appendLog('Uploaded: ' + r.url);
  } else appendLog('Upload failed: ' + (r.reason||'unknown'));
});

// Schedule
document.getElementById('schedule').addEventListener('click', async () => {
  const url = document.getElementById('uploaded-url').innerText;
  const delay = parseFloat(document.getElementById('delay').value || '3');
  if (!url) return appendLog('No uploaded track URL');
  const r = await api('/api/schedule', 'POST', JSON.stringify({ track_url: url, delay }));
  if (r.ok) appendLog('Scheduled to start at ' + new Date(r.start_at * 1000).toLocaleTimeString()); else appendLog('Schedule failed: ' + (r.reason||'unknown'));
});
