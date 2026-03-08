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
import argparse
from pathlib import Path
import logging

from extract_article import (
    extract_article_text,
)  # Debe existir def extract_article(url)
from convertir_text_voz import texto_a_mp3  # Debe existir def texto_a_mp3(...)


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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Activa mensajes de depuración adicionales(DEBUG).",
    )

    return parser.parse_args()


def configurar_logging(verbose: bool) -> None:
    """
    Configura el logging para mostrar mensajes de depuración si verbose es True.
    """
    if verbose:
        nivel = logging.DEBUG

        logging.basicConfig(level=nivel, format="%(levelname)s: %(message)s")
    else:
        nivel = logging.INFO
        logging.basicConfig(level=nivel, format="%(levelname)s: %(message)s")

    # Silenciar librerías ruidosas
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("gtts").setLevel(logging.WARNING)


def main():

    args = parse_args()
    configurar_logging(args.verbose)
    logger = logging.getLogger(__name__)
    url = (
        args.url or ""
    ).strip()  ## Si no se pasa URL, se asigna cadena vacía para evitar errores
    if not url:  ## Si no se proporcionó URL por argumentos, pedirla al usuario
        logger.info("=== Conversor de Artículos a MP3 ===")
        url = input("Introduce la URL del artículo a convertir: ").strip()

    if not url:
        logger.warning("⚠️ No se introdujo ninguna URL. Saliendo...")
        return

    logger.debug(f"Procesando URL: {url}")
    logger.info("Extrayendo artículo...")
    article = extract_article_text(url)

    # Validar que la extracción fue correcta
    if (
        article is None or not getattr(article, "text", "").strip()
    ):  ## getattr sirve para  confirmar que el objeto tiene el atributo text y no da error si no lo tiene
        logger.error(
            "❌ No se pudo extraer texto del artículo. Revisa la URL o el sitio."
        )
        return

    titulo = getattr(article, "title", "") or "Articulo sin título"
    texto = article.text

    logger.info(f"\n✅ Artículo extraído correctamente.")
    logger.info(
        f"📌 Título: {titulo[:80]}"
    )  # mostramos solo primeros 80 chars del título
    logger.info(f"📏 Longitud del texto: {len(texto)} caracteres aprox.\n")

    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Convertir a MP3
    logger.info("Convirtiendo texto a audio (esto puede tardar unos segundos)...")
    rutas_generadas, idioma = texto_a_mp3(
        titulo=titulo,
        texto=texto,
        carpeta_salida=args.output,
        idioma_forzado=args.lang,
        modo_lento=args.slow,
        limite_caracteres=args.limit,
    )

    logger.info(f"\n✅ Conversión terminada. Idioma usado: {idioma}")
    logger.info("Archivos generados:")
    for ruta in rutas_generadas:
        logger.info(f"   - {ruta}")

    logger.info(
        f"\n🎉 Listo. Puedes reproducir los MP3 desde la carpeta '{args.output}'."
    )


if __name__ == "__main__":
    main()
