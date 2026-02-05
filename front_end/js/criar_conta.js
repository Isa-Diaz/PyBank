const correntistaCheckbox = document.getElementById("correntista");
const saldoInput = document.getElementById("saldo_cc");
const form = document.getElementById("form-criar-conta");
const msg = document.getElementById("mensagem");

/* estado inicial */
saldoInput.readOnly = true;
saldoInput.value = "";

/* controla input de saldo */
correntistaCheckbox.addEventListener("change", () => {
  if (correntistaCheckbox.checked) {
    saldoInput.readOnly = false;
    saldoInput.focus();
  } else {
    saldoInput.readOnly = true;
    saldoInput.value = "";
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  msg.textContent = "";
  msg.style.color = "red";

  if (form.senha.value !== form.confirmar_senha.value) {
    msg.textContent = "As senhas não coincidem";
    return;
  }

  if (correntistaCheckbox.checked) {
    const saldo = Number(saldoInput.value);
    if (isNaN(saldo) || saldo < 0) {
      msg.textContent = "Saldo inicial inválido";
      return;
    }
  }

  const data = {
    nome: form.nome.value.trim(),
    cpf: form.cpf.value.trim(),
    telefone: form.telefone.value.trim(),
    email: form.email.value.trim(),
    senha: form.senha.value,
    correntista: correntistaCheckbox.checked,
    saldo_cc: correntistaCheckbox.checked ? Number(saldoInput.value) : 0
  };

  try {
    const resp = await fetch("http://localhost:5001/cliente", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const resultado = await resp.json();

    if (!resp.ok) {
      msg.textContent = resultado.erro || "Erro ao criar conta";
      return;
    }

    // ✅ sessão padronizada
    localStorage.setItem("cpf_cliente", data.cpf);

    window.location.href = "home.html";

  } catch (err) {
    msg.textContent = "Erro ao conectar com o servidor";
    console.error(err);
  }
});
