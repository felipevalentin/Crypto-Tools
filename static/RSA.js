document.getElementById('digestform').addEventListener('submit', formSubmit);
size = document.getElementById("sizes");
result = document.getElementById('result');
private = document.getElementById('private');
public = document.getElementById('public');

function formSubmit(event) {
  // Formulario envia requisição ao endpoint que gera par de chaves RSA o arquivo
  const url = event.target.action;
  fetch(url, { method: 'POST', body: new FormData(event.target) }).then(
    (response) => {
      // Verificamos se foi possível gerar as chaves
      if (!response.ok) {
        result.textContent = 'Não foi possível gerar a chave';
      } else {
        // caso sim, mostramos as chaves na interface
        result.textContent = 'Par de chaves RSA de ' + size.value + ' bits geradas com sucesso';
        response.json().then((response) => {
          private.innerHTML= response['private'];
          public.innerHTML = response['public'];
        });
      }
    }
  );
  event.preventDefault();
}
