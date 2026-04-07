// ── Configuração ──
const API_BASE = "https://tradutor-gemini-fastapi.onrender.com";

const LANGUAGES = [
  { code: "en",    label: "Inglês" },
  { code: "pt-br", label: "Português (Brasil)" },
  { code: "es",    label: "Espanhol" },
  { code: "fr",    label: "Francês" },
  { code: "de",    label: "Alemão" },
  { code: "it",    label: "Italiano" },
];

// ── Elementos do DOM ──
const themeBtn      = document.getElementById("themeBtn");
const sourceLang    = document.getElementById("sourceLang");
const targetLang    = document.getElementById("targetLang");
const sourceText    = document.getElementById("sourceText");
const targetText    = document.getElementById("targetText");
const charCount     = document.getElementById("charCount");
const clearBtn      = document.getElementById("clearBtn");
const copyBtn       = document.getElementById("copyBtn");
const swapBtn       = document.getElementById("swapBtn");
const translateBtn  = document.getElementById("translateBtn");
const alertWarn     = document.getElementById("alertWarn");
const alertWarnText = document.getElementById("alertWarnText");
const alertError    = document.getElementById("alertError");
const alertErrorText= document.getElementById("alertErrorText");

// ── Tema ──
const savedTheme = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", savedTheme);

themeBtn.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
});

// ── Idiomas ──
async function loadLanguages() {
  try {
    const res = await fetch(`${API_BASE}/languages`);
    if (res.ok) {
      const data = await res.json();
      const langs = data.languages.map(code => {
        const found = LANGUAGES.find(l => l.code === code);
        return found || { code, label: code.toUpperCase() };
      });
      populateSelects(langs);
      return;
    }
  } catch (_) {
    console.warn("Backend indisponível — usando lista de idiomas padrão.");
  }
  populateSelects(LANGUAGES);
}

function populateSelects(langs) {
  // Destino: todos os idiomas, sem "Detectar idioma"
  targetLang.innerHTML = "";
  langs.forEach(l => {
    const opt = document.createElement("option");
    opt.value = l.code;
    opt.textContent = l.label;
    targetLang.appendChild(opt);
  });
  targetLang.value = "pt-br";

  // Origem: idiomas adicionados após "Detectar idioma" (que já está no HTML)
  langs.forEach(l => {
    const opt = document.createElement("option");
    opt.value = l.code;
    opt.textContent = l.label;
    sourceLang.appendChild(opt);
  });
}

loadLanguages();

// ── Contador de caracteres ──
sourceText.addEventListener("input", () => {
  const len = sourceText.value.length;
  charCount.textContent = `${len} / 2000`;
  charCount.classList.toggle("warn", len >= 1800);
  clearBtn.style.display = len > 0 ? "flex" : "none";
  swapBtn.disabled = sourceLang.value === "auto";
  hideAlerts();
});

// ── Limpar texto ──
clearBtn.addEventListener("click", () => {
  sourceText.value = "";
  targetText.value = "";
  charCount.textContent = "0 / 2000";
  charCount.classList.remove("warn");
  clearBtn.style.display = "none";
  copyBtn.style.display = "none";
  hideAlerts();
});

// ── Copiar tradução ──
copyBtn.addEventListener("click", async () => {
  if (!targetText.value) return;

  await navigator.clipboard.writeText(targetText.value);

  copyBtn.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
      style="width:15px;height:15px">
      <polyline points="20 6 9 17 4 12"/>
    </svg>`;
  copyBtn.classList.add("success");

  setTimeout(() => {
    copyBtn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        style="width:15px;height:15px">
        <rect x="9" y="9" width="13" height="13" rx="2"/>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
      </svg>`;
    copyBtn.classList.remove("success");
  }, 2000);
});

// ── Inverter idiomas ──
swapBtn.addEventListener("click", () => {
  if (sourceLang.value === "auto") return;

  const tmpLang = sourceLang.value;
  const tmpText = sourceText.value;

  sourceLang.value = targetLang.value;
  targetLang.value = tmpLang;
  sourceText.value = targetText.value;
  targetText.value = tmpText;

  charCount.textContent = `${sourceText.value.length} / 2000`;
  clearBtn.style.display = sourceText.value.length > 0 ? "flex" : "none";
  copyBtn.style.display = targetText.value.length > 0 ? "flex" : "none";
  hideAlerts();
});

// ── Mudança de idioma de origem ──
sourceLang.addEventListener("change", () => {
  swapBtn.disabled = sourceLang.value === "auto";
  hideAlerts();
});

// ── Mudança de idioma de destino ──
targetLang.addEventListener("change", () => {
  validateLangs();
});

// ── Validação de idiomas ──
function validateLangs() {
  if (sourceLang.value !== "auto" && sourceLang.value === targetLang.value) {
    showWarn("Escolha um idioma de destino diferente do idioma de origem.");
    return false;
  }
  hideAlerts();
  return true;
}

// ── Traduzir ──
translateBtn.addEventListener("click", async () => {
  hideAlerts();

  const text = sourceText.value.trim();

  if (!text) {
    showWarn("Digite um texto para traduzir.");
    return;
  }

  if (text.length > 2000) {
    showWarn("Limite de 2000 caracteres atingido.");
    return;
  }

  if (!validateLangs()) return;

  setLoading(true);

  try {
    const res = await fetch(`${API_BASE}/translate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        source_lang: sourceLang.value,
        target_lang: targetLang.value,
      }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();

    if (!data.translated_text) {
      showError("A tradução retornou vazia. Tente novamente.");
      return;
    }

    targetText.value = data.translated_text;
    copyBtn.style.display = "flex";

  } catch (err) {
    showError("Erro ao traduzir. Verifique se o backend está rodando e tente novamente.");
    console.error(err);
  } finally {
    setLoading(false);
  }
});

// ── Helpers ──
function setLoading(on) {
  translateBtn.classList.toggle("loading", on);
  translateBtn.disabled = on;
}

function showWarn(msg) {
  alertWarnText.textContent = msg;
  alertWarn.classList.add("show");
  alertError.classList.remove("show");
}

function showError(msg) {
  alertErrorText.textContent = msg;
  alertError.classList.add("show");
  alertWarn.classList.remove("show");
}

function hideAlerts() {
  alertWarn.classList.remove("show");
  alertError.classList.remove("show");
}