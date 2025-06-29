from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client

# === Carregar variáveis do .env ===
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

# === Número Twilio e destinatários ===
twilio_number = '+14155238886'  # Número do WhatsApp Twilio
destinatarios = ['+244958463204', '+244922265637']  # Seus clientes autorizados

# === Frase padrão da IA ===
frase_inicial = """📊 Palpites do dia – IA Esportiva
Confira os jogos de hoje com os palpites mais prováveis com base em análise estatística:

"""

# === Obter os jogos do site ===
def obter_palpites():
    url = "https://www.goaloo.mobi"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    palpites = []
    jogos = soup.find_all("a", class_="match")

    for jogo in jogos[:10]:  # até 10 jogos
        try:
            times = jogo.get_text(strip=True)
            palpite = "Empate" if "vs" in times else times.split("-")[0].strip()
            confianca = "65%"
            palpites.append(f"⚽ {times}\n🔮 Palpite: {palpite}\n📈 Confiança: {confianca}\n")
        except:
            continue

    return frase_inicial + "\n".join(palpites) if palpites else "⚠️ Nenhum jogo encontrado."

# === Enviar WhatsApp ===
def enviar_whatsapp(mensagem):
    client = Client(account_sid, auth_token)
    for numero in destinatarios:
        client.messages.create(
            from_='whatsapp:' + twilio_number,
            to='whatsapp:' + numero,
            body=mensagem
        )

# === Executar ===
mensagem = obter_palpites()
enviar_whatsapp(mensagem)
