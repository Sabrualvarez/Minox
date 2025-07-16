# Minox
Sistema RAG/ chatbot proyecto IA

## Requisitos

El notebook utiliza varias librerías de Python para procesar los datos y conectarse con la API de Gemini:

* **pandas** – lectura y manipulación del archivo de Excel.
* **sqlite3** – base de datos SQLite donde se vuelca la información (incluida en Python).
* **google-generativeai** – cliente para el modelo Gemini.
* **python-dotenv** – carga de variables de entorno desde un archivo `.env`.

Para instalarlas se puede ejecutar:

```bash
pip install pandas google-generativeai python-dotenv
```

## Ejecución de `Proyecto_IA.ipynb`

1. Sitúa el archivo **`TOdo junto.xlsx`** en la misma carpeta que el notebook (o ajusta la ruta en el código).
2. Crea un archivo `.env` con tu clave de API de Gemini:

   ```
   GEMINI_API_KEY=<tu_clave_aqui>
   ```
3. Abre el notebook en Jupyter o Google Colab y ejecuta las celdas de forma secuencial. El cuaderno cargará los datos de Excel, generará una base de datos SQLite y realizará consultas utilizando el modelo de Gemini.

El módulo `dotenv` leerá el archivo `.env` para configurar la clave antes de iniciar la comunicación con la API.
