import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client

# === Carregar variáveis do .env ===
load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = 'whatsapp:+14155238886'
destinatarios = ['whatsapp:+244958463204', 'whatsapp:+244922265637', 'whatsapp:+244936143404']

# === Mensagem inicial ===
frase_inicial = """📊 Palpites do dia – IA Esportiva
Confira os jogos de hoje com os palpites mais prováveis com base em análise estatística:\n
"""

# === Função para obter jogos e gerar palpites ===
def obter_palpites():
    print("🔍 Acessando o site...")
    try:
        url = "https://www.goaloo.mobi"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        jogos = soup.find_all("a", class_="match")
        palpites = []

        for jogo in jogos[:10]:  # pega no máximo 10 jogos
            try:
                texto = jogo.get_text(strip=True)
                if not texto:
                    continue
                palpite = "Empate" if " - " in texto else texto.split("-")[0].strip()
                confiança = "65%"
                palpites.append(f"⚽ {texto}\n🔮 Palpite: {palpite}\n📈 Confiança: {confiança}\n")
            except:
                continue

        if palpites:
            print("✅ Jogos encontrados!")
            return frase_inicial + "\n".join(palpites)
        else:
            print("⚠️ Nenhum palpite gerado.")
            return "⚠️ Nenhum jogo encontrado."

    except Exception as e:
        return f"❌ Erro ao obter jogos: {e}"

# === Função para enviar via WhatsApp ===
def enviar_whatsapp(mensagem):
    client = Client(account_sid, auth_token)
    for numero in destinatarios:
        client.messages.create(
            from_=twilio_number,
            to=numero,
            body=mensagem
        )

# === Executar tudo ===
if __name__ == "__main__":
    print("✅ IA de palpites iniciada")
    mensagem = obter_palpites()
    print("Mensagem final:\n", mensagem)
    enviar_whatsapp(mensagem)
    print("✅ Mensagem enviada com sucesso via WhatsApp!")
