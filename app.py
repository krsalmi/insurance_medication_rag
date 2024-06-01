# app.py
from flask import Flask, request, jsonify
from rag import initialize_agent

app = Flask(__name__)
agent = initialize_agent()

@app.route('/api/generate', methods=['POST'])
def generate():
    print("called")
    data = request.get_json()
    input_text = data.get('text')
    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        response = agent.query(input_text)
        return jsonify({'output': str(response)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)