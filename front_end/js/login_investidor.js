const API_INVESTIDOR = "http://localhost:5002";

async function loginInvestidor() {
  const cpf = document.getElementById("cpf").value;
  const erro = document.getElementById("erro");

  erro.textContent = "";

  if (cpf.length !== 11) {
    erro.textContent = "CPF inválido";
    return;
  }

  try {
    const res = await fetch(`${API_INVESTIDOR}/investidor`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cpf })
    });

    const data = await res.json();

    // 🟢 CASO 1: já é investidor → ENTRA
    if (res.status === 409 && data.erro === "Cliente já é investidor") {
      localStorage.setItem("cpf_cliente", cpf);
      window.location.href = "investidor_home.html";
      return;
    }

    // 🟢 CASO 2: criado agora (201) → ENTRA
    if (res.status === 201) {
      localStorage.setItem("cpf_cliente", cpf);
      window.location.href = "investidor_home.html";
      return;
    }

    // 🔴 CASO 3: não é cliente
    erro.textContent = data.erro || "Acesso negado";

  } catch (err) {
    console.error(err);
    erro.textContent = "Erro de conexão com o servidor";
  }
}
