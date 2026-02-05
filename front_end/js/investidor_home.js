console.log("INVESTIDOR HOME CARREGADO");

const API_INVESTIDOR = "http://localhost:5002";
const cpf = localStorage.getItem("cpf_cliente");

let investimentoSelecionado = null;
let tickerSelecionado = null;
let graficoYF = null;
let graficoPatrimonio = null;
let acaoSelecionada = null;

/* ===============================
   VALIDA SESSÃO
================================ */
if (!cpf) {
  alert("Sessão inválida. Faça login novamente.");
  window.location.href = "index.html";
}

/* ===============================
   CARREGAR PATRIMÔNIO
================================ */
async function carregarPatrimonio() {
  try {

    const res = await fetch(`${API_INVESTIDOR}/patrimonio/${cpf}`);
    const data = await res.json();

    if (data.erro) return alert(data.erro);

    const patrimonio = Number(data.patrimonio_total) || 0;
    const rentabilidade = Number(data.retorno_percentual) || 0;

    document.getElementById("patrimonio").innerText =
      `R$ ${patrimonio.toFixed(2)}`;

    const rentEl = document.getElementById("rentabilidade");
    rentEl.innerText = `${rentabilidade.toFixed(2)}%`;
    rentEl.style.color = rentabilidade >= 0 ? "green" : "red";

    document.getElementById("projecao").innerText =
      `R$ ${(patrimonio * 1.12).toFixed(2)}`;

  } catch (err) {
    console.error(err);
  }
}

/* ===============================
   INVESTIMENTOS FIXOS
================================ */
async function carregarInvestimentos() {
  try {
    const res = await fetch(`${API_INVESTIDOR}/investimentos/${cpf}`);
    const resposta = await res.json();

    const investimentos = resposta.investimentos || resposta || [];

    const lista = document.getElementById("lista-investimentos");
    lista.innerHTML = "";

    investimentoSelecionado = null;

    const filtrados = investimentos.filter(inv =>
      !inv.ticker &&
      Number(inv.valor_investido || 0) > 0
    );

    if (!filtrados.length) {
      lista.innerHTML = "<p>Nenhum investimento ainda</p>";
      return;
    }

    filtrados.forEach(inv => {
      const item = document.createElement("div");
      item.className = "investimento-item";

      item.innerHTML = `
        <strong>Investimento ${inv.id_investimento}</strong>
        <p>Valor aplicado: R$ ${Number(inv.valor_investido).toFixed(2)}</p>
      `;

      item.onclick = () =>
        selecionarInvestimento(inv.id_investimento, item);

      lista.appendChild(item);
    });

  } catch (err) {
    console.error(err);
  }
}


function selecionarInvestimento(id, elemento) {

  investimentoSelecionado = id;

  document.querySelectorAll(".investimento-item")
    .forEach(el => el.classList.remove("ativo"));

  elemento.classList.add("ativo");
}

/* ===============================
   APORTE
================================ */
async function acaoAporte() {

  const valor = Number(document.getElementById("valor-aporte").value);

  if (!investimentoSelecionado)
    return alert("Selecione um investimento");

  if (!valor || valor <= 0)
    return alert("Valor inválido");

  try {

    const res = await fetch(
      `${API_INVESTIDOR}/investimentos/aporte/${investimentoSelecionado}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cpf, valor })
      }
    );

    const resp = await res.json();
    if (resp.erro) return alert(resp.erro);

    alert("Aporte realizado com sucesso");

    document.getElementById("valor-aporte").value = "";
    await atualizarDashboard();

  } catch (e) {
    console.error(e);
  }
}

/* ===============================
   RESGATE
================================ */
async function acaoResgate() {

  const valor = Number(document.getElementById("valor-resgate").value);

  if (!investimentoSelecionado)
    return alert("Selecione um investimento");

  if (!valor || valor <= 0)
    return alert("Valor inválido");

  try {

    const res = await fetch(
      `${API_INVESTIDOR}/investimentos/resgate/${investimentoSelecionado}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cpf, valor })
      }
    );

    const resp = await res.json();
    if (resp.erro) return alert(resp.erro);

    alert("Resgate realizado com sucesso");

    document.getElementById("valor-resgate").value = "";
    await atualizarDashboard();

  } catch (e) {
    console.error(e);
  }
}

/* ===============================
   GRÁFICO PATRIMÔNIO
================================ */
async function gerarGraficoPatrimonio() {

  try {

    const res = await fetch(`${API_INVESTIDOR}/investimentos/${cpf}`);
    const resposta = await res.json();

    const investimentos = resposta.investimentos || [];

    if (!investimentos.length) return;

    const labels = investimentos.map(inv =>
      inv.ticker ? inv.ticker : `Investimento ${inv.id_investimento}`
    );

    const valores = investimentos.map(inv =>
      Number(inv.custo_total || inv.valor_investido || 0)
    );

    const ctx = document.getElementById("graficoPatrimonio").getContext("2d");

    if (graficoPatrimonio)
      graficoPatrimonio.destroy();

    graficoPatrimonio = new Chart(ctx, {
      type: "pie",
      data: { labels, datasets: [{ data: valores }] },
      options: { responsive: true, maintainAspectRatio: false }
    });

  } catch (err) {
    console.error(err);
  }
}

