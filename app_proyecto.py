"""La idea de este proyecto es convertir un artículo existente en un archivo de audio reproducible
en formato mp3. Para ello puedes hacer uso de bibliotecas existenes como nltk (kit de
herramientas de lenguaje natural), newspaper3k y gtts (puedes seguir las instrucciones de
instalación de pip).
Puedes crear un programa al que proporcionarle una URL de un artículo a convertir para
luego manejar la conversión de texto a voz."""

"""app.py: Punto de entrada del proyecto.

- Pide una URL al usuario.
- Extrae el artículo con extract_article.py.
- Convierte el texto a audio con convertir_text_voz.py.
"""

from extract_article import (
    extract_article_text,
)  # Debe existir def extract_article(url)
from convertir_text_voz import texto_a_mp3  # Debe existir def texto_a_mp3(...)


def main():
    print("=== Conversor de Artículos a MP3 ===")
    url = input("Introduce la URL del artículo: ").strip()

    if not url:
        print("⚠️ No se introdujo ninguna URL. Saliendo...")
        return

    print("\n🔎 Extrayendo artículo...")
    article = extract_article_text(url)

    # Validar que la extracción fue correcta
    if article is None or not getattr(article, "text", "").strip():
        print("❌ No se pudo extraer texto del artículo. Revisa la URL o el sitio.")
        return

    titulo = getattr(article, "title", "") or "Articulo sin título"
    texto = article.text

    print(f"\n✅ Artículo extraído correctamente.")
    print(f"📌 Título: {titulo[:80]}")  # mostramos solo primeros 80 chars del título
    print(f"📏 Longitud del texto: {len(texto)} caracteres aprox.\n")

    # Convertir a MP3
    print("🎧 Convirtiendo texto a audio (esto puede tardar unos segundos)...")
    rutas_generadas, idioma = texto_a_mp3(
        titulo=titulo,
        texto=texto,
        carpeta_salida="outputs",
        idioma_forzado=None,  # o "es" si quieres forzarlo siempre a español
        modo_lento=False,  # pon True si quieres que hable más despacio
        limite_caracteres=4000,
    )

    print(f"\n✅ Conversión terminada. Idioma usado: {idioma}")
    print("Archivos generados:")
    for ruta in rutas_generadas:
        print(f"   - {ruta}")

    print("\n🎉 Listo. Puedes reproducir los MP3 desde la carpeta 'outputs'.")


if __name__ == "__main__":
    main()
