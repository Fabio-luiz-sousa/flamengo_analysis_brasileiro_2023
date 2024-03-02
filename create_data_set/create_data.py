from pathlib import Path
import numpy as np
import pandas as pd


# função que insere as informações básicas das partidas no df
def insert_info_basics_df():

    columns = ['rodada','time_casa','placar_time_casa','tecnico_time_casa','capitao_time_casa','time_visitante',
               'placar_time_visitante','tecnico_time_visitante','capitao_time_visitante','data_jogo','horario_jogo',
               'estadio_jogo','arbitro_jogo','var_jogo','gols_jogo']
    df_info_basics = pd.DataFrame(columns=columns)

    list_info_basics = list()
    with open('src/info_basicas_partidas.txt','r') as arq_info_basics:
        for info in arq_info_basics:
            list_info_basics.append(info.strip().split(','))
    count=1
    for i,info in enumerate(list_info_basics):
        info_arbitros = info[24].split('·')
        list_info = [f'{count}',info[0],info[1],info[6],info[7],info[8],info[9],info[14],info[15],info[16],info[18],
                  f'{info[22]} /{info[23]}',info_arbitros[0],info_arbitros[4],list_info_basics[i][25:]]
        count+=1
        df_temp = pd.DataFrame([list_info],columns=columns)
        df_info_basics = pd.concat([df_info_basics,df_temp],ignore_index=True)
    return df_info_basics


# função que insere as informações da quantidade de publico nas partidas no df
def insert_info_publico_df():
    columns = ['publico_jogo']
    df_public_matches = pd.DataFrame(columns=columns)
    list_publico = list()
    with open('src/publico.txt','r') as arq_info_publico:
        for info in arq_info_publico:
            list_publico.append(info.strip())
    for i,info in enumerate(list_publico):
        list_public_matches  = [info]
        df_temp = pd.DataFrame([list_public_matches],columns=columns)
        df_public_matches=pd.concat([df_public_matches,df_temp],ignore_index=True)
    return df_public_matches


#função que insere informações sobre a renda das partidas no df
def insert_info_renda_df():

    columns = ['renda_jogo']
    df_renda_matches = pd.DataFrame(columns = columns)
    list_renda = list()
    with open('src/renda.txt','r') as arq_info_renda:
        for info in arq_info_renda:
            list_renda.append(info.strip())
    for i,info in enumerate(list_renda):
        list_renda_matches = [info]
        df_temp = pd.DataFrame([list_renda_matches],columns=columns)
        df_renda_matches = pd.concat([df_renda_matches,df_temp],ignore_index=True)
    return df_renda_matches


#função que insere as informações das escalações no df
def insert_info_escalacao():

    columns = ['escalacao_jogo']
    df_escalacao = pd.DataFrame(columns = columns)
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
    for i in range(0,len(list_escalacao_home_and_away)):
        list_escalacao = [list_escalacao_home_and_away[i]]
        df_temp = pd.DataFrame([list_escalacao],columns = columns)
        df_escalacao = pd.concat([df_escalacao,df_temp],ignore_index=True)
    return df_escalacao


#função que insere as informações dos cartoes e substiruições no df
def insert_info_cards_and_subs():
    #diretório que contem os arquivos pdf
    directory = Path('src')
    #ordena os pdf por ordem de modificação
    files = sorted(directory.glob('*.csv'), key=lambda file: file.stat().st_mtime)
    list_name_pdfs = list()
    for file in files:
       list_name_pdfs.append(file.name)
    list_arqs_csvs = list()
    count = 0
    for info in list_name_pdfs:
        #estava dando erro na leirura da rodada_9.csv entao tive que resetar o index
        if count == 9:
            df = pd.read_csv(f'src/rodada_9.csv')
            df.reset_index(drop=True,inplace=True)
            list_arqs_csvs.append(df)
        #estava dando erro na leirura da rodada_36.csv entao tive que resetar o index
        elif count == 36:
            df = pd.read_csv(f'src/rodada_36.csv')
            df.reset_index(drop=True,inplace=True)
            list_arqs_csvs.append(df)
        else:
            df = pd.read_csv(f'src/{info}')
            list_arqs_csvs.append(df)
        count+=1
    df_cards_and_subs = pd.concat(list_arqs_csvs,ignore_index=True)
    return df_cards_and_subs

