from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import shutil
import os
from os import listdir
from os.path import isfile, join
import patoolib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def downloadCBR(url,pathCbr,pathImgTmp):
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # clicco sull'eventuale bottone dei cookie
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="ACCETTO"]'))).click()

    #r = SalvoEVadoAvanti(driver, pathCbr, pathImgTmp)

    while True:
        r = SalvoEVadoAvanti(driver, pathCbr, pathImgTmp)
        if not r:
            break  # ho finito le pagine



def SalvoEVadoAvanti(driver,pathCbr,pathImgTmp):
    # prendo url immagine
    Images = driver.find_elements(By.CLASS_NAME, 'img-fluid')
    for image in Images:
        if image.get_attribute("src") != 'https://www.mangaworld.in/public/assets/svg/MangaWorldLogo.svg?6':
            ImgSrc = image.get_attribute("src")

    file = re.findall("(?P<Directory>capitolo-[\d]{1,5})[^\/]+\/(?P<NomeFile>[^\/]+.[\w]{1,8})", ImgSrc)[0]

    # prendo il capitolo selezionato
    comboCap = Select(driver.find_element(By.XPATH, "//select[contains(@class, 'chapter custom-select')]"));
    cap = comboCap.first_selected_option.text.replace(".", "_");

    # prendo la pagina
    comboPage = Select(driver.find_element(By.XPATH, "//select[contains(@class, 'page custom-select')]"));
    pag = comboPage.first_selected_option.text;

    pag = re.findall("(?P<PaginaCorrente>[\d]{1,5})/(?P<PagineTotali>[\d]{1,5})", pag)[0]
    pag_attuale = pag[0]
    pag_totali = pag[1]

    # salvo immagine
    r = requests.get(ImgSrc)
    Path(pathImgTmp).mkdir(parents=True, exist_ok=True)
    with open(pathImgTmp + file[1], 'wb') as outfile:
        outfile.write(r.content)

    # verifico se sono sull'ultima pagina
    if (pag_attuale == pag_totali):
        # creo il cbr
        creaCBR(cap, pathImgTmp)
        # elimino folder
        shutil.rmtree(pathImgTmp)
        # mi assicuro che ci sia il folder dei cbr
        Path(pathCbr).mkdir(parents=True, exist_ok=True)
        # sposto il file cbr nel folder definitivo
        shutil.move(cap + ".cbr", pathCbr + cap + ".cbr")
        # avverto l'utente
        print('Cbr del capitolo '+cap+' creato')

    # clicco sul bottone
    # verifico che il bottone non sia disabilitato, se lo è mi fermo
    submitBtn = driver.find_element(By.XPATH, '//button[text()="Successivo "]')

    if (submitBtn.is_enabled()):
        submitBtn.click()
        return True
    else:
        return False


def creaCBR(nomefile, folder):
    onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    patoolib.create_archive(nomefile + ".rar", onlyfiles, verbosity=-1)
    os.rename(nomefile + ".rar", nomefile + ".cbr")
