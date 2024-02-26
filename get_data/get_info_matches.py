from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def make_driver_firefox():
    #caminho do driver do firefox
    GECKOFRIVER_EXEC = 'driver/geckodriver'  

    #instancia as opções
    firefox_options = Options()

    #define um perfil para o navegador
    firefox_profile = webdriver.FirefoxProfile()

    #inicia o service com o driver do firefox
    firefox_service = Service(executable_path=GECKOFRIVER_EXEC)

    #cria a instancia do driver
    firefox_browser = webdriver.Firefox(
        service=firefox_service,
        options=firefox_options,
    )
    return firefox_browser

firefox_browser = make_driver_firefox()

#função que grava as informações em arquivos txt
def write_infos(get,name_file):
    get = ','.join(get)
    with open(f'src/{name_file}.txt','a') as arq:
        arq.write(get)
        arq.write('\n')

# função que pega os links das partidas
def get_links_matches(firefox_browser):
    firefox_browser.get('https://fbref.com/pt/equipes/639950ae/2023/partidas/c24/schedule/Flamengo-Resultados-e-Calendarios-Serie-A')
    time.sleep(5)
    for i in range(1,42):
        try:
            links = firefox_browser.find_element(By.XPATH,f'/html/body/div[2]/div[6]/div[4]/div[2]/table/tbody/tr[{i}]/td[16]/a')
            with open('src/links_partidas.txt','a') as arq_links_partidas:
                arq_links_partidas.write(links.get_attribute("href"))
                arq_links_partidas.write('\n')
        except:
            ...
    firefox_browser.quit()
#get_links_matches(firefox_browser)

def read_arqs():
    list_links = list()
    with open('src/links_partidas.txt','r') as arq_links_matches:
        list_links.append(arq_links_matches.readlines())
    return list_links

list_links = read_arqs()

def get_info_matches(firefox_browser,list_links):
   for link in list_links[0]:
        try:
            firefox_browser.get(link)
            get_escalacao = firefox_browser.find_elements(by = By.ID,value = 'a')
            write_infos(get_escalacao[1].text.split('\n'),'escalacao')

            get_stats_match = firefox_browser.find_element(by = By.ID,value = 'team_stats')
            write_infos(get_stats_match.text.split('\n'),'estatisticas_partidas')

            get_stats_extra_match = firefox_browser.find_element(by = By.ID,value = 'team_stats_extra')
            write_infos(get_stats_extra_match.text.split('\n'),'estatisticas_extras_partidas')
        except:
            ...
        firefox_browser.quit()

get_info_matches(firefox_browser,list_links)
    
