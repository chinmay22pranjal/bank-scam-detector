from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", 0))
            device_age = float(request.form.get("device_age", 365))
            location_diff = float(request.form.get("location_diff", 0))
            hour = int(request.form.get("hour", 12))

            # ---- Simple rule-based "AI" for demo ----
            score = 0.0

            # High amount → more risky
            if amount > 20000:
                score += 0.5
            elif amount > 10000:
                score += 0.3
            elif amount > 5000:
                score += 0.15

            # Location far from usual
            if location_diff > 100:
                score += 0.3
            elif location_diff > 50:
                score += 0.2

            # Very new device
            if device_age < 30:
                score += 0.2
            elif device_age < 90:
                score += 0.1

            # Night time
            if hour < 6 or hour > 22:
                score += 0.1

            # Cap score between 0 and 1
            score = min(score, 1.0)

            if score >= 0.5:
                label = "⚠️ Fraudulent / Suspicious Transaction"
            else:
                label = "✅ Likely Legitimate Transaction"

            result = {
                "label": label,
                "risk": round(score * 100, 2),
                "amount": amount,
                "device_age": device_age,
                "location_diff": location_diff,
                "hour": hour,
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
