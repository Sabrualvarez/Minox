import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv


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

    sql_gemini = gemini
    chat = sql_gemini.start_chat(enable_automatic_function_calling=True)
    print(chat.send_message("¿Cuál es el visor que menos pesa?").text)


if __name__ == "__main__":
    main()
