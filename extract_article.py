from newspaper import Article
import requests

# Cabeceras para simular un navegador real (evita errores 401 o 403)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "Referer": "https://www.google.com/",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}
## Es el encabezado que se usa en las peticiones HTTP para simular un navegador web real.


def extract_article_text(url):
    """
    Extrae y devuelve el texto principal de un artículo a partir de su URL.
    """
    try:
        # Descarga manual del HTML (más seguro que article.download())
        response = requests.get(
            url, headers=HEADERS, timeout=20, allow_redirects=True
        )  ##
        print(
            f"[DEBUG] {response.status_code} {response.reason} -> final URL: {response.url}"
        )
        response.raise_for_status()  ##

        # Pasa el HTML descargado a Newspaper3k
        article = Article(url)
        article.set_html(response.text)  ### convierte el HTML en un objeto Newspaper3k
        article.parse()  ## parsea el HTML para extraer el contenido

        # Devuelve el objeto completo para poder acceder a title, authors, text...
        return article

    except Exception as e:
        print(f"❌ Error al extraer el artículo: {e}")
        return None


if __name__ == "__main__":
    test_url = "https://www.djangoproject.com/weblog/2024/aug/01/"

    article = extract_article_text(test_url)

    if article:
        print("✅ Artículo descargado correctamente.\n")
        print("📌 Título:", article.title)
        print("✍️  Autores:", article.authors)
        print("\n📰 Texto (primeros 600 caracteres):")
        print(article.text[:600])
    else:
        print("⚠️ No se pudo extraer el artículo.")
