import pyautogui
import time
import pyperclip

# Ler a primeira linha do arquivo text.txt com codificação UTF-8
with open('text.txt', 'r', encoding='utf-8') as file:
    primeira_linha = file.readline().strip()

# Copiar a primeira linha para a área de transferência
pyperclip.copy(primeira_linha)

# Aguardar alguns segundos antes de iniciar (para dar tempo de abrir o navegador)
time.sleep(5)

# Abrir o navegador e ir para Google (certifique-se de que o navegador esteja em foco)
pyautogui.hotkey('ctrl', 'l')  # Foca na barra de endereços
pyautogui.typewrite('https://www.google.com')  # Digita a URL do Google
pyautogui.press('enter')  # Pressiona Enter para abrir o Google

# Espera a página carregar
time.sleep(5)

# Foca na barra de pesquisa do Google
time.sleep(1)

# Colar a primeira linha lida do arquivo
pyautogui.hotkey('ctrl', 'v')  # Cola a linha copiada

# Opcional: Pressiona Enter para fazer a busca
pyautogui.press('enter')
