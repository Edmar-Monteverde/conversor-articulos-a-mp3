# Conversor de Artículos a MP3 (Python)

Este proyecto recibe una **URL de un artículo**, extrae el texto principal
y lo convierte en **uno o varios archivos de audio MP3** usando Google Text-to-Speech (gTTS).

Es un proyecto práctico para aprender:

- Cómo consumir contenido desde una URL
- Cómo extraer texto de artículos web
- Cómo procesar texto (limpieza, división por oraciones, troceado en bloques)
- Cómo convertir texto a voz y guardar audios en MP3
- Cómo organizar un proyecto real en varios archivos de Python

---

## 🧩 Requisitos

- Python 3.x instalado
- Librerías de Python:

  - `requests`
  - `newspaper3k`
  - `gTTS`
  - `langdetect`


Si tienes el archivo `requirements.txt`, puedes instalarlas con:

```bash
pip install -r requirements.txt 
```

## 🧩 Cómo Ejecutarlo

1. Ir a la carpeta del proyecto
    ``` bash
   cd "conversor-articulos-a-mp3"
   ```

2. Ejecutar la aplicación:
    ```bash
    python main.py
    ```

3. Introducir la URL cuando lo pida  el programa, ejemplo:
    ```text
    === Conversor de Artículos a MP3 ===
    Introduce la URL del artículo: https://martinfowler.com/articles/microservices.html
    ```

4. Esperar a que se genere el audio MP3.
    Los archivos MP3 se generan en la carpeta: 
    outputs/


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








