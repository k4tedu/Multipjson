from flask import Flask, request, jsonify
from multipjson.generate_json import build_json_array

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_json():
    data = request.get_json()
    try:
        json_data = build_json_array(
            total=int(data.get('total')),
            fields=data.get('fields'),
            values=data.get('values'),
            prefix=data.get('prefix', ''),
            suffix=data.get('suffix', ''),
            id_type=data.get('id_type', 'normal'),
            email_domain=data.get('email_domain', 'demo.org'),
            phone_digits=int(data.get('phone_digits', 12))
        )
        return jsonify(json_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
