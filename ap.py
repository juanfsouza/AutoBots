from math import prod
import re
import subprocess
import sys
from turtle import window_height, window_width
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random import uniform, choice, randint
from string import ascii_letters
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from nordvpn_switcher import initialize_VPN, rotate_VPN
from selenium_stealth import stealth
from seleniumbase import BaseCase
from selenium.webdriver.common.action_chains import ActionChains
from unidecode import unidecode
from selenium.webdriver.common.proxy import Proxy, ProxyType

from asyncio import wait
import pygetwindow as gw
import pandas as pd
import pyperclip
import random
import pyautogui
from time import sleep, time


log_file = open("app_log.txt", "a")

sys.stdout = log_file
sys.stderr = log_file

def usleep(a, b):
    sleep(uniform(a, b))

if __name__ == "__main__":
    while True:  # Start an infinite loop
        chrome_opt = uc.ChromeOptions()
                        
        options = uc.ChromeOptions()
        chrome_opt.add_argument(f'user-agent={UserAgent}')
        chrome_opt.add_argument("--window-size=1920,1080")

        # Desabilitar o gerenciador de senhas
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        chrome_opt.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")      
        options.add_experimental_option("excludeSwitches", ["enable-automation"])     
        
        try:
            # Limpar o conteúdo do arquivo de log
            with open("app_log.txt", "w") as log_file:
                log_file.write("")

            sys.stdout.reconfigure(line_buffering=True)
            sys.stdout.reconfigure(encoding='utf-8')


            # Inicializar o navegador Chrome
            driver = uc.Chrome(options=chrome_opt)
            print('\nIniciando Bot\n')


            driver.get('https://sso.acesso.gov.br/login?client_id=portal-logado.estaleiro.serpro.gov.br&authorization_id=1923a111179')
            usleep(3, 3)

            pyautogui.hotkey('f10')
            pyautogui.hotkey('f10')

            # Verifica se há algum iframe
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')

            # Se houver iframes, mude para o primeiro (ou identifique qual iframe contém o elemento)
            if len(iframes) > 0:
                driver.switch_to.frame(iframes[0])  # Mudar para o iframe específico

            pyautogui.typewrite("41672878896")

            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(5, 5)

            pyautogui.typewrite("Qwaszxc123@")

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(5, 5)

            driver.get('https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/pf/Emitir/ResultadoEmissao/NDUkODk3OCMyMzQ2Nzg5IyojKjAwNjUsbyBDUEYsNDE2LjcyOC43ODgtOTYsL1NlcnZpY29zL2NlcnRpZGFvaW50ZXJuZXQvcGYvQ29uc3VsdGFy')
            usleep(5, 5)

           # Espera até que o elemento com a classe 'pular submit' esteja clicável
            input_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='NI' and contains(@class, 'pular submit')]"))
            )
            # Clica no elemento
            input_element.click()
            input_element.send_keys("41672878896")
            usleep(2, 5)

            # Espera até que o elemento "Consultar" esteja clicável
            consultar_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@id='validar' and @type='button']"))
            )

            # Clica no elemento "Consultar"
            consultar_element.click()
            usleep(5, 5)

            
            # Espera até que o link "Emissão de nova certidão" esteja disponível
            certidao_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Emissão de nova certidão"))
            )

            # Clica no link "Emissão de nova certidão"
            certidao_link.click()
            usleep(2, 5)
            pyautogui.hotkey('enter')
            usleep(99992, 5)

            log_file.close()
            driver.quit()
             
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("\nRestarting the bot...\n")
            print("\nTrocando Ip...\n")
            usleep(3, 3)
            # Desconecta do Cloudflare Warp
            #desconectar_warp()
            log_file.close()
            driver.quit()
            continue  
        finally:
            if driver:
                driver.quit()