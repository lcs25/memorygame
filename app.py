# app.py
from flask import Flask, request, jsonify
from src.Engine import GameEngine

app = Flask(__name__)
game = GameEngine()

@app.post("/")
def index():
    start = game.next_move()
    return render_template('index.html', start)

# @app.post("/play")
# def post():
#     nxt, round_indicator  = game.next_move(payload)
#     return jsonify({"ok": True, "nxt": nxt, "indicator": round_indicator}), 200

@app.get("/play")
def get():
    nxt, round_indicator = game.next_move(payload)
    return jsonify({"ok": True, "nxt": nxt, "indicator": round_indicator}), 200

if __name__ == "__main__":
    app.run(debug=True)
