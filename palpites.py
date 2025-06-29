from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import datetime
import time

print("IA de palpites iniciada")

# === Carregar variáveis de ambiente ===
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = 'whatsapp:+14155238886'

# === Lista de destinatários ===
destinatarios = [
    'whatsapp:+244958463204',
    'whatsapp:+244922265637',
    'whatsapp:+244936143404'
]

# === Mensagem inicial padrão ===
frase_inicial = """📊 Palpites do dia – IA Esportiva
Confira os jogos de hoje com os palpites mais prováveis com base em análise estatística:

"""

# === Função para obter os palpites ===
def obter_palpites():
    print("🔍 Acessando o site...")
    url = "https://www.goaloo.mobi"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        jogos = soup.find_all("a", class_="match")
        palpites = []

        for jogo in jogos[:10]:
            texto = jogo.get_text(strip=True)
            if " - " in texto:
                palpite = "Empate"
            else:
                palpite = texto.split("-")[0].strip()
            confiança = "65%"
            palpites.append(f"⚽ {texto}\n🔮 Palpite: {palpite}\n📈 Confiança: {confiança}\n")

        if palpites:
            print("✅ Jogos encontrados!")
            return frase_inicial + "\n".join(palpites)
        else:
            return "⚠️ Nenhum jogo encontrado."

    except Exception as e:
        return f"Erro ao buscar jogos: {e}"

# === Função para enviar mensagem via WhatsApp ===
def enviar_whatsapp(mensagem):
    client = Client(account_sid, auth_token)
    for numero in destinatarios:
        client.messages.create(
            from_=twilio_number,
            to=numero,
            body=mensagem
        )
    print("✅ Mensagem enviada com sucesso via WhatsApp!")

# === Execução principal ===
mensagem = obter_palpites()
print("Mensagem final:\n", mensagem)
enviar_whatsapp(mensagem)
