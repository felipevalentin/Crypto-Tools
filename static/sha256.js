document.getElementById("digestform").addEventListener("submit", formSubmit);
file = document.getElementById("file");
result = document.getElementById("result");
digest = document.getElementById("digest");

function formSubmit(event) {
  // Formulario envia requisição ao endpoint que gera resumo resumo criptográfico
  const url = event.target.action;
  event.preventDefault();
  fetch(url, { method: "POST", body: new FormData(event.target) }).then(
    (response) => {
      // verificamos se o documento é valido
      if (!response.ok) {
        result.textContent = "Nenhum documento inserido, ou documento inválido.";
      } else {
        response.json().then((response) => {
          // mostramos caso seja valido
          result.textContent ="Resumo criptográfico em hexadecimal de " + file.files[0].name + " com o algoritmo sha256:";
          digest.textContent = response["digest"];
        });
      }
    }
  );
}
