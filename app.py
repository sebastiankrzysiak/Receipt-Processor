from flask import Flask
from routes.receipts import receipts_bp

app = Flask(__name__)
app.register_blueprint(receipts_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")