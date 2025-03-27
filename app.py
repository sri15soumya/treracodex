from flask import Flask, request, jsonify
from flask_cors import CORS  # Ensure CORS is imported
from search import run_agent  # Import your AI agent function

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to access API

# ✅ Root Route - Homepage
@app.route('/')
def home():
    return "Welcome to the AI Query API! Use POST /ask with a JSON payload."

# ✅ General AI Query Route
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query parameter is required!"}), 400

    response = run_agent(query)  # AI response based on any query
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
