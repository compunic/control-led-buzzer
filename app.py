
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)
# Status awal
status = {
    "lampu": "off",
    "buzzer": "off"
}
# =========================
# GET STATUS ESP32
# =========================
@app.route("/status", methods=["GET"])
def get_status():
    print(status)
    return jsonify(status)
# =========================
# SET LAMPU
# =========================
@app.route("/lampu/<state>", methods=["GET"])
def set_lampu(state):
    state = state.lower()

    if state not in ["on", "off"]:
        return jsonify({
            "success": False,
            "message": "Status lampu harus on atau off"
        }), 400

    status["lampu"] = state

    return jsonify({
        "success": True,
        "lampu": status["lampu"],
        "buzzer": status["buzzer"]
    })


# =========================
# SET BUZZER
# =========================
@app.route("/buzzer/<state>", methods=["GET"])
def set_buzzer(state):
    state = state.lower()

    if state not in ["on", "off"]:
        return jsonify({
            "success": False,
            "message": "Status buzzer harus on atau off"
        }), 400

    status["buzzer"] = state

    return jsonify({
        "success": True,
        "lampu": status["lampu"],
        "buzzer": status["buzzer"]
    })


# =========================
# SET LAMPU + BUZZER
# =========================
@app.route("/set", methods=["GET"])
def set_status():
    lampu = request.args.get("lampu")
    buzzer = request.args.get("buzzer")

    if lampu is not None:
        lampu = lampu.lower()

        if lampu not in ["on", "off"]:
            return jsonify({
                "success": False,
                "message": "lampu harus on atau off"
            }), 400

        status["lampu"] = lampu

    if buzzer is not None:
        buzzer = buzzer.lower()

        if buzzer not in ["on", "off"]:
            return jsonify({
                "success": False,
                "message": "buzzer harus on atau off"
            }), 400

        status["buzzer"] = buzzer

    return jsonify({
        "success": True,
        "lampu": status["lampu"],
        "buzzer": status["buzzer"]
    })

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

