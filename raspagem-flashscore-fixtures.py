import time
import os
from tqdm import tqdm
import numpy as np
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from funcoes import *

## PARA USO COM FIREFOX ###
opcoes = FirefoxOptions()
# opcoes.add_argument("--headless")
# opcoes.add_argument("--no-sandbox")
# opcoes.add_argument("--disable-dev-shm-usage")

driver = webdriver.Firefox(options=opcoes)

### PARA USO COM O GOOGLE CHROME ####

# driver = webdriver.Chrome()


x = input("Digite o nome do país: ")
y = input("Digite o nome da liga: ")
ano_inicial = int(input("Digite o ano inicial: "))
ano_final = ano_inicial

try:
    os.makedirs(
        rf"C:\PROJETOS\FUTEBOL\FLASHSCORE\base-dados\{x}\{y}\fixtures"
    )
except:
    pass


for ano in range(ano_inicial, ano_final + 1):
    # driver.maximize_window()

    # url = f"https://www.flashscore.com.br/futebol/{x}/{y}-{ano}/resultados/"

    driver.get(f"https://www.flashscore.com/football/{x}/{y}/fixtures/")
    # driver.get(f"https://www.flashscore.com/football/{x}/{y}-{ano}-{ano+1}/results/")
    # driver.get(url)

    time.sleep(3)

    FecharBanner(driver)
    ClicarPagina(driver)

    with open(
        rf"C:\PROJETOS\FUTEBOL\FLASHSCORE\base-dados\{x}\{y}\fixtures\{y}-{ano}-fixtures.csv",
        "a",
    ) as f:
        f.writelines(
            "id_jogo;nacao;campeonato;ano;dia;home;away;endereco\n"
        )

        id_jogos = CapturaIdJogoFixtures(driver)
        # id_jogos = id_jogos[-71:]

        # print(id_jogos)

        for j in tqdm(id_jogos):
            endereco = f"https://www.flashscore.com/match/{j}/#/"
            # endereco = f"https://www.flashscore.com.br/jogo/{j}/#/"

            driver.get(f"{endereco}match-summary")
            # driver.get(f"{endereco}resumo-de-jogo")

            # time.sleep(3.5)
            # Espera até que a página esteja completamente carregada
            try:
                wait = WebDriverWait(driver, 60)  # tempo máximo de espera de 10 segundos
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

            except TimeoutException:
                print(f"A página não carregou completamente para o jogo {j}")

            id_jogo = j

            print(f"\njogo_id: {j}")

            # obter o nome do campeonato e a rodada
            LigaRodada(driver)

            # obter data do jogo e nomes das equipes envolvidas
            InfoParticipantes(driver)

            time.sleep(3)

            f.writelines(
                f"{id_jogo};{LigaRodada(driver)[0]};{LigaRodada(driver)[1]};{ano};{InfoParticipantes(driver)[0]};{InfoParticipantes(driver)[1]};{InfoParticipantes(driver)[2]};{endereco}\n"
            )

            print(
                f"{LigaRodada(driver)[0]}|{LigaRodada(driver)[1]}|{ano}|{InfoParticipantes(driver)[0]}|{InfoParticipantes(driver)[1]}|{InfoParticipantes(driver)[2]}"
            )

    print(f"Arquivo salvo.")

    time.sleep(3)

driver.close()
