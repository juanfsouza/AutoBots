import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from random import uniform

def usleep(a, b):
    sleep(uniform(a, b))

def save_text_to_file(text, filename="output.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Conteúdo salvo em {filename}")

if __name__ == "__main__":
    while True:  # Loop infinito
        chrome_opt = uc.ChromeOptions()
        chrome_opt.add_argument("--window-size=1920,1080")
        chrome_opt.add_argument("--disable-blink-features=AutomationControlled")

        try:
            # Limpa o conteúdo do arquivo de log (opcional)
            with open("app_log.txt", "w") as log_file:
                log_file.write("")

            # Inicializar o navegador Chrome
            driver = uc.Chrome(options=chrome_opt)
            print('\nIniciando Bot\n')

            driver.get('https://web.telegram.org/k/')
            usleep(40, 40)

            # Acessar o grupo específico no Telegram
            driver.get('https://web.telegram.org/k/#-2259930645')
            usleep(5, 5)

            # Procurar o elemento pelo seletor de classe
            bubbles_element = driver.find_element(By.CLASS_NAME, "bubbles-group")
            if bubbles_element:
                # Capturar o conteúdo HTML do elemento
                content = bubbles_element.get_attribute('outerHTML')

                # Salvar o conteúdo no arquivo .txt
                save_text_to_file(content, "bubbles_content.txt")

            driver.quit()

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("\nRestarting the bot...\n")
            driver.quit()
            continue  # Recomeça o loop caso ocorra algum erro
        finally:
            if driver:
                driver.quit()
