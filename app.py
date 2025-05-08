
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "veritabani.json"

# Yardımcı fonksiyon: JSON dosyasını yükle
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Yardımcı fonksiyon: JSON dosyasına yaz
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# GET ile listeleme
@app.route("/plaka/<heat_no>", methods=["GET"])
def get_plaka(heat_no):
    data = load_data()
    for p in data:
        if p["heat_no"] == heat_no:
            return jsonify(p)
    return jsonify({"error": "Kayıt bulunamadı"}), 404

# POST ile kayıt ekleme
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
