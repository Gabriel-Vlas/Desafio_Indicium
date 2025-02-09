import os
import psycopg2
import csv
from datetime import datetime

# Configurações do banco de dados
DB_CONFIG = {
    "host": "db",
    "database": "northwind",
    "user": "northwind_user",
    "password": "thewindisblowing",
    "port": 5432,
}

# Lista de tabelas do banco de dados
TABLES = [
    "categories",
    "products",
    "suppliers",
    "employees",
    "employee_territories",
    "territories",
    "region",
    "orders",
    "shippers",
    "us_states",
    "customer_customer_demo",
]

# Diretório local onde os arquivos CSV serão armazenados (fora do contêiner)
LOCAL_OUTPUT_DIR = "/opt/airflow/meltano/data/postgres"

# Função para extrair dados de uma tabela e salvar em CSV
def extract_table_to_local(table_name):
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Executar a consulta
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        # Criar diretório local com data da extração
        execution_date = datetime.now().strftime("%Y-%m-%d")
        table_output_dir = os.path.join(LOCAL_OUTPUT_DIR, table_name, execution_date)
        os.makedirs(table_output_dir, exist_ok=True)

        # Salvar CSV
        output_file_csv = os.path.join(table_output_dir, f"{table_name}.csv")
        with open(output_file_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(colnames)
            writer.writerows(rows)
        print(f"✅ Dados extraídos: {output_file_csv}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao processar {table_name}: {e}")

# Função para extrair todas as tabelas
def extract_all_tables():
    for table in TABLES:
        extract_table_to_local(table)

if __name__ == "__main__":
    extract_all_tables()
