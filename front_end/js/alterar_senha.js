const API = "http://localhost:5001";
const cpf = localStorage.getItem("cpf_cliente");

if (!cpf) {
  alert("Sessão inválida. Faça login novamente.");
  window.location.href = "index.html";
}

const msg = document.getElementById("msg");

async function alterarSenha() {
  msg.textContent = "";
  msg.style.color = "red";

  const senhaAtual = document.getElementById("senha_atual").value.trim();
  const novaSenha = document.getElementById("nova_senha").value.trim();
  const confirmar = document.getElementById("confirmar_senha").value.trim();

  if (!senhaAtual || !novaSenha || !confirmar) {
    msg.textContent = "Preencha todos os campos";
    return;
  }

  if (novaSenha !== confirmar) {
    msg.textContent = "As novas senhas não coincidem";
    return;
  }

  try {
    const res = await fetch(`${API}/alterar-senha`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cpf,
        senha_atual: senhaAtual,
        nova_senha: novaSenha
      })
    });

    const data = await res.json();

    if (!res.ok) {
      msg.textContent = data.erro || "Erro ao alterar senha";
      return;
    }

    msg.style.color = "green";
    msg.textContent = "Senha alterada com sucesso";

    setTimeout(() => {
      window.location.href = "home.html";
    }, 1200);

  } catch (e) {
    msg.textContent = "Erro de conexão com o servidor";
    console.error(e);
  }
}

function voltar() {
  window.location.href = "home.html";
}
