# Desafio_Indicium

# Pipeline de Dados - Indicium

Este repositório contém um pipeline de dados projetado para automatizar a extração, processamento e carga de dados provenientes de duas fontes distintas: um banco de dados PostgreSQL e arquivos CSV. O pipeline realiza a extração diária dos dados, organiza esses dados em formatos apropriados e os grava tanto em arquivos locais quanto em um banco de dados PostgreSQL de destino. O objetivo final é permitir a análise integrada de dados, carregando informações de pedidos e seus detalhes, com a capacidade de reprocessar os dados conforme necessário.

## Requisitos

Antes de começar, é necessário ter o Docker instalado na sua máquina.

## Como Executar o Pipeline

1. **Instalar o Docker**
   - Faça o download e instale o Docker seguindo as instruções oficiais: [Docker Docs](https://www.docker.com/).

2. **Descompacte o Arquivo**
   - Extraia os arquivos do repositório fornecido.

3. **Executar os Contêineres**
   - Navegue até o diretório `postgres-docker` e execute o comando:
     ```bash
     docker-compose -f docker-compose.yml up -d
     ```
   - Em seguida, navegue até o diretório `apacheAirFlow` e execute:
     ```bash
     docker-compose -f docker-compose.yml up -d
     ```

4. **Acessar o Airflow**
   - Após os contêineres estarem em execução, abra o navegador e acesse [localhost:8080](http://localhost:8080).

5. **Executar o Pipeline**
   - No Airflow, procure pela DAG chamada `extract_postgres_and_csv_data`. Esta DAG executará todo o pipeline, realizando a extração e o carregamento dos dados.

## Conclusão

Após a execução bem-sucedida da DAG, o pipeline estará completo. Certifique-se de que todas as etapas foram concluídas corretamente antes de considerar a execução finalizada.