/* ===============================
   BUSCAR ATIVO
================================ */
async function buscarAtivo() {

  const ticker = document.getElementById("ticker").value.trim();
  if (!ticker) return alert("Digite um ticker");

  try {

    const resp = await fetch(`${API_INVESTIDOR}/analises/mercado/${ticker}`);
    const dados = await resp.json();

    tickerSelecionado = dados.ticker;

    document.getElementById("yf-nome").innerText = dados.ticker;
    document.getElementById("yf-preco").innerText =
      `R$ ${Number(dados.preco_atual).toFixed(2)}`;

    const variacao = Number(dados.rentabilidade_12m_percentual);
    const variacaoEl = document.getElementById("yf-variacao");

    variacaoEl.innerText = `${variacao.toFixed(2)}%`;
    variacaoEl.style.color = variacao >= 0 ? "green" : "red";

    gerarGraficoYFinance(
      dados.preco_12m_inicial,
      dados.preco_12m_final
    );

  } catch (e) {
    console.error(e);
  }
}

function limparBusca() {

  tickerSelecionado = null;

  document.getElementById("ticker").value = "";
  document.getElementById("yf-nome").innerText = "-";
  document.getElementById("yf-preco").innerText = "-";
  document.getElementById("yf-variacao").innerText = "-";
}

/* ===============================
   COMPRAR AÇÃO
================================ */
async function comprarAcao() {

  const valor = Number(document.getElementById("valor-compra-acao").value);

  if (!tickerSelecionado)
    return alert("Busque um ativo primeiro");

  if (!valor || valor <= 0)
    return alert("Valor inválido");

  try {

    const res = await fetch(`${API_INVESTIDOR}/acoes/comprar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cpf,
        ticker: tickerSelecionado,
        valor_investir: valor
      })
    });

    const resp = await res.json();
    if (resp.erro) return alert(resp.erro);

    alert("Compra realizada com sucesso");

    document.getElementById("valor-compra-acao").value = "";

    await carregarAcoes();

  } catch (e) {
    console.error(e);
  }
}

/* ===============================
   LISTAR AÇÕES
================================ */
async function carregarAcoes() {
  try {
    const res = await fetch(`${API_INVESTIDOR}/acoes/cliente/${cpf}`);
    let data = await res.json();

    let acoes = Array.isArray(data) ? data : data.acoes || [];

    const lista = document.getElementById("lista-acoes");
    lista.innerHTML = "";

    acaoSelecionada = null;

    const filtradas = acoes.filter(acao =>
      Number(acao.quantidade || 0) > 0 &&
      Number(acao.custo_total || 0) > 0
    );

    if (!filtradas.length) {
      lista.innerHTML = "<p>Nenhuma ação comprada</p>";
      return;
    }

    filtradas.forEach(acao => {
      const item = document.createElement("div");
      item.className = "investimento-item";

      item.innerHTML = `
        <strong>${acao.ticker}</strong>
        <p>Quantidade: ${acao.quantidade}</p>
        <p>Total investido: R$ ${Number(acao.custo_total).toFixed(2)}</p>
      `;

      item.onclick = () => selecionarAcaoVenda(acao, item);

      lista.appendChild(item);
    });

  } catch (e) {
    console.error("Erro ao carregar ações:", e);
  }
}

/* ===============================
   SELECIONAR AÇÃO
================================ */
function selecionarAcaoVenda(acao, elemento) {

  acaoSelecionada = acao;

  document
    .querySelectorAll("#lista-acoes .investimento-item")
    .forEach(el => el.classList.remove("ativo"));

  elemento.classList.add("ativo");

  document.getElementById("acao-venda-nome").innerText =
    `${acao.ticker} — ${acao.quantidade} ações disponíveis`;
}

/* ===============================
   VENDER AÇÃO
================================ */
async function venderAcao() {

  if (!acaoSelecionada)
    return alert("Selecione uma ação da lista");

  const quantidade = Number(
    document.getElementById("valor-venda-acao").value
  );

  if (!quantidade || quantidade <= 0)
    return alert("Digite uma quantidade válida");

  try {

    const res = await fetch(`${API_INVESTIDOR}/acoes/vender`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        cpf,
        id_investimento: acaoSelecionada.id_investimento,
        quantidade
      })
    });

    const resp = await res.json();
    if (resp.erro) return alert(resp.erro);

    alert("Venda realizada com sucesso");

    document.getElementById("valor-venda-acao").value = "";
    acaoSelecionada = null;

    await carregarAcoes();

  } catch (e) {
    console.error(e);
  }
}

/* ===============================
   GRÁFICO YFINANCE
================================ */
function gerarGraficoYFinance(precoInicial, precoFinal) {

  const ctx = document.getElementById("graficoYFinance").getContext("2d");

  if (graficoYF)
    graficoYF.destroy();

  graficoYF = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["12 meses atrás", "Hoje"],
      datasets: [{
        data: [precoInicial, precoFinal],
        borderWidth: 2,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });
}

/* ===============================
   ATUALIZAR DASHBOARD
================================ */
async function atualizarDashboard() {
  await carregarPatrimonio();
  await carregarInvestimentos();
  await gerarGraficoPatrimonio();
  await carregarAcoes();
}

/* ===============================
   NAVEGAÇÃO
================================ */
function voltarConta() {
  window.location.href = "home.html";
}

function logout() {
  localStorage.removeItem("cpf_cliente");
  window.location.href = "index.html";
}

function novoInvestimento() {
  window.location.href = "investimento_fixo_criar.html";
}

/* ===============================
   ABAS
================================ */
function mostrarAba(nomeAba) {

  document.querySelectorAll(".conteudo-aba")
    .forEach(aba => aba.classList.remove("ativa"));

  document.querySelectorAll(".aba")
    .forEach(btn => btn.classList.remove("ativa"));

  document.getElementById(`aba-${nomeAba}`)
    ?.classList.add("ativa");
}

/* ===============================
   INIT
================================ */
atualizarDashboard();
