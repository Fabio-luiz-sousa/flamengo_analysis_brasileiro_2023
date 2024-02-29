import numpy as np
import pandas as pd
import pdfplumber #tive usar pois estava dando problema para ler os cartoes vermelhos usanso so o pymupdf(fitz)
from pathlib import Path

df=pd.DataFrame()
#função que le os pdfs

def read_name_pdfs():
    #diretório que contem os arquivos pdf
    directory = Path('src')
    #ordena os pdf por ordem de modificação
    files = sorted(directory.glob('*.pdf'), key=lambda file: file.stat().st_mtime)
    list_name_pdfs = list()
    for file in files:
       list_name_pdfs.append(file.stem)
    return list_name_pdfs
list_name_pdfs = read_name_pdfs()

def get_info_pdf(name_pdf):
    #abri os pdfs
    try:
        with pdfplumber.open(f'src/{name_pdf}.pdf') as pdf:
            list_arrays_infos_pdf=list()
            for page in pdf.pages:
                # Extrair tabelas da página atual do pdf
                tables = page.extract_tables()
                array_tables_yellow_cards = np.zeros((len(tables),1),dtype=object)
                for i in np.arange(0,len(tables)):   
                    array_tables_yellow_cards[i][0] = tables[i]
                for i in np.arange(0,len(array_tables_yellow_cards)):
                    # list comprehension para tirar os valores nulos das listas
                    array_tables_yellow_cards[i][0] = [data for data in array_tables_yellow_cards[i][0] if data is not None]
                list_arrays_infos_pdf.append(array_tables_yellow_cards)
    except:
        ...
    return list_arrays_infos_pdf


def get_info_cards(list_arrays_infos_pdf,name_pdf):
    for i in range(0,len(list_arrays_infos_pdf[1])):
        if 'Cartões Amarelos' in list_arrays_infos_pdf[1][i][0][0]:
            index_yellow_cards = i
        elif 'Cartões Vermelhos' in list_arrays_infos_pdf[1][i][0][0]:
            index_red_cards = i
    list_time_yellow_cards = list()
    list_which_time_yellow_cards = list()
    list_name_player_yellow_card = list()
    list_team_player_yellow_card = list()
    list_motivo_yellow_card = list()
    for i in range(index_yellow_cards,index_red_cards):
        if 'Cartões Amarelos' in list_arrays_infos_pdf[1][i][0][0]:
            list_time_yellow_cards.append(list_arrays_infos_pdf[1][i][0][2][0])
            list_which_time_yellow_cards.append(list_arrays_infos_pdf[1][i][0][2][1])
            list_name_player_yellow_card.append(list_arrays_infos_pdf[1][i][0][2][3])
            list_team_player_yellow_card.append(list_arrays_infos_pdf[1][i][0][2][4])
            list_motivo_yellow_card.append(list_arrays_infos_pdf[1][i][0][3][3])
            df['tempo_cartao_amarelo'] = [list_time_yellow_cards]
            df['1T/2T_cartao_amarelo'] = [list_which_time_yellow_cards]
            df['jogadores_cartao_amarelo'] = [list_name_player_yellow_card]
            df['time_jogadores_cartao_amarelo'] = [list_team_player_yellow_card]
            df['motivo_cartao_amarelo'] = [list_motivo_yellow_card]
        else:
            list_time_yellow_cards.append(list_arrays_infos_pdf[1][i][0][0][0])
            list_which_time_yellow_cards.append(list_arrays_infos_pdf[1][i][0][0][1])
            list_name_player_yellow_card.append(list_arrays_infos_pdf[1][i][0][0][3])
            list_team_player_yellow_card.append(list_arrays_infos_pdf[1][i][0][0][4])
            list_motivo_yellow_card.append(list_arrays_infos_pdf[1][i][0][1][3])
            df['tempo_cartao_amarelo'] = [list_time_yellow_cards]
            df['1T/2T_cartao_amarelo'] = [list_which_time_yellow_cards]
            df['jogadores_cartao_amarelo'] = [list_name_player_yellow_card]
            df['time_jogadores_cartao_amarelo'] = [list_team_player_yellow_card]
            df['motivo_cartao_amarelo'] = [list_motivo_yellow_card]
        
    list_time_red_cards = list()
    list_which_time_red_cards = list()
    list_name_player_red_card = list()
    list_team_player_red_card = list()
    list_red_card_direct_or_2_yellow_card = list()
    list_motivo_red_card = list()
    for i in range(index_red_cards,len(list_arrays_infos_pdf[1])):
            if 'NÃO HOUVE EXPULSÕES' in list_arrays_infos_pdf[1][i][0][1]:
                df['tempo_cartao_vermelho'] = None
                df['1T/2T_cartao_vermelho'] = None
                df['jogadores_cartao_vermelho'] = None
                df['time_jogadores_cartao_vermelho'] = None
                df['cartao_vermelho_direto_ou_2_cartao_amarelo'] = None
                df['motivo_cartao_vermelho'] = 'NÃO HOUVE EXPULSÕES'
            elif 'Cartões Vermelhos' in list_arrays_infos_pdf[1][i][0][0]:
                list_time_red_cards.append(list_arrays_infos_pdf[1][i][0][2][0])
                list_which_time_red_cards.append(list_arrays_infos_pdf[1][i][0][2][1])
                name_player_team_player = list_arrays_infos_pdf[1][i][0][2][3].split('-')
                list_name_player_red_card.append(name_player_team_player[0])
                list_team_player_red_card.append(name_player_team_player[1])
                list_red_card_direct_or_2_yellow_card.append(list_arrays_infos_pdf[1][i][0][3][0])
                list_motivo_red_card.append(list_arrays_infos_pdf[1][i][0][3][3])
                df['tempo_cartao_vermelho'] = [list_time_red_cards]
                df['1T/2T_cartao_vermelho'] = [list_which_time_red_cards]
                df['jogadores_cartao_vermelho'] = [list_name_player_red_card]
                df['time_jogadores_cartao_vermelho'] = [list_team_player_red_card]
                df['cartao_vermelho_direto_ou_2_cartao_amarelo'] = [list_red_card_direct_or_2_yellow_card]
                df['motivo_cartao_vermelho'] = [list_motivo_red_card]
            else:
                list_time_red_cards.append(list_arrays_infos_pdf[1][i][0][0][0])
                list_which_time_red_cards.append(list_arrays_infos_pdf[1][i][0][0][1])
                name_player_team_player = list_arrays_infos_pdf[1][i][0][0][3].split('-')
                list_name_player_red_card.append(name_player_team_player[0])
                list_team_player_red_card.append(name_player_team_player[1])
                list_red_card_direct_or_2_yellow_card.append(list_arrays_infos_pdf[1][i][0][1][0])
                list_motivo_red_card.append(list_arrays_infos_pdf[1][i][0][1][3])
                df['tempo_cartao_vermelho'] = [list_time_red_cards]
                df['1T/2T_cartao_vermelho'] = [list_which_time_red_cards]
                df['jogadores_cartao_vermelho'] = [list_name_player_red_card]
                df['time_jogadores_cartao_vermelho'] = [list_team_player_red_card]
                df['cartao_vermelho_direto_ou_2_cartao_amarelo'] = [list_red_card_direct_or_2_yellow_card]
                df['motivo_cartao_vermelho'] = [list_motivo_red_card]
    
            
        

