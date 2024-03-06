from pathlib import Path
#função que renomeia os pdfs
def rename_pdfs(range_min,range_max):
    #diretório que contem os arquivos pdf
    directory = Path('src')
    #ordena os pdf por ordem de modificação
    files = sorted(directory.glob('*'), key=lambda file: file.stat().st_mtime)
    numbers = range(range_min,range_max)
    count=0
    for file in files:
        #renomeia o pdf de acordo com a rodada
        new_name = directory / f'rodada_{numbers[count]}.pdf'
        file.rename(new_name)
        count+=1
rename_pdfs(1,39)



