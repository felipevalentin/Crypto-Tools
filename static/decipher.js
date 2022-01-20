document.getElementById('digestform').addEventListener('submit', formSubmit);
paragraph = document.getElementById('result');

function formSubmit(event) {
  // Formulario envia requisição ao endpoint que decifra o arquivo
  const url = event.target.action;
  fetch(url, { method: 'POST', body: new FormData(event.target) }).then(
    (response) => {
      // Verificando se não ouve algum erro!
      if (!response.ok) {
        response.text().then((text) => {
          paragraph.textContent = 'Não foi possível decifrar a mensagem, pois ' + text;
        });
      } else {
        // Realiza o download do arquivo com o nome do arquivo baixado
        let filename = response.headers.get('Content-Disposition').split('filename=')[1];
        response.blob().then((blob) => {
          paragraph.textContent = 'Arquivo decifrado. Download do arquivo decifrado será iniciado.';
          saveBlob(blob, filename);
        });
      }
    }
  );
  event.preventDefault();
}

function saveBlob(blob, fileName) {
  // Serve para criar uma janela de download
  var a = document.createElement('a');
  document.body.appendChild(a);
  a.style = 'display: none';

  var url = window.URL.createObjectURL(blob);
  a.href = url;
  a.download = fileName;
  a.click();
  window.URL.revokeObjectURL(url);
}
