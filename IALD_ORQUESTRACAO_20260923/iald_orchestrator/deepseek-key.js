'use strict';
document.getElementById('keyForm').addEventListener('submit', async event => {
  event.preventDefault();
  const input = document.getElementById('apiKey');
  const button = document.getElementById('save');
  const status = document.getElementById('status');
  button.disabled = true;
  try {
    const pending = fetch('/admin/api/orchestrator/connections/deepseek/key', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'same-origin',
      body: JSON.stringify({key: input.value, authorize_paid_tasks: document.getElementById('consent').checked})
    });
    input.value = '';
    const response = await pending;
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Não foi possível guardar a chave.');
    status.textContent = 'Chave guardada com criptografia Windows DPAPI. Uso autorizado; falta validar a conexão.';
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
