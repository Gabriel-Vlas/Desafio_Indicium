import os
import shutil
from datetime import datetime

# Obtém o caminho absoluto do diretório onde o script está localizado
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho do arquivo CSV de forma relativa ao script
CSV_SOURCE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "csv_fornecido", "order_details.csv")

# Função para copiar o arquivo CSV
def extract_csv_to_local():
    
    execution_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"./meltano/data/csv/{execution_date}"
    os.makedirs(output_dir, exist_ok=True)

    # Copia o arquivo CSV
    output_file = os.path.join(output_dir, "order_details.csv")
    shutil.copy(CSV_SOURCE_PATH, output_file)

    print(f"Arquivo CSV copiado para: {output_file}")

if __name__ == "__main__":
    extract_csv_to_local()
