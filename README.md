# Airflow Docker Quickstart

Este repositório contém um código boilerplate para iniciar rapidamente um projeto com Airflow e Docker. Com este código, você pode começar a criar DAGs, executar workflows e monitorar o status de suas tarefas em minutos. **A versão do Airflow utilizada nesse projeto é a 2.5.1**

## Como usar

1. Clone este repositório em sua máquina local
2. Instale o Docker em sua máquina local, caso ainda não tenha feito isso
3. Execute o comando `docker-compose up` na pasta `compose/` para iniciar o Airflow e os serviços relacionados
4. Acesse o Airflow Web UI em `localhost:8080` e comece a criar e executar DAGs

## Conteúdo do Projeto

Este repositório contém os seguintes arquivos e pastas:

- `compose/docker-compose.yaml`: O arquivo de configuração do Docker Compose para iniciar o Airflow e outros serviços relacionados
- `compose/.env`: O arquivo com definição de algumas variáveis de ambiente que serão utilizadas pelo Docker para configurar o Airflow
- `dags/`: Pasta para armazenar seus DAGs personalizados
- `scripts/`: Pasta para armazenar scripts auxiliares para seus DAGs
- `plugins/`: Pasta para armazenar seus plugins personalizados para o Airflow

## Referências

1. https://towardsdatascience.com/setting-up-apache-airflow-with-docker-compose-in-5-minutes-56a1110f4122
