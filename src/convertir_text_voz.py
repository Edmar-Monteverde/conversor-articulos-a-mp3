"""convertir_text_voz.py: Convierte texto a voz utilizando gTTS y guarda el resultado en un archivo MP3."""

## Importanto librerias
import re

from gtts import gTTS
from pathlib import Path

# 1) obtener el titutlo del articulo para usarlo como nombre del archivo de audio
# 2) limpiar el texto del articulo para evitar problemas en la conversion a voz
# 3) dividir el texto en partes mas pequeñas para evitar limites de gTTS
# 4) #detectar el idioma del texto para usarlo en gTTS
# 5) convertir el texto a voz y guardar el archivo mp3


## Falta el codigo de descargar articulo usando extract_article.py

# Intentar usar langdetect si está instalado (para detectar idioma)
try:
    from langdetect import detect, LangDetectException
except Exception:
    detect = None
    LangDetectException = Exception


## funcion para obtener titulo para el audio
def slugify(
    text: str, default: str = "audio"
):  ## Slug= simple, obtenemos una version simplificada del texto para usarlo como nombre de archivo
    text = (
        text.strip().lower()
    )  ##elimina espacios al inicio y al final y convierte a minusculas
    text = re.sub(
        r"[^\w\s-]", "", text, flags=re.UNICODE
    )  ##elimina caracteres especiales
    text = re.sub(
        r"[\s_-]+", "-", text
    )  ##reemplaza espacios y guiones bajos por guiones
    text = re.sub(r"^-+|-+$", "", text)  ##elimina guiones al inicio y al final
    return text or default


## funcion para limpiar el texto o el parrafo
def clean_text(text: str) -> str:
    text = re.sub(r"http[s]?://\S+", "", text)  # quita URLs
    text = re.sub(r"[ \t]{2,}", " ", text)  # colapsa espacios
    text = re.sub(r"\n{3,}", "\n\n", text)  # normaliza saltos
    return text.strip()


def dividir_en_oraciones(texto: str):
    """
    Divide el texto en oraciones de forma sencilla usando expresiones regulares.

    """
    partes = re.split(
        r"([\.!?]\s+)", texto
    )  ## hace split por puntos, signos de exclamacion e interrogacion seguidos de espacio
    oraciones = []

    for i in range(0, len(partes), 2):
        frase = partes[i]  ## frases en posiciones pares
        separador = (
            partes[i + 1] if i + 1 < len(partes) else ""
        )  ## si hay un separador, lo toma de la posicion impar siguiente sino es vacio
        oracion_completa = (frase + separador).strip()
        if oracion_completa:
            oraciones.append(oracion_completa)

    return oraciones or [texto]


## funcion para dividir el texto en partes mas pequeñas
def dividir_texto_en_bloques_por_oraciones(
    texto: str,
    limite_caracteres: int = 4000,
):
    """
    Divide un texto largo en bloques más pequeños respetando las oraciones completas.
    Cada bloque tendrá un máximo aproximado de 'limite_caracteres'.
    """

    # 1) Dividir el texto en oraciones completas
    lista_oraciones = dividir_en_oraciones(texto)

    # 2) Variables de trabajo más claras
    bloques_finales = []  # Resultado final (lista de bloques)
    bloque_actual = []  # Oraciones que se están acumulando
    tamano_bloque = 0  # Conteo de caracteres del bloque actual

    # 3) Recorrer oraciones una por una
    for oracion in lista_oraciones:

        # Si agregar la oración supera el límite, cerramos este bloque
        if tamano_bloque + len(oracion) + 1 > limite_caracteres and bloque_actual:
            bloques_finales.append(" ".join(bloque_actual).strip())
            bloque_actual = [oracion]  # Nuevo bloque con la oración actual
            tamano_bloque = len(oracion)

        else:
            # Si aún cabe, agregamos la oración al bloque
            bloque_actual.append(oracion)
            tamano_bloque += len(oracion) + 1

    # 4) Si quedó contenido pendiente, guardarlo como último bloque
    if bloque_actual:
        bloques_finales.append(" ".join(bloque_actual).strip())

    # 5) Retornar al menos un bloque aunque el texto esté vacío
    return bloques_finales or [texto]


def detectar_idioma_del_texto(texto: str, idioma_por_defecto: str = "es") -> str:
    """
    Intenta detectar el idioma del texto usando langdetect.
    Si falla o no está instalado, devuelve un idioma por defecto.
    """

    # Intentar importar langdetect
    if detect is None:
        return idioma_por_defecto

    try:
        codigo_detectado = detect(texto)
    except LangDetectException:
        return idioma_por_defecto

    # Tabla simple de idiomas permitidos
    idiomas_soportados = {
        "es": "es",  # español
        "en": "en",  # inglés
        "pt": "pt",  # portugués
        "fr": "fr",  # francés
        "de": "de",  # alemán
        "it": "it",  # italiano
    }

    # Retornar el idioma detectado SI está en nuestra lista
    return idiomas_soportados.get(codigo_detectado.lower(), idioma_por_defecto)


def texto_a_mp3(
    titulo: str,
    texto: str,
    carpeta_salida: str = "outputs",
    idioma_forzado: str | None = None,
    modo_lento: bool = False,
    limite_caracteres: int = 4000,
):
    """
    Convierte un texto largo en uno o varios archivos MP3 usando gTTS.
    - Limpia el texto
    - Lo divide en bloques por oraciones
    - Detecta idioma (o usa idioma forzado)
    - Genera los MP3

    Devuelve: (lista_de_rutas_generadas, idioma_utilizado)
    """

    # Crear carpeta de salida si no existe
    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)

    # Limpiar el texto para evitar URLs y espacios extra
    texto_limpio = clean_text(texto)

    # Elegir el idioma:
    # → Si el usuario pasa uno forzado, se usa ese
    # → Si no, detectar automáticamente
    idioma_final = idioma_forzado or detectar_idioma_del_texto(texto_limpio)

    # Dividir texto en bloques manejables
    bloques = dividir_texto_en_bloques_por_oraciones(
        texto=texto_limpio,
        limite_caracteres=limite_caracteres,
    )

    # Crear nombre base del archivo
    nombre_base = slugify(titulo)[:60] or "audio"

    rutas_generadas = []

    # Si el texto cabe en un solo archivo, generar un solo MP3
    if len(bloques) == 1:
        ruta_mp3 = Path(carpeta_salida) / f"{nombre_base}.mp3"
        gTTS(text=bloques[0], lang=idioma_final, slow=modo_lento).save(str(ruta_mp3))
        rutas_generadas.append(ruta_mp3)

    # Si el texto es largo, generar varios MP3
    else:
        for numero, bloque in enumerate(bloques, start=1):
            ruta_mp3 = Path(carpeta_salida) / f"{nombre_base}-parte-{numero:02d}.mp3"
            gTTS(text=bloque, lang=idioma_final, slow=modo_lento).save(str(ruta_mp3))
            rutas_generadas.append(ruta_mp3)

    return rutas_generadas, idioma_final
