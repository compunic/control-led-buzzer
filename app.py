from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

status = {
    "gerakan": False,
    "lampu3": "off",
    "lampu4": "off",
    "mode3": "auto",
    "mode4": "auto"
}


@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status)


@app.route("/status", methods=["POST"])
def update_status():
    data = request.get_json()

    if "gerakan" in data:
        status["gerakan"] = data["gerakan"]

    # Hanya izinkan update lampu jika mode auto
    if status["mode3"] == "auto" and "lampu3" in data:
        status["lampu3"] = data["lampu3"]

    if status["mode4"] == "auto" and "lampu4" in data:
        status["lampu4"] = data["lampu4"]

    print("Status ESP32:", status)

    return jsonify({
        "success": True,
        "status": status
    })


# ==========================================
# CONTROL LAMPU (DARI DASHBOARD BROWSER)
# ==========================================

@app.route("/control", methods=["POST"])
def control():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Data JSON tidak ditemukan"
            }), 400

        lampu = data.get("lampu")
        mode = data.get("mode")
        lamp_status = data.get("status")

        # ======================================
        # VALIDASI LAMPU
        # ======================================
        if lampu not in ["lampu3", "lampu4"]:
            return jsonify({
                "success": False,
                "message": "Lampu tidak valid"
            }), 400

        # Tentukan key mode
        mode_key = "mode3" if lampu == "lampu3" else "mode4"

        # ======================================
        # UBAH MODE
        # ======================================
        if mode is not None:
            mode = mode.lower()

            if mode not in ["auto", "manual"]:
                return jsonify({
                    "success": False,
                    "message": "Mode harus auto atau manual"
                }), 400

            status[mode_key] = mode

            # Jika AUTO, kembalikan status
            if mode == "auto":
                return jsonify({
                    "success": True,
                    "message": f"{lampu} masuk mode AUTO",
                    "status": status
                })

        # ======================================
        # KONTROL MANUAL ON / OFF
        # ======================================
        if lamp_status is not None:
            lamp_status = lamp_status.lower()

            if lamp_status not in ["on", "off"]:
                return jsonify({
                    "success": False,
                    "message": "Status harus on atau off"
                }), 400

            # Pastikan mode MANUAL
            status[mode_key] = "manual"

            # Ubah status lampu
            status[lampu] = lamp_status

        return jsonify({
            "success": True,
            "message": f"Perintah {lampu} berhasil",
            "status": status
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================
# UPDATE STATUS (DARI SENSOR / ESP32)
# ==========================================

@app.route("/update", methods=["POST"])
def in_update_status():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Data JSON kosong"
            }), 400

        # Sensor Gerakan selalu di-update
        if "gerakan" in data:
            gerakan = data["gerakan"]
            if isinstance(gerakan, str):
                gerakan = (gerakan.lower() == "true")
            else:
                gerakan = bool(gerakan)

            status["gerakan"] = gerakan

        # HANYA update status lampu jika mode-nya sedang AUTO
        # Ini mencegah ESP32 menimpa status perintah manual dari user
        if status["mode3"] == "auto" and data.get("lampu3") in ["on", "off"]:
            status["lampu3"] = data["lampu3"]

        if status["mode4"] == "auto" and data.get("lampu4") in ["on", "off"]:
            status["lampu4"] = data["lampu4"]

        print("Update dari ESP32:", status)

        return jsonify({
            "success": True,
            "message": "Status berhasil diperbarui",
            "status": status
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/")
def index():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
