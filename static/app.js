const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const conversation = document.querySelector('#conversation');
const sendButton = form.querySelector('button');
let messageNumber = 1;

function addMessage(label, content, type = '') {
  const message = document.createElement('div');
  message.className = `message ${type}`;
  message.innerHTML = `<span class="message-index">${String(messageNumber++).padStart(2, '0')}</span><div><p class="message-label">${label}</p><p></p></div>`;
  message.querySelector('p:last-child').textContent = content;
  conversation.appendChild(message);
  conversation.scrollTop = conversation.scrollHeight;
  return message;
}

document.querySelectorAll('[data-prompt]').forEach((button) => {
  button.addEventListener('click', () => {
    input.value = button.dataset.prompt;
    input.focus();
    input.dispatchEvent(new Event('input'));
  });
});

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 100)}px`;
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message || sendButton.disabled) return;

  addMessage('YOU', message, 'user');
  input.value = '';
  input.style.height = 'auto';
  sendButton.disabled = true;
  sendButton.querySelector('span:first-child').textContent = 'Researching';

  const pending = addMessage('CITYSCOPE', 'Checking live city data...');
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    pending.querySelector('p:last-child').textContent = data.response || data.error || 'No response received.';
  } catch (error) {
    pending.querySelector('p:last-child').textContent = 'Unable to reach the local assistant. Make sure the server is running.';
  } finally {
    sendButton.disabled = false;
    sendButton.querySelector('span:first-child').textContent = 'Send';
  }
});
