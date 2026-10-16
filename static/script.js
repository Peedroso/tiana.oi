document.addEventListener("DOMContentLoaded", () => {
  // Revelar ao rolar
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("show"); io.unobserve(e.target); }
  }), { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  // Contagem regressiva (início do convite do convidado)
  const target = new Date(document.getElementById("countdown").dataset.start).getTime();
  const pad = n => String(n).padStart(2, "0");
  const tick = () => {
    let diff = Math.max(0, target - Date.now());
    const d = Math.floor(diff / 864e5); diff %= 864e5;
    const h = Math.floor(diff / 36e5); diff %= 36e5;
    const m = Math.floor(diff / 6e4);
    const s = Math.floor((diff % 6e4) / 1000);
    cdd.textContent = pad(d); cdh.textContent = pad(h); cdm.textContent = pad(m); cds.textContent = pad(s);
  };
  const cdd = document.getElementById("cd-d"), cdh = document.getElementById("cd-h"),
        cdm = document.getElementById("cd-m"), cds = document.getElementById("cd-s");
  tick(); setInterval(tick, 1000);

  // RSVP
  const form = document.getElementById("rsvp-form");
  const msg = document.getElementById("rsvp-msg");
  const guestsWrap = document.getElementById("guests-wrap");
  form.querySelectorAll("[name=status]").forEach(r => r.addEventListener("change", () => {
    guestsWrap.style.display = form.status.value === "sim" ? "flex" : "none";
  }));
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const body = { name: form.name.value, status: form.status.value, guests: form.guests.value, message: form.message.value };
    try {
      const r = await fetch("/api/rsvp", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const j = await r.json();
      msg.textContent = j.msg; msg.className = "feedback" + (j.ok ? "" : " err");
      if (j.ok) form.reset();
    } catch { msg.textContent = "Erro de conexão. Tente novamente."; msg.className = "feedback err"; }
  });

  // Copiar endereço
  const copyBtn = document.getElementById("copy-addr");
  if (copyBtn) copyBtn.addEventListener("click", async () => {
    const txt = "Rua dos Marmelos, 60, Portal dos Ipês 3, Cajamar";
    const out = document.getElementById("copy-msg");
    try { await navigator.clipboard.writeText(txt); out.textContent = "Endereço copiado! 💚"; }
    catch { out.textContent = txt; }
  });
});
