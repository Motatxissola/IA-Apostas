from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client

# === CARREGAR VARIÁVEIS DO ARQUIVO .env ===
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = '+14155238886'
destinatarios = ['+244922265637', '+244958463204']

# === FRASE INICIAL ===
frase_inicial = """📊 Palpites do dia – IA Esportiva
Confira os jogos de hoje com os palpites mais prováveis com base em análise estatística:

"""

# === FUNÇÃO PARA OBTER JOGOS ===
def obter_palpites():
    url = "https://www.goaloo.mobi"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    palpites = []
    jogos = soup.find_all("a", class_="match")
    
    for jogo in jogos[:10]:
        try:
            times = jogo.get_text(strip=True)
            palpite = "Empate" if "vs" in times else times.split("-")[0].strip()
            confiança = "65%"
            palpites.append(f"⚽ {times}\n🔮 Palpite: {palpite}\n📈 Confiança: {confiança}\n")
        except:
            continue

    return frase_inicial + "\n".join(palpites) if palpites else "⚠️ Nenhum jogo encontrado."

# === FUNÇÃO PARA ENVIAR WHATSAPP ===
def enviar_whatsapp(mensagem):
    client = Client(account_sid, auth_token)
    for numero in destinatarios:
        client.messages.create(
            from_='whatsapp:' + twilio_number,
            to='whatsapp:' + numero,
            body=mensagem
        )

# === EXECUTAR ===
mensagem = obter_palpites()
enviar_whatsapp(mensagem)
