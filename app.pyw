import os
import sys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import undetected_chromedriver as uc
import random
import string
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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
            # Aguarda até que o iframe esteja presente
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.game-full"))
            )
            
            # Alterna para o iframe
            driver.switch_to.frame(iframe)
            print("Mudou para o iframe com sucesso!")

            # Aguarda o elemento dentro do iframe e clica
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(7)"))
            )
            elemento.click()
            print("Elemento clicado com sucesso dentro do iframe!")
            print("Clicado no elemento Aurum Roulette A.")
            
        else:
            # Aguarda até que o iframe esteja presente
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.game-full"))
            )
            
            # Alterna para o iframe
            driver.switch_to.frame(iframe)
            print("Mudou para o iframe com sucesso!")

            # Aguarda o elemento dentro do iframe e clica
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(14) > div:nth-child(1) > a:nth-child(3)"))
            )
            elemento.click()
            print("Elemento clicado com sucesso dentro do iframe!")
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
    for i in range(20):  # Envia 20 mensagens
        try:
            mensagem = linhas[i % num_mensagens]  # Seleciona a mensagem, permitindo repetir
            print(f"Enviando mensagem: {mensagem}")

            # Localiza o campo de entrada
            element = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Digite a mensagem aquí']")
            element.click()

            # Define o texto no campo de entrada usando JavaScript
            script = f"arguments[0].value = `{mensagem}`; arguments[0].dispatchEvent(new Event('input'));"
            driver.execute_script(script, element)

            # Localiza o botão usando o seletor CSS
            button_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='chat-actions-inner'] button[class='button button-default'] svg"))
            )

            # Garante que o elemento esteja visível e clica nele
            ActionChains(driver).move_to_element(button_element).click().perform()
            print("Botão clicado com sucesso!")

            # Espera antes de enviar a próxima mensagem
            time.sleep(message_interval)

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

        # Espera até o campo de e-mail estar visível e clicável
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']"))
        )
        # Clica no campo de e-mail
        email_input.click()
        email_input.clear()
        email_input.send_keys(random_email)
        print(f"Email inserida: {random_email}")

        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='relative mb-3']//input[@placeholder='Digite a senha']"))
        )
        # Clica no campo de senha
        password_input.click()
        password_input.clear()
        password_input.send_keys(random_password)
        print(f"Senha inserida: {random_password}")

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
        time.sleep(10)

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
