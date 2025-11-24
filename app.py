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
            prev_fraud = request.form.get("prev_fraud", "no")

            score = 0.0
            reasons = []

            if amount > 50000:
                score += 0.5
                reasons.append("Very high transaction amount")
            elif amount > 20000:
                score += 0.35
                reasons.append("High transaction amount")
            elif amount > 10000:
                score += 0.2
                reasons.append("Moderate transaction amount")

            if location_diff > 200:
                score += 0.3
                reasons.append("Unusual location (very far from normal)")
            elif location_diff > 80:
                score += 0.2
                reasons.append("Location different from usual city")

            if device_age < 7:
                score += 0.25
                reasons.append("New / untrusted device used")
            elif device_age < 30:
                score += 0.15
                reasons.append("Recently used new device")

            if hour < 6 or hour > 22:
                score += 0.15
                reasons.append("Transaction at unusual time (night hours)")

            if prev_fraud == "yes":
                score += 0.25
                reasons.append("Account has previous fraud history")

            if score < 0:
                score = 0
            if score > 1:
                score = 1

            risk_percent = round(score * 100, 2)

            if risk_percent >= 70:
                risk_level = "High Risk"
                label = "⚠️ Highly Suspicious / Possible Fraud"
                color = "high"
            elif risk_percent >= 40:
                risk_level = "Medium Risk"
                label = "⚠️ Suspicious Transaction – Needs Review"
                color = "medium"
            else:
                risk_level = "Low Risk"
                label = "✅ Likely Legitimate Transaction"
                color = "low"

            if not reasons:
                reasons.append("No strong fraud signals detected")

            result = {
                "label": label,
                "risk_percent": risk_percent,
                "risk_level": risk_level,
                "color": color,
                "amount": amount,
                "device_age": device_age,
                "location_diff": location_diff,
                "hour": hour,
                "prev_fraud": prev_fraud,
                "reasons": reasons
            }

        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
