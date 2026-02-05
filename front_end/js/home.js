const API = "http://localhost:5001";
const API_INVESTIDOR = "http://localhost:5002";
const cpf = localStorage.getItem("cpf_cliente");

if (!cpf) {
  alert("Sessão inválida. Faça login novamente.");
  window.location.href = "index.html";
}

/* SALDO */
async function carregarCliente() {
  try {
    const res = await fetch(`${API}/cliente/${cpf}`);
    const cliente = await res.json();

    document.getElementById("saldo").innerText =
      `R$ ${Number(cliente.saldo_cc).toFixed(2)}`;
  } catch {
    alert("Erro ao carregar dados");
  }
}

/* EXTRATO */
async function carregarExtrato() {
  try {
    const res = await fetch(`${API}/cliente/transacoes/${cpf}`);
    const extrato = await res.json();

    const div = document.getElementById("extrato");
    div.innerHTML = "";

    extrato.forEach(op => {
      const item = document.createElement("div");
      item.className = "extrato-item";
      item.innerHTML = `
        <span>${op.tipo.toUpperCase()}</span>
        <span>R$ ${Number(op.valor).toFixed(2)}</span>
      `;
      div.appendChild(item);
    });
  } catch {
    console.log("Erro ao carregar extrato");
  }
}

/* OPERAÇÕES */
async function operar(tipo, inputId) {
  const valor = Number(document.getElementById(inputId).value);
  if (valor <= 0) return alert("Valor inválido");

  await fetch(`${API}/cliente/operacao/${cpf}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tipo, valor })
  });

  document.getElementById(inputId).value = "";
  carregarCliente();
  carregarExtrato();
}

function depositar() {
  operar("deposito", "valor-deposito");
}

function sacar() {
  operar("saque", "valor-saque");
}


function irAlterarSenha() {
  window.location.href = "alterar_senha.html";
}
function irAtualizar() {
  window.location.href = "atualizar_dados.html";
}


function logout() {
  localStorage.removeItem("cpf_cliente");
  window.location.href = "index.html";
}

/* INIT */
carregarCliente();
carregarExtrato();
function toggleMenu() {
  const menu = document.getElementById("menu");

  if (menu.style.display === "block") {
    menu.style.display = "none";
  } else {
    menu.style.display = "block";
  }
}
document.addEventListener("click", (e) => {
  const menu = document.getElementById("menu");
  const btn = document.querySelector(".menu-btn");

  if (!menu.contains(e.target) && !btn.contains(e.target)) {
    menu.style.display = "none";
  }
});
async function deletarConta() {
  const confirmar = confirm(
    "⚠️ ATENÇÃO\n\n" +
    "Esta ação é PERMANENTE.\n" +
    "Sua conta será excluída definitivamente.\n\n" +
    "Deseja continuar?"
  );

  if (!confirmar) return;

  try {
    const res = await fetch(`${API}/cliente/${cpf}`, {
      method: "DELETE"
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.erro || "Erro ao deletar conta");
      return;
    }

    alert("Conta excluída com sucesso");

    localStorage.removeItem("cpf_cliente");
    window.location.href = "index.html";

  } catch (err) {
    console.error(err);
    alert("Erro de conexão com o servidor");
  }
}

function irInvestidor() {
  window.location.href = "investidor_opcoes.html";
}
