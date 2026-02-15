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
import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convierte un artículo web (URL) a un o varios archivos de audio MP3."
    )

    parser.add_argument("--url", type=str, help="URL del artículo a convertir.")
    parser.add_argument(
        "--output",
        type=str,
        default="outputs",
        help="Carpeta donde se guardarán los archivos MP3 generados.",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        help="Código de idioma (ej. 'es', 'en') para forzar la conversión de texto a voz. si no se especifica,"
        " se intentará detectar automáticamente.",
    )

    parser.add_argument(
        "--slow",
        action="store_true",
        help="Si se activa, el audio se generará a una velocidad más lenta (modo lento).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=4000,
        help="Número máximo de caracteres por bloque de texto para generar cada MP3. Por defecto es 4000.",
    )

    return parser.parse_args()


def main():

    args = parse_args()
    url = (
        args.url or ""
    ).strip()  ## Si no se pasa URL, se asigna cadena vacía para evitar errores
    if not url:  ## Si no se proporcionó URL por argumentos, pedirla al usuario
        print("=== Conversor de Artículos a MP3 ===")
        url = input("Introduce la URL del artículo a convertir: ").strip()

    if not url:
        print("⚠️ No se introdujo ninguna URL. Saliendo...")
        return

    print("\n🔎 Extrayendo artículo...")
    article = extract_article_text(url)

    # Validar que la extracción fue correcta
    if (
        article is None or not getattr(article, "text", "").strip()
    ):  ## getattr sirve para  confirmar que el objeto tiene el atributo text y no da error si no lo tiene
        print("❌ No se pudo extraer texto del artículo. Revisa la URL o el sitio.")
        return

    titulo = getattr(article, "title", "") or "Articulo sin título"
    texto = article.text

    print(f"\n✅ Artículo extraído correctamente.")
    print(f"📌 Título: {titulo[:80]}")  # mostramos solo primeros 80 chars del título
    print(f"📏 Longitud del texto: {len(texto)} caracteres aprox.\n")

    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Convertir a MP3
    print("🎧 Convirtiendo texto a audio (esto puede tardar unos segundos)...")
    rutas_generadas, idioma = texto_a_mp3(
        titulo=titulo,
        texto=texto,
        carpeta_salida=args.output,
        idioma_forzado=args.lang,
        modo_lento=args.slow,
        limite_caracteres=args.limit,
    )

    print(f"\n✅ Conversión terminada. Idioma usado: {idioma}")
    print("Archivos generados:")
    for ruta in rutas_generadas:
        print(f"   - {ruta}")

    print(f"\n🎉 Listo. Puedes reproducir los MP3 desde la carpeta '{args.output}'.")


if __name__ == "__main__":
    main()
