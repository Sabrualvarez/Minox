import os
import re
import sqlite3
import pandas as pd
from dotenv import load_dotenv


def generate_sql(model, question: str, columns: list[str]) -> str:
    """Ask Gemini to create a SQL query for the question."""
    system = (
        "Eres un asistente experto en SQL. "
        "Genera solo la consulta SQL necesaria para responder a la pregunta "
        "utilizando la tabla 'productos_minox' que contiene las columnas: "
        f"{', '.join(columns)}."
    )
    response = model.generate_content([system, question])
    text = response.text.strip()
    # Remove ``` blocks or leading 'sql' markers that could cause syntax errors
    text = re.sub(r"```(?:sql)?", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()
    return text


def answer_with_rows(model, question: str, rows: list[dict]) -> str:
    """Generate a final answer using the query results."""
    prompt = (
        "Responde a la pregunta solo con la siguiente informacion extraida de la base de datos:\n"
        f"{rows}\nPregunta: {question}"
    )
    return model.generate_content(prompt).text.strip()


def load_data(path: str) -> pd.DataFrame:
    """Load and clean the product spreadsheet."""
    df = pd.read_excel(path)
    df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    if 'Precio' in df.columns:
        df['Precio'] = (
            df['Precio']
            .astype(str)
            .apply(lambda x: str(x).replace('€', '').replace('.', '').replace(',', '.').strip())
        )
        df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
    return df


def setup_database(df: pd.DataFrame, db_path: str = "mydatabase.db") -> sqlite3.Connection:
    """Store the dataframe in a SQLite database."""
    conn = sqlite3.connect(db_path)
    df.to_sql('productos_minox', conn, if_exists='replace', index=False)
    return conn


def sql_query(query: str, connection: sqlite3.Connection):
    """Run a SQL SELECT query on the database."""
    return pd.read_sql_query(query, connection).to_dict(orient='records')


def load_gemini():
    """Initialise the Gemini client using the environment API key."""
    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise RuntimeError("google-generativeai is not installed") from exc

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not found")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def main():
    df = load_data("todo_junto.xlsx")
    conn = setup_database(df)
    gemini = load_gemini()
    columns = list(df.columns)

    while True:
        question = input("Pregunta (salir para terminar): ").strip()
        if question.lower() == "salir":
            break

        sql = generate_sql(gemini, question, columns)
        try:
            rows = sql_query(sql, conn)
        except Exception as exc:
            print(f"Error al ejecutar la consulta '{sql}': {exc}")
            continue

        answer = answer_with_rows(gemini, question, rows)
        print(answer)


if __name__ == "__main__":
    main()
