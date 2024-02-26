import fitz
import numpy as np

# doc armazena o pdf
doc = fitz.open('src/1421se.pdf')
# pega a primeira pagina
page1 = doc.load_page(0)
#procura as tabelas na pagina
table = page1.find_tables()

# lista com as informações das tabelas
list_tables = table.tables[0].extract()
# arrray para armazenar as info das tabelas
array_tables = np.zeros((len(list_tables),1),dtype=object)
# loop para armazenas as infos no array
for i in np.arange(0,len(list_tables)):
    array_tables[i][0] = list_tables[i]

for i in np.arange(0,len(array_tables)):
    # list comprehension para tirar os valores nulos das listas
    array_tables[i][0] = [data for data in array_tables[i][0] if data is not None]

print(array_tables[20])

#criar arquivos csv atraves do pandas para armazenar as informações 
#cada linha do array é uma linha da tabela no pdf
#fazer automação com o selenium para baixar os pdfs
