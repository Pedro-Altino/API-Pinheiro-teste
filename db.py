import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração de conexão com o banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'arena_pinheiro',
    'user': 'postgres',
    'password': '180482',
    'port': 5432
}

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def get_db_cursor(conn):
    """Retorna um cursor para executar queries"""
    return conn.cursor(cursor_factory=RealDictCursor)
