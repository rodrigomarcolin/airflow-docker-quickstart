# Airflow Docker Quickstart

Este repositório contém um código boilerplate para iniciar rapidamente um projeto com Airflow e Docker. Com este código, você pode começar a criar DAGs, executar workflows e monitorar o status de suas tarefas em minutos.

## Como usar

1. Clone este repositório em sua máquina local
2. Instale o Docker em sua máquina local, caso ainda não tenha feito isso
3. Execute o comando `docker-compose up` na raiz do projeto para iniciar o Airflow e os serviços relacionados
4. Acesse o Airflow Web UI em `localhost:8080` e comece a criar e executar DAGs

## Conteúdo do Projeto

Este repositório contém os seguintes arquivos e pastas:

- `docker-compose.yaml`: O arquivo de configuração do Docker Compose para iniciar o Airflow e outros serviços relacionados
- `dags/`: Pasta para armazenar seus DAGs personalizados
- `scripts/`: Pasta para armazenar scripts auxiliares para seus DAGs
- `plugins/`: Pasta para armazenar seus plugins personalizados para o Airflow

## Contribuição

Se você tiver sugestões ou melhorias para este projeto, sinta-se à vontade para abrir uma issue ou um pull request. Estamos sempre buscando melhorar o código e a experiência do usuário.
