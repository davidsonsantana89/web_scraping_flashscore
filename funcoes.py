import selenium.webdriver as webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import numpy as np
from tqdm import tqdm


def ConfigTempoGol(lista):
    lista_nova = []

    for n in lista:
        if "+" in n:
            lista_nova.append(int(n.split("+")[0]))
        else:
            lista_nova.append(int(n[:-1]))

    return lista_nova


def TempoGolMandante(driver):  # capturar os tempos dos gols para mandante
    lista_tempos_gols_home = []

    elem_gol_home = driver.find_elements(By.CLASS_NAME, "smv__homeParticipant")

    for elem_h in elem_gol_home:
        elem_texto = elem_h.find_elements(By.CLASS_NAME, "smv__incidentHomeScore")

        if len(elem_texto) > 0:
            lista_tempos_gols_home.append(elem_h.text.splitlines()[0])

    lista_tempos_gols_home = ConfigTempoGol(lista_tempos_gols_home)

    return lista_tempos_gols_home


def TempoGolVisitante(driver):  # capturar os tempos dos gols para visitante
    lista_tempos_gols_away = []

    elem_gol_away = driver.find_elements(By.CLASS_NAME, "smv__awayParticipant")

    for elem_a in elem_gol_away:
        elem_texto = elem_a.find_elements(By.CLASS_NAME, "smv__incidentAwayScore")

        if len(elem_texto) > 0:
            lista_tempos_gols_away.append(elem_a.text.splitlines()[0])

    lista_tempos_gols_away = ConfigTempoGol(lista_tempos_gols_away)

    return lista_tempos_gols_away


def FecharBanner(driver):
    try:
        driver.execute_script(
            "document.getElementById('onetrust-banner-sdk').style.display= 'none';"
        )

        time.sleep(2)

        driver.execute_script(
            "document.getElementsByClassName('otPlaceholder')[0].style.display= 'none';"
        )

        # time.sleep(5)
        time.sleep(1.5)

    except:
        pass


def ClicarPagina(driver):
    for n in range(10):
        lista = driver.find_elements(
            By.CSS_SELECTOR, "a.event__more.event__more--static"
        )
        if len(lista) != 0:
            lista[0].click()
        else:
            pass
        time.sleep(1.5)


def CapturaIdJogo(driver):
    # Pegando o ID dos Jogos
    id_jogos = []
    partidas = driver.find_elements(By.CSS_SELECTOR, "div.event__match")

    # Exemplo de ID de um jogo: 'g_1_Gb7buXVt'
    for i in tqdm(partidas):
        id_jogos.append(i.get_attribute("id")[4:])

    id_jogos.reverse()

    return id_jogos


def LigaRodada(driver):
    try:
        nacao = driver.find_element(By.CSS_SELECTOR, "span.tournamentHeader__country")
        nacao = nacao.text.split(":")[0]
        campeonato_info = driver.find_element(
            By.CSS_SELECTOR, "span.tournamentHeader__country"
        )
        campeonato_info = campeonato_info.find_element(By.CSS_SELECTOR, "a").text.split(
            "-"
        )
        campeonato = campeonato_info[0].strip()
        if len(campeonato_info) == 3:
            rodada = campeonato_info[2].strip()
        else:
            rodada = campeonato_info[1].strip()

    except:
        pass

    return (nacao, campeonato, rodada)


# obter data do jogo e nomes das equipes envolvidas
def InfoParticipantes(driver):
    elem = driver.find_elements(By.CLASS_NAME, "duelParticipant")

    dia = (
        elem[0]
        .find_element(By.CLASS_NAME, "duelParticipant__startTime")
        .text.split()[0]
    )

    home = (
        elem[0]
        .find_elements(
            By.CLASS_NAME, "participant__participantName.participant__overflow"
        )[0]
        .text
    )

    away = (
        elem[0]
        .find_elements(
            By.CLASS_NAME, "participant__participantName.participant__overflow"
        )[-1]
        .text
    )

    return (dia, home, away)


def GolsPartida(driver):
    # obter placares do 1º e 2º tempos
    placares = driver.find_elements(
        By.CSS_SELECTOR, "div.smv__incidentsHeader.section__title"
    )

    if len(placares) == 0:
        HGFT = '*'
        AGFT = "*"
        HGHT = "*"
        AGHT = "*"
    elif len(placares) == 1:
        HGFT = int(placares[0].text.split("-")[0].strip())
        AGFT = int(placares[0].text.split("-")[1].strip())
        HGHT = 0
        AGHT = 0
    else:
        HGHT = int(placares[0].text.splitlines()[1].split("-")[0])
        AGHT = int(placares[0].text.splitlines()[1].split("-")[1])
        HGFT = int(placares[1].text.splitlines()[1].split("-")[0]) + HGHT
        AGFT = int(placares[1].text.splitlines()[1].split("-")[1]) + AGHT

    return (HGHT, AGHT, HGFT, AGFT)


def MatchOdds(driver):
    tabela_odds = driver.find_elements(By.CSS_SELECTOR, "div.ui-table__row")

    lista_odds = [item.text.split("\n") for item in tabela_odds]

    if len(lista_odds) != 0:
        # odd_home = round(np.mean([float(i[0]) for i in lista_odds]), 2)
        # odd_draw = round(np.mean([float(i[1]) for i in lista_odds]), 2)
        # odd_away = round(np.mean([float(i[2]) for i in lista_odds]), 2)

        odd_home = float(lista_odds[0][0])
        odd_draw = float(lista_odds[0][1])
        odd_away = float(lista_odds[0][2])

    else:
        odd_home = 0
        odd_draw = 0
        odd_away = 0

    return (odd_home, odd_draw, odd_away)


def OddsOver(driver):
    tabela_ou = driver.find_elements(By.CSS_SELECTOR, "div.ui-table__row")

    lista_odds = np.array([item.text.split("\n") for item in tabela_ou])

    lista_over25 = [i for i in lista_odds if i[0] == "2.5"]

    if len(lista_odds) != 0:
        # over25 = round(np.mean([float(i[1]) for i in lista_odds if i[0] == "2.5"]), 2)
        over25 = float(lista_over25[0][1])
    else:
        over25 = 0

    return over25

def OddsBTTS(driver):
    tabela_btts = driver.find_elements(By.CSS_SELECTOR, "div.ui-table__row")

    lista_odds = np.array([item.text.split("\n") for item in tabela_btts])

    if len(lista_odds) != 0:
        # btts = round(np.mean([float(i[1]) for i in lista_odds]), 2)
        btts = float(lista_odds[0][0])
    else:
        btts = 0

    return btts
