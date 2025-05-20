function consultarCPF() {
  const cpf = document.getElementById('cpf').value;
  const resposta = document.getElementById('resposta');
  resposta.innerHTML += `<div class="user">${cpf}</div>`;

  fetch('/api/extrato', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({cpf})
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === "not_found") {
      resposta.innerHTML += `<div class="bot">${data.message}</div>`;
    } else {
      let html = '<div class="bot"><strong>Débitos encontrados:</strong><ul>';
      data.data.forEach(item => {
        html += `<li>${item.nome} (${item.unidade}) - ${item.descricao} - Venc: ${item.vencimento} - <strong>R$ ${item.valor_final.toFixed(2)}</strong></li>`;
      });
      html += '</ul></div>';
      resposta.innerHTML += html;
    }
    resposta.scrollTop = resposta.scrollHeight;
  })
  .catch(() => {
    resposta.innerHTML += `<div class="bot text-danger">Erro ao consultar. Tente novamente mais tarde.</div>`;
  });
}