def get_info_subs(list_arrays_infos_pdf,name_pdf):
    for i in range(0,len(list_arrays_infos_pdf[2])):
        if 'Substituições' in list_arrays_infos_pdf[2][i][0][0]:
            index_subs = i
    list_time_subs = list()
    list_which_time_subs = list()
    list_team_player_subs = list()
    list_name_players_subs_in_and_out = list()
    count=0
    try:
        for info in list_arrays_infos_pdf[2][index_subs][0][2:]:
            
            list_time_subs.append(info[0])
            list_which_time_subs.append(info[1])
            list_team_player_subs.append(info[2])
            list_name_players_subs_in_and_out.append((info[3],info[4]))
            df['tempo_substituicao'] = [list_time_subs]
            df['1T/2T_substituicao'] = [list_which_time_subs]
            df['time_jogadores_substituicao'] = [list_team_player_subs]
            df['jogadores_substituidos'] = [list_name_players_subs_in_and_out]

    except:
        print(f'Erro: {name_pdf}.pdf')
def create_cvs_files(df,name_pdf):
    df.to_csv(f'src/{name_pdf}.csv',index=False)

""" for name_pdf in list_name_pdfs:
    print(name_pdf)
    list_arrays_infos_pdf = get_info_pdf(name_pdf)
    get_info_cards(list_arrays_infos_pdf,name_pdf)
    get_info_subs(list_arrays_infos_pdf,name_pdf)
    create_cvs_files(df,name_pdf) """
name_pdf='rodada_1'
list_arrays_infos_pdf = get_info_pdf(name_pdf)
get_info_cards(list_arrays_infos_pdf,name_pdf)
get_info_subs(list_arrays_infos_pdf,name_pdf)
create_cvs_files(df,name_pdf)