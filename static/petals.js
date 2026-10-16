// Pétalas e brilhinhos caindo (usado no login e no convite)
(function () {
  const box = document.getElementById("petals");
  if (!box || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const icons = ["✨", "🤍", "🌿", "✿"];
  setInterval(() => {
    const el = document.createElement("span");
    const sparkle = Math.random() < 0.35;
    el.className = sparkle ? "sparkle" : "petal";
    if (sparkle) { el.textContent = icons[Math.floor(Math.random() * icons.length)]; el.style.fontSize = 10 + Math.random() * 10 + "px"; }
    else el.style.transform = `scale(${0.6 + Math.random()})`;
    el.style.left = Math.random() * 100 + "vw";
    el.style.setProperty("--x", (Math.random() * 160 - 80) + "px");
    el.style.animationDuration = 7 + Math.random() * 6 + "s";
    box.appendChild(el);
    setTimeout(() => el.remove(), 14000);
  }, 800);
})();
