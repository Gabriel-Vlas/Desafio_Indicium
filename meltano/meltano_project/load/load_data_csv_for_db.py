import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Configuração do banco de dados
DB_CONFIG = {
    "host": "db", 
    "database": "northwind",
    "user": "northwind_user",
    "password": "thewindisblowing",
    "port": 5432,
}

# Conectar ao banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Conexão bem-sucedida ao banco de dados!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela 'order_details' com chaves estrangeiras
def create_order_details_table():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL,
            discount DECIMAL(5, 2) NOT NULL,
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabela 'order_details' criada com sucesso!")
        conn.close()

# Diretório base onde as pastas com datas estão armazenadas
base_directory = "/opt/airflow/meltano/data/csv"

def get_latest_folder(directory):
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    if not folders:
        print("Nenhuma pasta encontrada.")
        return None
    
    # Ordenar pastas por nome assumindo que seguem um padrão
    latest_folder = max(folders)
    return os.path.join(directory, latest_folder)

# Função para carregar os dados do CSV mais recente
def load_data_from_csv():

    latest_folder = get_latest_folder(base_directory)

    if latest_folder:
        latest_csv = os.path.join(latest_folder, "order_details.csv")
        
        if os.path.exists(latest_csv):
            print(f"Carregando dados do arquivo: {latest_csv}")

            df = pd.read_csv(latest_csv)

            # Garantir que os tipos de dados estão corretos
            df['order_id'] = df['order_id'].astype(int)
            df['product_id'] = df['product_id'].astype(int)
            df['unit_price'] = df['unit_price'].astype(float)
            df['quantity'] = df['quantity'].astype(int)
            df['discount'] = df['discount'].astype(float)

            # Inserir os dados no banco
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                for index, row in df.iterrows():
                    insert_query = """
                    INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (order_id, product_id) DO NOTHING;
                    """
                    cursor.execute(insert_query, (
                        int(row['order_id']),
                        int(row['product_id']),
                        float(row['unit_price']),
                        int(row['quantity']),
                        float(row['discount'])
                    ))
                conn.commit()
                print("Dados inseridos com sucesso!")
                conn.close()
        else:
            print(f"O arquivo 'order_details.csv' não foi encontrado na pasta {latest_folder}.")
    else:
        print("Nenhuma pasta válida encontrada.")

# Função para consultar pedidos e seus detalhes e exportar para Excel
def fetch_orders_and_details():
    try:
        # Conectar ao banco de dados
        conn = connect_to_db()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            o.order_id,
            o.customer_id,
            o.order_date,
            d.product_id,
            d.unit_price,
            d.quantity,
            d.discount
        FROM orders o
        JOIN order_details d
            ON o.order_id = d.order_id
        ORDER BY o.order_id;
        """
        
        cursor.execute(query)
        print(f"Executou query")
        result = cursor.fetchall()
        
        # Converter o resultado da consulta em DataFrame
        columns = ['order_id', 'customer_id', 'order_date', 'product_id', 'unit_price', 'quantity', 'discount']
        df = pd.DataFrame(result, columns=columns)
        
        # Exportar o DataFrame para Excel
        df.to_excel("/opt/airflow/meltano/data/objetivo_final/LH_ED_GABRIEL_VLASSOV.xlsx", index=False,engine='openpyxl')
        print("Consulta exportada para Excel com sucesso!")
        
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Criar a tabela order_details se não existir
create_order_details_table()

# Carrega dados do CSV mais recente
load_data_from_csv()

# Consultar pedidos e seus detalhes e exportar para Excel
fetch_orders_and_details()
