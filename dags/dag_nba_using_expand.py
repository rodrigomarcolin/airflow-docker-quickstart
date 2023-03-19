import datetime
from airflow.decorators import task, dag, task_group
import pandas as pd
from airflow.utils.task_group import TaskGroup
import os
from airflow.models import Variable
import requests
import json
from bs4 import BeautifulSoup

def get_yesterday_date(today_date):
    """
        Calcula a data do dia anterior

        Parâmetros
        __________

        today_date : String
            Data do dia atual no formato YYYY-MM-DD

        
        Retorno
        _______

        yesterday_date : String
            Data do dia anterior no formato YYYY-MM-DD
    """


    return (datetime.datetime.strptime(today_date, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def get_team_info(team):
    """
        Gera lista com estatísticas dos jogadores de um time em um jogo da NBA

        Parâmetros
        __________

        team : Dict
            Dicionário com informações sobre o desempenho de um time em um jogo da NBA. 
            Extraído a partir do site de um jogo
        
        Retorno
        _______

        (team_name, players_info) : TUPLE
            team_name : STRING
                Nome do time
            players_info : DICT[]
                Lista de dicionários em que cada um possui informações sobre o desempenho
    """
    team_name = f"{team['teamCity']} {team['teamName']}"
    team_id = team['teamId']

    players_info = []
    
    for player in team['players']:
        player_stats = player['statistics']
        for key in player.keys():
            if key == "statistics":
                continue
            player_stats[key] = player[key]    

        player_stats['team'] = team_name
        player_stats['teamId'] = team_id
        players_info.append(player_stats)
    return team_name, players_info

@dag(
    "dag_nba", # Nome da dag
    schedule_interval = "00 10 * * *", # Agendamento da execução (CRON: https://crontab.guru/)
    start_date=datetime.datetime(2023, 3, 10), 
    catchup=True,
    max_active_runs=5,
)
def generate_dag():
    """
        Dag responsável por extrair diariamente informações sobre o desempenho
        dos jogadores nos jogos da NBA do dia anterior e armazená-las em CSVs
    """
    base_url = "https://www.nba.com" 
    doc = {}

    @task
    def create_folder(**kwargs):
        """
            Cria uma pasta no sistema operacional onde
            serão armazenados os CSVs com informações dos
            jogos do dia anterior

            Parâmetros
            __________

            kwargs : DICT 
                Keyword arguments passados pelo próprio Airflow com 
                base no contexto em que a task roda. Por exemplo, a 
                data em que a DAG está rodando pode ser acessada na
                chave 'ds' desse dicionário. 
        """
        folder_path = Variable.get('nba_games_folder')
        print(".\n\n\n" + kwargs['ds'] + '\n\n\n.')
        return os.makedirs(os.path.join(folder_path, get_yesterday_date(kwargs['ds'])), exist_ok=True)

    @task
    def scrape_games(foo, **kwargs):
        """
            Acessa o site da NBA com a listagem dos jogos do dia anterior e
            coleta o link de cada jogo

            Parâmetros
            __________

            kwargs : DICT 
                Keyword arguments passados pelo próprio Airflow com 
                base no contexto em que a task roda. Por exemplo, a 
                data em que a DAG está rodando pode ser acessada na
                chave 'ds' desse dicionário. 


            Retorno
            _______

            uri_list : STRING[]
                Lista em que cada elemento é a URI de um jogo do dia anterior
                no site da NBA
        """
        print(foo)

        date_execution = get_yesterday_date(kwargs['ds'])
        url = base_url + f"/games?date={date_execution}"

        print('.\n\n\n' + url + '\n\n\n.')

        response = requests.get(url).content.decode()
        soup = BeautifulSoup(response, 'html.parser')
        
        return [x['href'] for x in soup.find_all(attrs={"data-text" : "BOX SCORE"})]

    @task_group
    def scrape_game_info(game_uri):
        """
            TaskGroup responsável por receber a URI de um jogo e extrair
            informações sobre o desempenho dos jogadores a partir dele, 
            e armazená-las em um CSV.

            Parâmetros
            __________

            game_uri : STRING
                URI de um jogo no site da NBA
        """
        @task
        def scrape_game_site(game_uri):
            """
                Task responsável por receber a URI de um jogo e extrair
                informações sobre o desempenho dos times e jogadores

                Parâmetros
                __________

                game_uri : STRING
                    URI de um jogo no site da NBA


                Retorno
                _______

                game : DICT 
                    Contém informações sobre o jogo (times, estatísticas, 
                    lista de jogadores, etc)
            """
            url = base_url + game_uri
            response = requests.get(url).content.decode()
            soup = BeautifulSoup(response, 'html.parser')

            data = soup.find(id="__NEXT_DATA__").contents[0]
            game = json.loads(data)['props']['pageProps']['game']
            return game

        @task
        def save_game_info(game_info, **kwargs):
            """
                Task responsável por receber um dicionário contendo 
                informações sobre um jogo e extrair estatísticas sobre 
                o desempenho dos jogadores, armazenando-as em um CSV

                Parâmetros
                __________

                game_info : DICT
                    Contém informações sobre o jogo (times, estatísticas, 
                    lista de jogadores, etc)
            """
            path = os.path.join(Variable.get('nba_games_folder'), get_yesterday_date(kwargs['ds']))
            
            # Extrai nome e infos dos times
            home_team, home_players = get_team_info(game_info['homeTeam'])
            away_team, away_players = get_team_info(game_info['awayTeam'])

            # Cria CSV
            pd.DataFrame.from_records(home_players + away_players).to_csv(os.path.join(path, f"{home_team} vs {away_team}.csv"), index=False)
            
            return
        
        return save_game_info(scrape_game_site(game_uri))
    
    @task
    def done(foo):
        """
            Task dummy que é executada quando todos os taskgroups terminam
            de executar
        """
        print('Done')
        return 

    # scores = scrape_games()

    created = create_folder()
    scores = scrape_games(created)
    scrapers = scrape_game_info.expand(game_uri=scores)
    done(scrapers)

generate_dag() # Instancia DAG