from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def make_driver_firefox():
    #caminho do driver do firefox
    GECKOFRIVER_EXEC = 'driver/geckodriver'  
    #caminho para onde os arquivos pdf vão ao seer baixados
    DOWNLOAD_FOLDER = '/run/media/fabio/arqs_linux/Ciencia_de_dados/projetos_analise_exploratoria/flamengo_analysis/src'

    #instancia as opções
    firefox_options = Options()

    #define um perfil para o navegador
    firefox_profile = webdriver.FirefoxProfile()

    #preferencia para salvar os pdf no caminho do Download_folder
    firefox_profile.set_preference('browser.download.dir',DOWNLOAD_FOLDER)
    firefox_profile.set_preference("browser.download.folderList", 2) 
    # Define a preferência para sempre salvar arquivos PDF
    firefox_profile.set_preference('browser.download.useDownloadDir',True)
    # Define a preferência para não abrir PDFs no navegador, e sim baixá-los
    firefox_profile.set_preference("pdfjs.disabled", True)

    #coloca as preferencias nao opções do navegador 
    firefox_options.profile = firefox_profile

    #inicia o service com o driver do firefox
    firefox_service = Service(executable_path=GECKOFRIVER_EXEC)

    #cria a instancia do driver
    firefox_browser = webdriver.Firefox(
        service=firefox_service,
        options=firefox_options,
    )
    return firefox_browser

firefox_browser = make_driver_firefox()

#função que pega as informações de publico e renda
def get_info_prublico_renda(search_publico_renda):
    search_publico_renda_list = search_publico_renda.text.split('\n')
    for word in search_publico_renda_list:
        if word.startswith('Público'):
            index = search_publico_renda_list.index(word)
            with open('publico.txt','a') as arq_pulico:
                arq_pulico.write(search_publico_renda_list[index])
                arq_pulico.write('\n')
        elif word.startswith('Renda'):
            index = search_publico_renda_list.index(word)
            with open('renda.txt','a') as arq_renda:
                arq_renda.write(search_publico_renda_list[index])
                arq_renda.write('\n')

#função que baixa os pdfs
def get_pdfs(firefox_browser):
    firefox_browser.get('https://pt.wikipedia.org/wiki/Temporada_do_Clube_de_Regatas_do_Flamengo_de_2023#Primeiro_turno')
    time.sleep(0.5)
    for i in range(24,62):
        if i <=42:
            search = firefox_browser.find_element(by = By.ID,value = f'collapseButton{i}')
            search.send_keys(Keys.ENTER)
            search_publico_renda = firefox_browser.find_element(by = By.ID,value = f'collapsibleTable{i}')
            get_info_prublico_renda(search_publico_renda)
            search = firefox_browser.find_element(by = By.LINK_TEXT,value = 'CBF (Súmula)')
            search.click()
            search = firefox_browser.find_element(by = By.ID,value = f'collapseButton{i}')
            search.click()
        else:
            search2 = firefox_browser.find_element(by = By.ID,value = f'collapseButton{i}')
            search2.send_keys(Keys.ENTER)
            search_publico_renda = firefox_browser.find_element(by = By.ID,value = f'collapsibleTable{i}')
            get_info_prublico_renda(search_publico_renda)
            search2 = firefox_browser.find_element(by = By.LINK_TEXT,value = 'Súmula (CBF)')
            search2.click()
            search2 = firefox_browser.find_element(by = By.ID,value = f'collapseButton{i}')
            search2.click()
    firefox_browser.quit() 
get_pdfs(firefox_browser)