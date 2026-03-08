# 🎧 Conversor de Artículos Web a MP3 (CLI en Python)

Este proyecto recibe una **URL de un artículo**, extrae el texto principal
y lo convierte en **uno o varios archivos de audio MP3** usando Google Text-to-Speech (gTTS).

Es una herramienta CLI orientada a automatización y procesamiento de contenido web.
---
## 🚀 Características

- Extracción automática de artículos (newspaper3k)

- Limpieza y procesamiento de texto

- División inteligente en bloques por oraciones

- Detección automática de idioma (langdetect)

- Soporte para idioma forzado (--lang)

- Modo audio lento (--slow)

- Control del tamaño de bloques (--limit)

- Logging profesional con --verbose

- Proyecto modular y estructurado

## 🧩 Requisitos

- Python 3.10 – 3.12 (recomendado)
- Dependencias:

  ```bash
    pip install -r requirements.txt 
   ```



## ▶️ Uso básico

1. Ir a la carpeta del proyecto
    ``` bash
   cd "conversor-articulos-a-mp3"
   ```

2. Ejecutar la aplicación:
    ```bash
    python src/main.py
    ```

3. Introducir la URL cuando lo pida  el programa, ejemplo:
    ```text
    === Conversor de Artículos a MP3 ===
    Introduce la URL del artículo: https://martinfowler.com/articles/microservices.html
    ```

4. Esperar a que se genere el audio MP3.
    Los archivos MP3 se generan en la carpeta: 
    outputs/

## ⚙️ Argumentos disponibles

    Tambien se puede ejecutar de la terminal, con los siguientes argumentos.

| Argumento   | Descripción                                             |
| ----------- | ------------------------------------------------------- |
| `--url`     | URL del artículo                                        |
| `--output`  | Carpeta donde se guardarán los MP3 (default: `outputs`) |
| `--lang`    | Idioma forzado (`es`, `en`, `pt`, etc.)                 |
| `--slow`    | Genera audio en modo lento                              |
| `--limit`   | Máximo de caracteres por bloque                         |
| `--verbose` | Activa mensajes de depuración (DEBUG)                   |

- Ejemplo básico
```bash
python src/main.py --url "https://martinfowler.com/articles/microservices.html"
```
- Forzar idioma
```bash
python src/main.py --url "https://example.com/articulo" --lang es
```
- Modo audio lento
```bash
python src/main.py --url "https://example.com/articulo" --slow
```
- Limitar tamaño de bloques
```bash
python src/main.py --url "https://example.com/articulo" --limit 1500
```
- Elegir carpeta de salida
```bash
python src/main.py --url "https://example.com/articulo" --output audios
```

## 🪵 Uso del Logging (--verbose)

El proyecto incluye logging estructurado para depuración.

Al activar --verbose, el programa mostrará información adicional sobre:

- Extracción del artículo

- Procesamiento del texto

- Conversión a audio

- Generación de archivos

Ejemplo:
```bash
python src/main.py --url "https://example.com" --verbose
```

Esto permite depurar el programa y entender mejor el flujo de ejecución.

## 📁 Estructura del proyecto

```text
.
├── src/
│   ├── main.py
│   ├── extract_article.py
│   └── convertir_text_voz.py
│
├── requirements.txt
├── outputs/
└── README.md

```


## Flujo  del Programa 

1.El usuario escribe una URL.

2.extract_article.py:

    - Descarga la página,

    - Extrae el título,

    - Extrae el texto principal.

3.convertir_text_voz.py:

    - Limpia el texto (quita URLs, espacios extra, etc.),

    - Divide el texto en bloques por oraciones,

    - Detecta el idioma del texto (langdetect),

    - Genera uno o varios archivos MP3 con gTTS.

    - Los MP3 se guardan en outputs/.

## 🌐 Páginas recomendadas para pruebas

Puedes probar con:

https://martinfowler.com/articles/microservices.html

https://realpython.com/python-logging/

https://medium.com/

https://dev.to/

https://blog.jetbrains.com/

⚠️ Algunos sitios pueden bloquear scraping.


## 🧠 Aprendizajes aplicados

 Este proyecto demuestra:

- 📌 Uso de argparse para CLI profesional

- 📌 Uso estructurado de logging con niveles (INFO / DEBUG)

- 📌 Manejo de dependencias externas

- 📌  Procesamiento de texto con expresiones regulares

- 📌 División inteligente de contenido en bloques

- 📌 Manejo de rutas con pathlib

- 📌 Modularización de código

- 📌 Buenas prácticas en estructura de proyecto

## ⚠️ Limitaciones actuales

- No traduce el texto (solo cambia idioma de voz)

- Algunos sitios bloquean la extracción

- No incluye tests automatizados (aún)




##👤 Autor

Edmar Monteverde


