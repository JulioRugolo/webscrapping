from flask import Flask
import requests
from bs4 import BeautifulSoup
from werkzeug.test import EnvironBuilder

app = Flask(__name__)

def extrair_titulos(url):
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/58.0.3029.110 Safari/537.3')
        }

        # Construindo o ambiente da solicitação local
        builder = EnvironBuilder(path=url, method='GET', headers=headers)
        env = builder.get_environ()

        with app.request_context(env):
            response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            resultados = []

            if 'leianoticias.com.br' in url:
                titulos_divs = soup.find_all('div', class_='eael-post-list-post')
                for div in titulos_divs:
                    titulo_tag = div.find('h2', class_='eael-post-list-title').find('a')
                    titulo = titulo_tag.text.strip()
                    link = titulo_tag['href']
                    imagem_div = div.find('div', class_='eael-post-list-thumbnail')
                    if imagem_div:
                        imagem_tag = imagem_div.find('img')
                        if imagem_tag:
                            if 'data:image' in imagem_tag['src']:
                                imagem = imagem_tag['data-lazy-src']
                            else:
                                imagem = imagem_tag['src']
                        else:
                            imagem = None
                    else:
                        imagem = None
                    resultados.append({'titulo': titulo, 'link': link, 'imagem': imagem})

            elif 'acontecebotucatu.com.br' in url:
                titulos_divs = soup.find_all('div', class_='blog-grid lidos-relacionados h-100')
                for div in titulos_divs:
                    titulo_tag = div.find('h4')
                    titulo = titulo_tag.text.strip()
                    link = titulo_tag.find('a')['href']
                    imagem_div = div.find('div', class_='blog-grid-img')
                    if imagem_div:
                        imagem_tag = imagem_div.find('img')
                        if imagem_tag:
                            if 'data:image' in imagem_tag['src']:
                                imagem = imagem_tag['data-src']
                            else:
                                imagem = imagem_tag['src']
                        else:
                            imagem = None
                    else:
                        imagem = None
                    resultados.append({'titulo': titulo, 'link': link, 'imagem': imagem})

            else:
                titulos_divs = soup.find_all('div', class_='col-md-4 col-sm-4 col-12 mb-25')
                for div in titulos_divs:
                    titulo_tag = div.find('h4')
                    titulo = titulo_tag.text.strip()
                    link = titulo_tag.find('a')['href']
                    imagem_tag = div.find('img')
                    if imagem_tag:
                        imagem = imagem_tag['src']
                    else:
                        imagem = None
                    resultados.append({'titulo': titulo, 'link': link, 'imagem': imagem})

            return resultados
        else:
            print(f"Erro ao acessar {url}. Status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []


@app.route('/')
def index():
    urls = [
        'https://leianoticias.com.br/',
        'https://acontecebotucatu.com.br/',
        # Adicione outras URLs conforme necessário
    ]
    titulos_por_site = {}
    for url in urls:
        titulos_por_site[url] = extrair_titulos(url)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Notícias Botucatu </title>
        <style>
            * {
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            .header {
                display: flex;
                position: sticky;
                top: 0;
                justify-content: space-between;
                align-items: center;
                background-color: #333;
                height: 60px;
                color: white;
                padding: 15px;
                text-align: center;
                margin-bottom: 20px;
            }
            .card {
                width: 200px;
                height: 350px;
                margin: 5px;
                border: 1px solid #ccc;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }

            a {
                color: inherit;
                text-decoration: none;
            }
            a.card:hover {
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
            }

            .card img {
                width: 100%;
                height: 200px; /* Altura fixa para todas as imagens */
                object-fit: cover; /* Mantém a proporção da imagem */
            }

            .card-content {
                padding: 15px;
                text-align: center;
                flex-grow: 1; /* O conteúdo ocupa todo o espaço restante */
            }

            .card h3 {
                font-size: 1rem;
                margin-bottom: 10px;
            }

            .card a {
                color: inherit;
                text-decoration: none;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 15px;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
            }

            @media (max-width: 768px) {
                .container {
                    justify-content: center;
                }

                .card {
                    margin-bottom: 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h2 style="text-align: center;">Notícias Botucatu</h2>
            <h3 style="text-align: center;">Fontes: Leia Notícias e Acontece Botucatu</h3>
        </div>
        <div class="container">
    """
    for url, noticias in titulos_por_site.items():
        for noticia in noticias:
            if noticia['imagem']:  # Verifica se há imagem
                html += f"<a href='{noticia['link']}' class='card'>"
                html += f"<img src='{noticia['imagem']}'" \
                        f" alt='Imagem da notícia'>"

                html += "<div class='card-content'>"
                html += f"<h3>{noticia['titulo']}</h3>"
                html += "</div>"
                html += "</a>"
    html += """
        </div>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    app.run(debug=True)
