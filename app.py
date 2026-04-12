from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:
        num1 = float(data.get("num1"))
        num2 = float(data.get("num2"))
        operation = data.get("operation")

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                return jsonify({"error": "Division by zero"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation"}), 400

        # Round result to avoid floating point issues like 0.1 + 0.2 = 0.30000000000000004
        result = round(result, 10)
        # Convert to int if it's a whole number
        if result == int(result):
            result = int(result)

        return jsonify({"result": result})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", 3000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    app.run(debug=debug, host=host, port=port)
