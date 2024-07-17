from flask import Flask, redirect, request, session, url_for, render_template_string
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la aplicación de Facebook
FB_APP_ID = 'your_app_id'
FB_APP_SECRET = 'your_app_secret'
REDIRECT_URI = 'http://localhost:5000/callback'

# URL de autenticación de Facebook
AUTH_URL = (
    f"https://www.facebook.com/v12.0/dialog/oauth"
    f"?client_id={FB_APP_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=instagram_basic,instagram_manage_insights"
    f"&response_type=code"
)

@app.route('/')
def index():
    return redirect(AUTH_URL)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code is None:
        return 'Error: No se recibió el código de autenticación.'

    # Intercambiar el código por un token de acceso
    token_url = (
        f"https://graph.facebook.com/v12.0/oauth/access_token"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&client_secret={FB_APP_SECRET}"
        f"&code={code}"
    )

    token_response = requests.get(token_url)
    token_data = token_response.json()
    access_token = token_data.get('access_token')

    if access_token is None:
        return 'Error: No se pudo obtener el token de acceso.'

    # Renderizar la página con el token de acceso
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Gallery</title>
    </head>
    <body>
        <div class="galery"></div>
        <div class="contenedor-galery">
            <button id="prev">Previous</button>
            <button id="next">Next</button>
        </div>
        <script>
            const token = '{{ access_token }}';
        </script>
        <script src="{{ url_for('static', filename='gallery.js') }}"></script>
    </body>
    </html>
    ''', access_token=access_token)

if __name__ == '__main__':
    app.run(debug=True)
