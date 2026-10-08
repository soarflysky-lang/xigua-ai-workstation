const form = document.getElementById('taskForm');
const statusBox = document.getElementById('status');
const resultBox = document.getElementById('result');

async function createTask(payload) {
  const response = await fetch('http://localhost:8000/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  return response.json();
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    topic: document.getElementById('topic').value,
    audience: document.getElementById('audience').value,
    style: document.getElementById('style').value,
    duration: Number(document.getElementById('duration').value),
    platform: 'douyin',
    tone: '干净利落，带场景感',
    industry: '商家/转行自媒体',
  };

  statusBox.textContent = '生成中...';

  try {
    const task = await createTask(payload);
    statusBox.textContent = `任务已创建：${task.id}`;
    resultBox.innerHTML = `
      <h3>${task.headline}</h3>
      <p><strong>状态：</strong>${task.status}</p>
      <p><strong>平台：</strong>${task.platform}</p>
      <p><strong>概述：</strong>${task.summary}</p>
      <p><strong>脚本：</strong></p>
      <pre>${task.script}</pre>
    `;
  } catch (err) {
    statusBox.textContent = '生成失败';
    resultBox.innerHTML = `<p>请确认后端已启动，并检查接口是否可用。</p>`;
  }
});
