const API = "http://localhost:5001";
const cpf = localStorage.getItem("cpf_cliente");

if (!cpf) {
  alert("Sessão inválida");
  window.location.href = "index.html";
}

/* ELEMENTOS */
const nome = document.getElementById("nome");
const email = document.getElementById("email");
const telefone = document.getElementById("telefone");
const correntista = document.getElementById("correntista");
const msg = document.getElementById("msg");

/* ================= CARREGAR DADOS ================= */
async function carregarDados() {
  try {
    const res = await fetch(`${API}/cliente/${cpf}`);
    const data = await res.json();

    if (data.erro) {
      msg.textContent = data.erro;
      return;
    }

    nome.value = data.nome || "";
    email.value = data.email || "";
    telefone.value = data.telefone || "";
    correntista.checked = !!data.correntista;

  } catch (err) {
    console.error(err);
    msg.textContent = "Erro ao carregar dados";
  }
}

/* ================= ATUALIZAR ================= */
async function atualizar() {
  msg.textContent = "";
  msg.style.color = "red";

  try {
    const res = await fetch(`${API}/cliente/${cpf}`, {
      method: "PATCH", // ✔ correto
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nome: nome.value.trim(),
        email: email.value.trim(),
        telefone: telefone.value.trim(),
        correntista: correntista.checked
      })
    });

    const data = await res.json();

    /* 🔒 VALIDAÇÃO LÓGICA (MS2) */
    if (data.erro) {
      msg.textContent = data.erro;
      return;
    }

    /* fallback extra (caso use outro padrão) */
    if (data.success === false) {
      msg.textContent = data.mensagem || "Erro ao atualizar dados";
      return;
    }

    /* SUCESSO REAL */
    msg.style.color = "green";
    msg.textContent = "Dados atualizados com sucesso";

  } catch (err) {
    console.error(err);
    msg.textContent = "Erro de conexão";
  }
}

/* ================= VOLTAR ================= */
function voltar() {
  window.location.href = "home.html";
}

/* INIT */
carregarDados();
