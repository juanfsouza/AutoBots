import os
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
            # Aumentar o tempo de espera
            x = 233
            y = 989 

            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()
            print("Clicado no elemento Aurum Roulette A.")
            
        else:
            x = 1326
            y = 984

            pyautogui.moveTo(x, y, duration=1)
            pyautogui.click()
            print("Clicado no elemento Brasileira.")
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

# Função para selecionar um arquivo aleatório da pasta 'texto'
def get_random_text_file(directory):
    # Lista todos os arquivos da pasta
    arquivos = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    if not arquivos:
        print("Nenhum arquivo de texto encontrado na pasta.")
        return None
    
    # Seleciona um arquivo de forma aleatória
    arquivo_aleatorio = random.choice(arquivos)
    
    # Retorna o caminho completo do arquivo selecionado
    return os.path.join(directory, arquivo_aleatorio)

# Função para enviar mensagens a partir de um arquivo de texto aleatório
def send_messages_from_file(driver, message_interval):
    # Define o diretório onde os arquivos de texto estão
    diretorio_textos = 'texto'
    
    # Obtém um arquivo de texto aleatório da pasta
    arquivo_texto = get_random_text_file(diretorio_textos)
    
    if not arquivo_texto:
        print("Não foi possível selecionar um arquivo de texto.")
        return

    print(f"Arquivo selecionado: {arquivo_texto}")

    # Lê todas as linhas do arquivo selecionado
    with open(arquivo_texto, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    # Remove espaços em branco das linhas
    
    linhas = [linha.strip() for linha in linhas if linha.strip()]  # Ignora linhas vazias
    
    num_mensagens = len(linhas)
    for i in range(20):  # Envia 100 mensagens
        try:
            mensagem = linhas[i % num_mensagens]  # Usa o operador % para repetir mensagens

            # Verifica se há algum iframe
            if iframes := driver.find_elements(By.TAG_NAME, 'iframe'):
                driver.switch_to.frame(iframes[0])  # Muda para o primeiro iframe

            # Copia a mensagem para a área de transferência
            pyperclip.copy(mensagem)
            time.sleep(1)  # Tempo de espera para garantir que a mensagem é copiada

            # Localiza o campo de entrada da mensagem
            element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Digite a mensagem aquí']")
            element.click()  # Clica no campo para ativá-lo

            # Cola a mensagem copiada e envia
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')
            time.sleep(2)  # Aguardando um pequeno tempo para o envio da mensagem

            time.sleep(message_interval)  # Intervalo entre mensagens

            driver.switch_to.default_content()  # Volta para o conteúdo principal

        except NoSuchElementException as e:
            print(f"Erro ao encontrar o campo de entrada: {e}")
            break
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

def start_bot(driver):
    try:
        sys.stdout.reconfigure(line_buffering=True)
        sys.stdout.reconfigure(encoding='utf-8')

        # Captura o valor do intervalo das mensagens a partir dos argumentos da linha de comando
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

        # Localiza e clica no botão de registro
        botao_registro = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button-register')]"))
        )
        botao_registro.click()

        # Gerando valores aleatórios
        random_name = generate_random_name()
        random_email = generate_random_email()
        random_password = generate_random_password()

        # Preenche os campos de nome, e-mail e senha
        campo_nome = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='name']"))
        )
        campo_nome.click()
        campo_nome.clear()
        campo_nome.send_keys(random_name)
        print(f"Nome inserido: {random_name}")
        time.sleep(2)

        # Preenche e-mail e senha usando pyautogui
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

        # Aceita os termos e finaliza o registro
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
        driver.get("https://vipercassino.online/games/play/14379/19798")
        time.sleep(5)

        pyautogui.hotkey('f10')

        for _ in range(7):
            pyautogui.hotkey('tab')
            time.sleep(0.1)  # Atraso opcional entre as pressões de tecla

        pyautogui.hotkey('enter')
        pyautogui.hotkey('f5')
        time.sleep(5)
        pyautogui.hotkey('f10')
        pyautogui.hotkey('f10') 

        escolha(driver)
        time.sleep(6)

        # Envia mensagens 100 vezes, com intervalo de 5 segundos
        send_messages_from_file(driver, message_interval=message_interval)

        time.sleep(2)

    except Exception as e:
        print(f"Erro: {e}")
        driver.quit()  # Fecha o navegador
        return False  # Retorna False para indicar falha

    return True  # Retorna True para indicar sucesso


# Loop para rodar o bot indefinidamente
while True:
    try:
        # Cria uma nova instância do driver
        driver = uc.Chrome()

        # Tenta rodar o bot, se falhar o navegador é fechado e reiniciado
        if not start_bot(driver):
            print("Reiniciando navegador e tentando novamente...")
            time.sleep(2)  # Tempo de espera antes de reiniciar

        driver.quit()  # Fecha o navegador ao final da execução

    except Exception as e:
        print(f"Erro crítico no loop principal: {e}")
        driver.quit()  # Garante que o navegador seja fechado em caso de erro crítico
        time.sleep(2)  # Espera um pouco antes de reiniciar o loop
