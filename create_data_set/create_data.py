from pathlib import Path
import numpy as np
import pandas as pd

df_info = pd.DataFrame()

# função que cria o df contendo as informações basicas as partidas
def insert_info_basics_df(df_info):
    list_goals = list()
    list_info_basics = list()
    with open('src/info_basicas_partidas.txt','r') as arq_info_basics:
        for info in arq_info_basics:
            list_info_basics.append(info.strip().split(','))
    count=1
    for i,info in enumerate(list_info_basics):
        df_info.loc[i,'rodada'] = f'{count}'
        df_info.loc[i,'time_casa'] = info[0]
        df_info.loc[i,'placar_time_casa'] = info[1]
        df_info.loc[i,'tecnico_time_casa'] = info[6]
        df_info.loc[i,'capitao_time_casa'] = info[7]
        df_info.loc[i,'time_visitante'] = info[8]
        df_info.loc[i,'placar_time_visitante'] = info[9]
        df_info.loc[i,'tecnico_time_visitante'] = info[14]
        df_info.loc[i,'capitao_time_visitante'] = info[15]
        df_info.loc[i,'data_jogo'] = info[16]
        df_info.loc[i,'horario_jogo'] = info[18]
        df_info.loc[i,'estadio_jogo'] = f'{info[22]} /{info[23]}'
        info_arbitros = info[24].split('·')
        df_info.loc[i,'arbitro_jogo'] = info_arbitros[0]
        df_info.loc[i,'var_jogo'] = info_arbitros[4]
        list_goals.append(list_info_basics[i][25:])
        df_info['gols_jogo'] = list_goals
        count+=1
    
        
insert_info_basics_df(df_info)

def insert_info_publico_df(df_info):
    list_publico = list()
    with open('src/publico.txt','r') as arq_info_publico:
        for info in arq_info_publico:
            list_publico.append(info.strip())
    for i,info in enumerate(list_publico):
        df_info.loc[i,'publico_jogo'] = info
insert_info_publico_df(df_info)

def insert_info_renda_df(df_info):
    list_renda = list()
    with open('src/renda.txt','r') as arq_info_renda:
        for info in arq_info_renda:
            list_renda.append(info.strip())
    for i,info in enumerate(list_renda):
        df_info.loc[i,'renda_jogo'] = info
insert_info_renda_df(df_info)

def insert_info_escalacao(df_info):
    l=list()
    list_escalacao_home = list()
    list_escalacao_away = list()
    list_escalacao_home_and_away = list()
    with open('src/escalacao_time_casa.txt','r') as arq_info_escalacao:
        for info in arq_info_escalacao:
            if info.startswith('Flamengo'):
                info_new = info.strip().split(',')
                list_escalacao_home_and_away.append(info_new[1:])
    with open('src/escalacao_time_visitante.txt','r') as arq_info_basics:
        for info in arq_info_basics:
            if info.startswith('Flamengo'):
                info_new = info.strip().split(',')
                list_escalacao_home_and_away.append(info_new[1:])
    
    df_info['escalacao_flamengo'] = list_escalacao_home_and_away
        
    
insert_info_escalacao(df_info)

def inser_info_stats_matches(df_info):
    list_info_stats_matches = list()
    with open('src/estatisticas_partidas.txt','r') as arq_info_stats_matches:
        for info in arq_info_stats_matches:
            list_info_stats_matches.append(info.strip().split(','))
    for i,info in enumerate(list_info_stats_matches):
        df_info.loc[i,'posse_time_casa'] = info[3]
        df_info.loc[i,'posse_time_visitante'] = info[4]

        passes_home_team =  list_info_stats_matches[i][6].split()
        df_info.loc[i,'quant_total_passes_time_casa'] = passes_home_team[2]
        df_info.loc[i,'quant_passes_certos_time_casa'] = passes_home_team[0]
        df_info.loc[i,'por_passes_certos_time_casa'] = passes_home_team[4]

        passes_away_team =  list_info_stats_matches[i][7].split()
        df_info.loc[i,'quant_total_passes_time_visitante'] = passes_away_team[4]
        df_info.loc[i,'quant_passes_certos_time_visitante'] = passes_away_team[2]
        df_info.loc[i,'por_passes_certos_time_visitante'] = passes_away_team[0]

        shots_home_team =  list_info_stats_matches[i][9].split()
        df_info.loc[i,'quant_total_chutes_time_casa'] = shots_home_team[2]
        df_info.loc[i,'quant_chutes_certos_time_casa'] = shots_home_team[0]
        df_info.loc[i,'por_chutes_certos_time_casa'] = shots_home_team[4]

        shots_away_team =  list_info_stats_matches[i][10].split()
        df_info.loc[i,'quant_total_chutes_time_visitante'] = shots_away_team[4]
        df_info.loc[i,'quant_chutes_certos_time_visitante'] = shots_away_team[2]
        df_info.loc[i,'por_chutes_certos_time_visitante'] = shots_away_team[0]

        defesas_home_team =  list_info_stats_matches[i][12].split()
        df_info.loc[i,'quant_total_desefas_time_casa'] = defesas_home_team[2]
        df_info.loc[i,'quant_desefas_certas_time_casa'] = defesas_home_team[0]
        df_info.loc[i,'por_desefas_certas_time_casa'] = defesas_home_team[4]

        defesas_away_team =  list_info_stats_matches[i][10].split()
        df_info.loc[i,'quant_total_defesas_time_visitante'] = defesas_away_team[4]
        df_info.loc[i,'quant_defesas_certas_time_visitante'] = defesas_away_team[2]
        df_info.loc[i,'por_defesas_certas_time_visitante'] = defesas_away_team[0]

    #print(list_info_stats_matches[0][6].split())
inser_info_stats_matches(df_info)
print(df_info)