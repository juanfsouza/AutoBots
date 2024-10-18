import logging
import re
import threading
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import nodriver as uc

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Função para iniciar o bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Estou gravando as mensagens do grupo.')

# Função para salvar mensagens em um arquivo
def save_message(message: str):
    with open('messages.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')

# Função para extrair valores e abrir o link
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    save_message(message_text)

    # Extraindo o link no formato 🏆 EXPRESS (https://www.bet365.com/#/AVR/B146/R%5E1/) 🏆
    link_match = re.search(r'🏆 EXPRESS \((.*?)\) 🏆', message_text)
    if link_match:
        link = link_match.group(1)
        logging.info(f'Abrindo o link: {link}')
        # Passa o link e o texto da mensagem para a função em uma thread
        threading.Thread(target=lambda: asyncio.run(open_link(link, message_text))).start()

async def open_link(link, message_text):
    driver = None
    try:
        # Iniciando o driver com opções customizadas
        options = uc.ChromeOptions()
        options.add_argument("--incognito")  # Ativa o modo anônimo/incógnito
        options.add_argument("--disable-save-password-bubble")  # Desativa a bolha de salvar senhas
        options.add_argument("--disable-autofill")  # Desativa o preenchimento automático de formulários
        options.add_argument("--disable-password-manager-reauthentication")  # Desativa a reautenticação do gerenciador de senhas

        # Inicia o driver usando as opções configuradas
        driver = await uc.start(options=options)
        
        # Abre a URL extraída
        tab = await driver.get(link)
        logging.info("Página carregada com sucesso.")
        await tab.sleep(5)

        # Espera pelo botão de login e clica
        login_button = await tab.find("Login", best_match=True, timeout=30)
        if login_button:
            await login_button.click()
            logging.info("Botão de login clicado.")
        await tab.sleep(2)

        # Localizando o input de email (usuário) com base no placeholder e classe
        email_field = await tab.select('input[placeholder="Usuário"].lms-StandardLogin_Username')
        password_field = await tab.select("input[type=password]")

        if email_field and password_field:
            await email_field.send_keys("juanfsouzaz")
            await password_field.send_keys("Polkmn123@")
            logging.info("Credenciais inseridas.")

            login_submit_button = await tab.select('div.lms-LoginButton')
            if login_submit_button:
                await login_submit_button.click()
                logging.info("Botão de login clicado com sucesso.")
        
        await tab.sleep(10)

        # Extraindo os minutos do texto da mensagem
        time_match = re.search(r'⏰\s*H:\s*(\d+)\s*➡️\s*(\d+)', message_text)
        if time_match:
            # Extrai as horas e os minutos do match
            selected_hour = time_match.group(1)
            selected_minute = time_match.group(2)
            logging.info(f"Selecionando o horário: {selected_hour}:{selected_minute}")

            # Clicar no elemento correspondente à hora e minuto
            time_element_selector = f'div[data-content="{selected_hour}:{selected_minute}"]'
            time_element = await tab.select(time_element_selector)
            
            if time_element:
                await time_element.click()
                logging.info(f"Clicou no elemento com o horário: {selected_hour}:{selected_minute}.")
                await tab.sleep(9990)
            else:
                logging.info(f"Elemento para o horário {selected_hour}:{selected_minute} não encontrado.")
        else:
            logging.info("Nenhum horário encontrado no texto.")
    finally:
        if driver is not None:
            await driver.stop()  # Garante que o driver seja encerrado corretamente


# Função principal
def main():
    application = ApplicationBuilder().token("6953201006:AAHLLa8j1hT0jI7_4rVpH2E8nh2cWMhWJJI").build()

    # Comandos
    application.add_handler(CommandHandler("start", start))

    # Manipulador de mensagens
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciando o bot
    application.run_polling()

if __name__ == '__main__':
    main()