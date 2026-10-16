import json, os, threading
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "yasmim-convite-2027-troque-esta-chave")
BASE = os.path.dirname(os.path.abspath(__file__))
RSVP_FILE = os.path.join(BASE, "confirmacoes.json")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "yasmim2027")
# Dois convites, cada um com seu código de entrada
EVENTOS = {
    "piscina": {
        "codigo": os.environ.get("CODIGO_AMIGOS", "YASMIM18"),
        "horario": "14:00 às 16:00 continuaçaõ 18:00 às 23:00.",
        "inicio": "2027-02-20T14:00:00",
        "badge": "🏊 Festa na Piscina",
        "nota": "Leve roupa de banho e toalha 🩱",
    },
    "festa": {
        "codigo": os.environ.get("CODIGO_CONVITE", "YASMIM27"),
        "horario": "18:00 às 23:00",
        "inicio": "2027-02-20T18:00:00",
        "badge": "🥂 Festa de Aniversário",
        "nota": "",
    },
}
lock = threading.Lock()


def read(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def login_required(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        if not session.get("guest"):
            if request.path.startswith("/api/"):
                return jsonify(ok=False, msg="Entre no convite primeiro 💚"), 401
            return redirect(url_for("login"))
        return fn(*a, **kw)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        code = (request.form.get("code") or "").strip().upper()
        if len(name) < 2:
            return render_template("login.html", error="Digite seu nome para entrar 💚", name=name)
        tipo = next((k for k, v in EVENTOS.items() if v["codigo"].upper() == code), None)
        if not tipo:
            return render_template("login.html", error="Código do convite incorreto. Confira com a Yasmim 💚", name=name)
        session["guest"] = name[:60]
        session["tipo"] = tipo
        return redirect(url_for("index"))
    # permite link direto: /login?codigo=YASMIM27
    return render_template("login.html", error=None, name="", code=request.args.get("codigo", ""))


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    tipo = session.get("tipo", "festa")
    return render_template("index.html", guest=session["guest"], ev=EVENTOS[tipo], tipo=tipo)


@app.route("/api/rsvp", methods=["POST"])
@login_required
def rsvp():
    d = request.get_json(silent=True) or {}
    name = (d.get("name") or "").strip()
    status = d.get("status")
    try:
        guests = max(1, min(int(d.get("guests", 1)), 10))
    except (TypeError, ValueError):
        guests = 1
    if len(name) < 2 or status not in ("sim", "nao"):
        return jsonify(ok=False, msg="Preencha seu nome e escolha uma opção."), 400
    entry = {"convite": session.get("tipo", "festa"), "name": name[:80], "status": status, "guests": guests if status == "sim" else 0,
             "message": (d.get("message") or "").strip()[:300],
             "date": datetime.now().strftime("%d/%m/%Y %H:%M")}
    with lock:
        data = read(RSVP_FILE, [])
        data.append(entry)
        write(RSVP_FILE, data)
    msg = ("Presença confirmada! Mal posso esperar para te ver 💚" if status == "sim"
           else "Poxa, vamos sentir sua falta! Obrigada por avisar 💚")
    return jsonify(ok=True, msg=msg)


@app.route("/admin/confirmacoes")
def admin():
    if request.args.get("token") != ADMIN_TOKEN:
        return "Acesso negado", 403
    data = read(RSVP_FILE, [])
    def total(t):
        return sum(e["guests"] for e in data if e["status"] == "sim" and e.get("convite") == t)
    return jsonify(confirmados_piscina=total("piscina"), confirmados_festa=total("festa"), respostas=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
