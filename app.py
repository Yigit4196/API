
from flask import Flask, request, jsonify, render_template_string, abort
import json
import os

app = Flask(__name__)

DATA_FILE = "veritabani.json"

# Yardımcı fonksiyonlar
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# HTML Şablon
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Plaka Bilgisi</title>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        h1 {{ color: #333; }}
        .kutu {{ border: 1px solid #aaa; padding: 15px; border-radius: 10px; max-width: 500px; }}
    </style>
</head>
<body>
    <h1>Plaka Bilgisi</h1>
    <div class="kutu">
        <p><strong>Heat No:</strong> {{ plaka["heat_no"] }}</p>
        <p><strong>Kalınlık:</strong> {{ plaka["kalinlik"] }}</p>
        <p><strong>Cinsi:</strong> {{ plaka["cins"] }}</p>
        <p><strong>Proje:</strong> {{ plaka["proje"] }}</p>
        <p><strong>Boyutlar:</strong> {{ plaka["boyutlar"] }}</p>
        <p><strong>Durum:</strong> {{ "Geldi" if plaka["geldi"] else "Gelmedi" }}</p>
    </div>
</body>
</html>
"""

@app.route("/plaka/<heat_no>", methods=["GET"])
def get_plaka(heat_no):
    data = load_data()
    for p in data:
        if p["heat_no"] == heat_no:
            return render_template_string(HTML_TEMPLATE, plaka=p)
    return abort(404)

@app.route("/api/ekle", methods=["POST"])
def add_plaka():
    data = load_data()
    yeni_kayit = request.get_json()

    if not yeni_kayit or "heat_no" not in yeni_kayit:
        return jsonify({"error": "Eksik veri"}), 400

    if any(p["heat_no"] == yeni_kayit["heat_no"] for p in data):
        return jsonify({"error": "Bu heat_no zaten var"}), 409

    data.append(yeni_kayit)
    save_data(data)
    return jsonify({"message": "Kayıt eklendi"}), 201

# Render uyumu
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
