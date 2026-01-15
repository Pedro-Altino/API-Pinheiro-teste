import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

os.environ["LC_MESSAGES"] = "C"
os.environ["LANG"] = "C"

DB_CONFIG = {
    'host': 'localhost',
    'database': 'arena_pinheiro',
    'user': 'postgres',
    'password': 'Asd45678910!',
    'port': 5432,
    'client_encoding': 'utf-8'
}

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except UnicodeDecodeError:
        print("Aviso: Falha de decodificação Unicode ao conectar. Tentando conexão simplificada...")
        try:
            config_simple = DB_CONFIG.copy()
            if 'client_encoding' in config_simple:
                del config_simple['client_encoding']
                
            conn = psycopg2.connect(**config_simple)
            conn.set_client_encoding('utf8')
            return conn
        except UnicodeDecodeError:
             print("ERRO CRÍTICO: Não foi possível conectar ao banco de dados e a mensagem de erro contém caracteres inválidos.")
             print("Verifique se:")
             print(f"1. O banco de dados '{DB_CONFIG['database']}' existe.")
             print(f"2. A senha para o usuário '{DB_CONFIG['user']}' está correta.")
             print("3. O PostgreSQL está rodando na porta 5432.")
             raise RuntimeError("Falha na conexão com o Banco de Dados (Erro de autenticação ou DB inexistente)")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
    except Exception as e:
        try:
            print(f"Erro ao conectar ao banco de dados: {e}")
        except:
            print("Erro ao conectar ao banco de dados (mensagem ilegível)")
        raise

def get_db_cursor(conn):
    """Retorna um cursor para executar queries"""
    return conn.cursor(cursor_factory=RealDictCursor)
