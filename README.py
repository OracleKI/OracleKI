from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Ganti dengan token akses GitHub Anda
    github_token = 'YOUR_GITHUB_TOKEN'

    # Mengambil data repositori publik dari GitHub API
    response = requests.get(
        'https://api.github.com/users/YOUR_USERNAME/repos',
        headers={'Authorization': f'token {github_token}'}
    )

    if response.status_code == 200:
        repos = response.json()
    else:
        repos = []

    return render_template('dashboard.html', repos=repos)

if __name__ == '__main__':
    app.run(debug=True)
