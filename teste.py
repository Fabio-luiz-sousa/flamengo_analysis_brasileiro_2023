import fitz
import numpy as np
import pandas as pd

#função que pega as informações de todas as paginas dos pdfs
def get_info_page_pdf(number_page):
    list_arrays=list()
    # doc armazena o pdf
    doc = fitz.open('src/rodada_1.pdf')
    for i in range(0,number_page):
        # pega a primeira pagina
        page1 = doc.load_page(i)
        #procura as tabelas na pagina
        table = page1.find_tables()

        # lista com as informações das tabelas
        list_tables = table.tables[0].extract()
        # arrray para armazenar as info das tabelas
        list_tables_info = list()
        # loop para armazenas as infos no array
        for i in np.arange(0,len(list_tables)):
            list_tables_info.append(list_tables[i])
        #print(list_tables_info)
        for i in np.arange(0,len(list_tables_info[0])):
            # list comprehension para tirar os valores nulos das listas
            list_tables_info[0][i] = [data for data in list_tables_info[0][i] if data is not None]
        list_arrays.append(list_tables_info[0][i])
    return list_arrays

list_arrays = get_info_page_pdf(3)
print(list_arrays)
#print(list(list_arrays[1]))
#função que cria um arquivo csv com as informações ddos pdfs
def write_info_csv(list_arrays):
    df = pd.DataFrame()
    team_home_and_away = list_arrays[0][1][0][1].split('X')
    df['rodada'] = [list_arrays[0][0][0][3]]

    df['time_casa'] = [team_home_and_away[0]]

    df['time_visitante'] = [team_home_and_away[1]]

    df['horario'] = [list_arrays[0][2][0][3]]

    df['estadio'] = [list_arrays[0][2][0][5]]

    df['arbitro'] = [list_arrays[0][5][0][1]]

    df['var'] = [list_arrays[0][11][0][1]]

    df['acrescimo_1_tempo'] = [list_arrays[0][19][0][3]]

    df['acrescimo_2_tempo'] = [list_arrays[0][19][0][7]]

    result_team_home_and_away_fisrt_time = list_arrays[0][20][0][0][23:28].split('X')
    df['time_casa_resultado_1_tempo'] = [result_team_home_and_away_fisrt_time[0]]
    df['time_visitante_resultado_1_tempo'] = [result_team_home_and_away_fisrt_time[1]]

    result_team_home_and_away_final_time = list_arrays[0][20][0][1][17:22].split('X')
    df['time_casa_resultado_final'] = [result_team_home_and_away_final_time[0]]
    df['time_visitante_resultado_final'] = [result_team_home_and_away_final_time[1]]

    df['tecnico_flamengo'] = [list_arrays[1][2][0][1]]

    sum_gols = int(df['time_casa_resultado_final'])+int(df['time_visitante_resultado_final'])
    list_time_goals = list()
    list_which_time = list()
    list_type_goals = list()
    list_name_player = list()
    list_team_player_goal = list()
    for i in range(1,sum_gols+1):
        list_time_goals.append(list_arrays[1][10+i][0][0])
        list_which_time.append(list_arrays[1][10+i][0][1])
        list_type_goals.append(list_arrays[1][10+i][0][3])
        list_name_player.append(list_arrays[1][10+i][0][4])
        list_team_player_goal.append(list_arrays[1][10+i][0][5])
        df['tempo_gols'] = [list_time_goals]
        df['1T/2T_gols'] = [list_which_time]
        df['tipo_gols'] = [list_type_goals]
        df['jogadores_gols'] = [list_name_player]
        df['time_jogadores_gols'] = [list_team_player_goal]
    
    list_time_yellow_cards = list()
    list_which_time_yellow_cards = list()
    list_name_player_yellow_card = list()
    list_team_player_goal_yellow_card = list()
    list_motivo_yellow_card = list()
    count=0
    if 'Cartões Vermelhos' not in list_arrays[1][11+sum_gols+2][0]:
        for i in range(10+sum_gols+5,19):
            list_time_yellow_cards.append(list_arrays[1][i+count][0][0])
            list_which_time_yellow_cards.append(list_arrays[1][i][0][1])
            list_name_player_yellow_card.append(list_arrays[1][i][0][3])
            list_team_player_goal_yellow_card.append(list_arrays[1][i][0][4])
            list_motivo_yellow_card.append(list_arrays[1][i+1][0][0])
            df['tempo_cartao_amarelo'] = [list_time_yellow_cards]
            df['1T/2T_cartao_amarelo'] = [list_which_time_yellow_cards]
            df['jogadores_cartao_amarelo'] = [list_name_player_yellow_card]
            df['time_jogadores_cartao_amarelo'] = [list_team_player_goal_yellow_card]
            df['motivo_cartao_amarelo'] = [list_motivo_yellow_card]
            
            
    
 
    print(df[['tempo_cartao_amarelo','1T/2T_cartao_amarelo','jogadores_cartao_amarelo','time_jogadores_cartao_amarelo','motivo_cartao_amarelo']])
    
#write_info_csv(list_arrays)

#arrumar a parte dos cartoes amarelos, arrumar um jeito para nao dar erro