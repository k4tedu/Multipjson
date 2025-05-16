from flask import Flask, request, Response
from multipjson.generate_json import build_json_array
import json

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_json():
    data = request.get_json()
    try:
        total = int(data.get('total', 0))
        fields = data.get('fields')
        values = data.get('values')

        if not total or not fields or not values:
            return Response(
                json.dumps({"error": "Missing required parameters: total, fields, or values"}),
                status=400,
                mimetype='application/json'
            )

        json_data = build_json_array(
            total=total,
            fields=fields,
            values=values,
            prefix=data.get('prefix', ''),
            suffix=data.get('suffix', ''),
            id_type=data.get('id_type', 'normal'),
            email_domain=data.get('email_domain', 'demo.org'),
            phone_digits=int(data.get('phone_digits', 12))
        )

        return Response(
            json.dumps(json_data, indent=2),
            mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}),
            status=400,
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