# função que insere as estatisticas das partidas no df
def insert_info_stats_matches():

    columns1 = ['posse_time_casa','posse_time_visitante','quant_total_passes_time_casa','quant_passes_certos_time_casa','por_passes_certos_time_casa',
               'quant_total_passes_time_visitante','quant_passes_certos_time_visitante','por_passes_certos_time_visitante','quant_total_chutes_time_casa',
               'quant_chutes_certos_time_casa','por_chutes_certos_time_casa','quant_total_chutes_time_visitante','quant_chutes_certos_time_visitante',
               'por_chutes_certos_time_visitante','quant_total_desefas_goleiro_time_casa','quant_desefas_certas_goleiro_time_casa','por_desefas_certas_goleiro_time_casa',
               'quant_total_defesas_goleiro_time_visitante','quant_defesas_certas_goleiro_time_visitante','por_defesas_certas_goleiro_time_visitante']
    df_info_stats_matches1 = pd.DataFrame(columns = columns1)

    list_info_stats_matches = list()
    with open('src/estatisticas_partidas.txt','r') as arq_info_stats_matches:
        for info in arq_info_stats_matches:
            list_info_stats_matches.append(info.strip().split(','))
    for i,info in enumerate(list_info_stats_matches):
        passes_home_team =  list_info_stats_matches[i][6].split()
        passes_away_team =  list_info_stats_matches[i][7].split()
        shots_home_team =  list_info_stats_matches[i][9].split()
        shots_away_team =  list_info_stats_matches[i][10].split()
        defesas_home_team =  list_info_stats_matches[i][12].split()
        defesas_away_team =  list_info_stats_matches[i][13].split()
        list_info1 = [info[3],info[4],passes_home_team[2],passes_home_team[0],passes_home_team[4],passes_away_team[4],passes_away_team[2],passes_away_team[0],
                     shots_home_team[2],shots_home_team[0],shots_home_team[4],shots_away_team[4],shots_away_team[2],shots_away_team[0],
                     defesas_home_team[2],defesas_home_team[0],defesas_home_team[4],defesas_away_team[4],
                     defesas_away_team[2],defesas_away_team[0]]
       
        df_temp = pd.DataFrame([list_info1],columns=columns1)
        df_info_stats_matches1 = pd.concat([df_info_stats_matches1,df_temp],ignore_index=True)
        

    columns2 = ['quant_faltas_time_casa','quant_faltas_time_visitante','quant_escanteios_time_casa','quant_escanteios_time_visitante',
                    'quant_cruzamentos_time_casa','quant_cruzamentos_time_visitante','quant_contatos_time_casa','quant_contatos_time_visitante',
                    'quant_bote_defensivo_time_casa','quant_bote_defensivo_time_visitante','quant_cortes_time_casa','quant_cortes_time_visitante',
                    'quant_jogada_aereas_time_casa','quant_jogada_aereas_time_visitante','quant_defesas_time_casa','quant_defesas_time_visitante',
                    'quant_impedimentos_time_casa','quant_impedimentos_time_visitante','quant_tiros_meta_time_casa','quant_tiros_meta_time_visitante',
                    'quant_cobranca_lateral_time_casa','quant_cobranca_lateral_time_visitante','quant_bolas_longas_time_casa','quant_bolas_longas_time_visitante']

    df_info_stats_matches2 = pd.DataFrame(columns=columns2)
    list_info_extra_stats_matches = list()
    with open('src/estatisticas_extras_partidas.txt','r') as arq_info_estra_stats_matches:
        for info in arq_info_estra_stats_matches:
            list_info_extra_stats_matches.append(info.strip().split(','))
    for i,info in enumerate(list_info_extra_stats_matches):
        list_info2 = [info[2],info[4],info[5],info[7],info[8],info[10],info[11],info[13],info[16],info[18],info[19],info[21],info[22],
                        info[24],info[25],info[27],info[30],info[32],info[33],info[35],info[36],info[38],info[39],info[41]]
        df_temp = pd.DataFrame([list_info2],columns=columns2)
        df_info_stats_matches2 = pd.concat([df_info_stats_matches2,df_temp],ignore_index=True)
    df_info_stats_matches = pd.concat([df_info_stats_matches1,df_info_stats_matches2],axis=1)
    return df_info_stats_matches

df_info_basics = insert_info_basics_df()
df_public_matches = insert_info_publico_df()
df_renda_matches = insert_info_renda_df()
df_escalacao =  insert_info_escalacao()
df_cards_and_subs = insert_info_cards_and_subs()
df_info_stats_matches = insert_info_stats_matches()

def concat_all_dfs(df_info_basics,df_public_matches,df_renda_matches,df_escalacao,df_cards_and_subs,df_info_stats_matches):
    df_flamengo = pd.concat([df_info_basics,df_public_matches,df_renda_matches,df_info_stats_matches,df_cards_and_subs,df_escalacao],axis=1)
    df_flamengo.to_csv('src_final/estatiticas_flamengo_brasileiro_2023.csv',index=False)
    print(df_flamengo)
concat_all_dfs(df_info_basics,df_public_matches,df_renda_matches,df_escalacao,df_cards_and_subs,df_info_stats_matches)
