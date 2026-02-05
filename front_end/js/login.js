const API = "http://localhost:5001";

async function login() {
  const cpf = document.getElementById("cpf").value.trim();
  const senha = document.getElementById("senha").value.trim();
  const erro = document.getElementById("erro");

  erro.textContent = "";

  if (!cpf || !senha) {
    erro.textContent = "CPF e senha são obrigatórios";
    return;
  }

  try {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cpf, senha })
    });

    if (!res.ok) {
      erro.textContent = "CPF ou senha inválidos";
      return;
    }

    const data = await res.json();

    console.log("Resposta backend:", data);

    // 🔥 SALVA OS DADOS DA SESSÃO
    localStorage.setItem("cliente_id", data.id);
    localStorage.setItem("cpf_cliente", cpf);

    window.location.href = "home.html";

  } catch (e) {
    erro.textContent = "Erro ao conectar com o servidor";
    console.error(e);
  }
}
