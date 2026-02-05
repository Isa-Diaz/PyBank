const API_INVESTIDOR = "http://localhost:5002";

const cpf = localStorage.getItem("cpf_cliente");
const form = document.getElementById("form-investimento");
const mensagem = document.getElementById("mensagem");
const inputCpf = document.getElementById("cpf");

/* autopreenche cpf */
inputCpf.value = cpf;

/* valida sessão */
if (!cpf) {
  alert("Sessão inválida");
  window.location.href = "index.html";
}

/* criar investimento */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const valor = Number(document.getElementById("valor").value);

  try {

    const res = await fetch(`${API_INVESTIDOR}/investimentos/fixo`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        cpf: cpf,
        valor_investido: valor
      })
    });

    const data = await res.json();

    if (!res.ok) {
      mensagem.innerText = data.erro || "Erro ao criar investimento";
      mensagem.style.color = "red";
      return;
    }

    mensagem.innerText = "Investimento criado com sucesso!";
    mensagem.style.color = "green";

    setTimeout(() => {
      window.location.href = "investidor_home.html";
    }, 1500);

  } catch (err) {
    console.error(err);
    mensagem.innerText = "Erro ao conectar com servidor";
    mensagem.style.color = "red";
  }
});

/* voltar */
function voltarHome() {
  window.location.href = "investidor_home.html";
}
