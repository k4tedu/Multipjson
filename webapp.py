from flask import Flask, render_template, request, send_file, redirect, url_for
from multipjson.generate_json import build_json_array
import os
import json

app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total = int(request.form.get('total'))
        fields = request.form.get('fields')
        values = request.form.get('values')
        prefix = request.form.get('prefix', '')
        suffix = request.form.get('suffix', '')
        id_type = request.form.get('id_type', 'normal')
        email_domain = request.form.get('email_domain', 'demo.org')
        phone_digits = int(request.form.get('phone_digits', 12))

        try:
            json_data = build_json_array(
                total=total,
                fields=fields,
                values=values,
                prefix=prefix,
                suffix=suffix,
                id_type=id_type,
                email_domain=email_domain,
                phone_digits=phone_digits
            )
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"

        # Simpan ke folder output
        output_path = os.path.join("output", "web_output.json")
        os.makedirs("output", exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)

        # Salin juga ke folder static supaya bisa diakses via /static/web_output.json
        os.makedirs("static", exist_ok=True)
        static_output_path = os.path.join("static", "web_output.json")
        with open(static_output_path, 'w') as f:
            json.dump(json_data, f, indent=2)

        return render_template('result.html', data=json_data)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
