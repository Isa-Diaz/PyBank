const API_INVESTIDOR = "http://localhost:5002";
const cpf = localStorage.getItem("cpf_cliente");

if (!cpf) {
  alert("Sessão inválida");
  window.location.href = "index.html";
}

async function irHomeInvestidor() {
  try {
    const res = await fetch(`${API_INVESTIDOR}/investidor/${cpf}`);

    if (res.ok) {
      window.location.href = "investidor-home.html";
      return;
    }

    if (res.status === 404) {
      alert("Você ainda não possui conta investidora");
      return;
    }

    alert("Erro ao verificar conta investidora");

  } catch (err) {
    console.error(err);
    alert("Erro de conexão com investimentos");
  }
}
