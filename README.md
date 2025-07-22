Resumen del Proyecto: Chatbot Inteligente Minox (IA + RAG)

Tu proyecto consiste en desarrollar un chatbot inteligente que responda preguntas sobre productos de la marca Minox, integrando técnicas de inteligencia artificial basadas en un sistema RAG (Retrieval-Augmented Generation).¿En qué se basa tu proyecto?
Base de conocimiento estructurada:
Utilizas un archivo Excel (Proyecto_IA.xlsx) que contiene información detallada de productos Minox: modelos, precios, peso, dimensiones, número de material (SAP), etc.

Recuperación semántica (RAG):
Se generan embeddings (representaciones vectoriales) de cada producto usando la API de Cohere, lo que permite buscar productos relevantes aunque el usuario no escriba exactamente el nombre del modelo.

Generación de respuestas con lenguaje natural:
Una vez recuperada la información más relevante del Excel, se pasa como contexto a Gemini (Google) para generar respuestas claras, naturales y profesionales, como lo haría un experto humano.

Interacción en lenguaje natural:
El usuario puede hacer preguntas del tipo:

“¿Cuánto pesa el modelo DTC 1200?”

“¿Qué productos pesan menos de 500 g?”

“¿Cuál es el número de material del visor RS-4?”

Y el chatbot responde combinando la búsqueda semántica con generación inteligente.
