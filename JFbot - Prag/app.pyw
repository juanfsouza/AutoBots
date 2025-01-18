import subprocess
import sys
from bs4 import BeautifulSoup
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import undetected_chromedriver as uc
import random
import string
import time
import pyperclip

# Define um arquivo de log para capturar a saída
log_file = open("app_log.txt", "a")

# Redireciona stdout e stderr para o arquivo de log
sys.stdout = log_file
sys.stderr = log_file

# Função para ler URLs do arquivo token.txt
def read_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens]

def escolha(driver):
    jogo_escolhido = "Brasileira"  # Valor padrão

    if len(sys.argv) > 2:
        jogo_escolhido = sys.argv[2]

    try:
        if jogo_escolhido == "Aurum":
            x = 1739
            y = 266
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()
        else:
            x = 724
            y = 855
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()

    except TimeoutException:
        print("Timeout: O elemento não foi encontrado.")
    except NoSuchElementException as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Função para gerar um e-mail aleatório
def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gmail.com"

# Função para gerar um nome aleatório
def generate_random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8)).capitalize()

# Função para gerar uma senha aleatória
def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def send_messages_from_file(driver, message_interval):
    with open('text.txt', 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    linhas = [linha.strip() for linha in linhas if linha.strip()]  # Ignora linhas vazias

    num_mensagens = len(linhas)
    for i in range(25):  # Envia 25 mensagens
        try:
            mensagem = linhas[i % num_mensagens]  # Usa o operador % para repetir mensagens

            if iframes := driver.find_elements(By.TAG_NAME, 'iframe'):
                driver.switch_to.frame(iframes[0])  # Muda para o primeiro iframe

            pyperclip.copy(mensagem)
            time.sleep(1)

            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')
            time.sleep(2)

            time.sleep(message_interval)
            driver.switch_to.default_content()

        except NoSuchElementException as e:
            print(f"Erro ao encontrar o campo de entrada: {e}")
            break
        except TimeoutException as e:
            print(f"Timeout ao encontrar o campo de entrada: {e}")
            break
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

def start_bot(driver):
    try:
        sys.stdout.reconfigure(line_buffering=True)
        sys.stdout.reconfigure(encoding='utf-8')

        message_interval = 5  # Valor padrão
        if len(sys.argv) > 1:
            try:
                message_interval = int(sys.argv[1])
            except ValueError:
                print("O valor do intervalo deve ser um número inteiro.")
                return

        driver.get('https://vipercassino.online/')
        time.sleep(2)

        print("\nCriando Conta!\n")

        botao_registro = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button-register')]"))
        )
        botao_registro.click()

        random_name = generate_random_name()
        random_email = generate_random_email()
        random_password = generate_random_password()

        campo_nome = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='name']"))
        )
        campo_nome.click()
        campo_nome.clear()
        campo_nome.send_keys(random_name)
        print(f"Nome inserido: {random_name}")
        time.sleep(2)

        pyautogui.hotkey('f10')
        pyautogui.hotkey('f10')
        pyautogui.hotkey('tab')
        pyautogui.write(random_email)
        print(f"Email inserido: {random_email}")
        time.sleep(2)
        pyautogui.hotkey('tab')
        pyautogui.write(random_password)
        print(f"Senha inserida: {random_password}")
        time.sleep(2)

        campo_terms = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='term_a']"))
        )
        campo_terms.click()
        print("\nTermos aceitos!\n")
        botao_registro_final = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrar')]"))
        )
        
        botao_registro_final.click()
        print("\nRegistro com Sucesso!\n")

        time.sleep(2)
        driver.get("https://vipercassino.online")
        time.sleep(5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        elemento = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/games/play/15208/23664']"))
        )
        elemento.click()

        time.sleep(10)

        pyautogui.hotkey('f11')
        time.sleep(5)

        x = 126
        y = 128

        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(10)

        x = 86
        y = 333

        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(5)

        escolha(driver)
        time.sleep(10)

        x = 716
        y = 788
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(5)

        x = 717
        y = 788
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(5)

        x = 718
        y = 788
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(5)

        x = 718
        y = 788
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(5)

        x = 719
        y = 788
        pyautogui.moveTo(x, y, duration=1)
        pyautogui.click()

        time.sleep(2)

        pyautogui.hotkey('tab')
        pyautogui.hotkey('tab')

        send_messages_from_file(driver, message_interval=message_interval)

        time.sleep(2)

    except Exception as e:
        print(f"Erro: {e}")
        driver.quit()
        return False

    return True

while True:
    try:
        driver = uc.Chrome()

        if not start_bot(driver):
            print("Reiniciando navegador e tentando novamente...")
            time.sleep(2)

        driver.quit()

    except Exception as e:
        print(f"Erro crítico no loop principal: {e}")
        driver.quit()
        time.sleep(2)
