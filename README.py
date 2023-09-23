import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Tampilan awal
app.layout = html.Div([
    html.H1("GitHub Dashboard"),
    dcc.Input(id="repo-input", type="text", placeholder="Masukkan pemilik/nama repositori"),
    dcc.Graph(id="repo-stats"),
])

@app.callback(
    Output("repo-stats", "figure"),
    [Input("repo-input", "value")]
)
def update_repo_stats(repo_name):
    if repo_name:
        # Di sini Anda dapat menambahkan kode untuk mengambil data dari GitHub
        # dan menghasilkan visualisasi statistik repositori
        # Sebagai contoh, kita akan membuat grafik batang sederhana.
        data = {
            "Category": ["Stars", "Forks", "Watchers"],
            "Count": [10, 5, 15]  # Ganti ini dengan data aktual dari GitHub
        }

        fig = px.bar(data, x="Category", y="Count", title=f"Statistik Repositori: {repo_name}")

        return fig
    else:
        return {}

if __name__ == "__main__":
    app.run_server(debug=True)
