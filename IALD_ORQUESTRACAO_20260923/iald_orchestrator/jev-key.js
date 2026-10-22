'use strict';
document.getElementById('keyForm').addEventListener('submit', async event => {
  event.preventDefault();
  const input = document.getElementById('apiKey');
  const button = document.getElementById('save');
  const status = document.getElementById('status');
  button.disabled = true;
  try {
    const pending = fetch('/admin/api/orchestrator/connections/jev/key', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, credentials: 'same-origin',
      body: JSON.stringify({key: input.value})
    });
    input.value = '';
    const response = await pending;
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Não foi possível guardar a chave.');
    status.textContent = 'Chave guardada no cofre Windows. Jev aguarda validação da conexão e saldo.';
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
