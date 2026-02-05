console.log("JS INVESTIDOR CARREGADO");

const form = document.getElementById("form-investidor");
const mensagem = document.getElementById("mensagem");

// 🔐 pega CPF da sessão
const cpfSalvo = localStorage.getItem("cpf_cliente");

if (!cpfSalvo) {
  alert("Sessão inválida. Faça login novamente.");
  window.locationx.href = "index.html";
}

// 👉 AUTOPREENCHER O INPUT
form.cpf.value = cpfSalvo;

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  mensagem.textContent = "";
  mensagem.className = "mensagem";

  const payload = {
    cpf: form.cpf.value, // 👈 vem preenchido automaticamente
    perfil_investidor: form.perfil.value,
    patrimonio_inicial: Number(form.patrimonio.value)
  };

  try {
    const res = await fetch("http://localhost:5002/investidor", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      mensagem.textContent = data.erro || "Erro ao criar conta investidora";
      mensagem.classList.add("erro");
      return;
    }

// ✅ MOSTRA MENSAGEM
mensagem.textContent =
  data.msg || "Conta investidora criada com sucesso!";
mensagem.classList.add("sucesso");

// ✅ SÓ REDIRECIONA SE FOR 201
if (res.status === 201) {
  localStorage.setItem("cpf_cliente", payload.cpf);

  setTimeout(() => {
    window.location.href = "investidor_home.html";
  }, 1200);
}

  } catch (err) {
    console.error(err);
    mensagem.textContent = "Erro ao conectar com o serviço de investimentos";
    mensagem.classList.add("erro");
  }
});

