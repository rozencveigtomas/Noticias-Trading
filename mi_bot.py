import requests
import os

# 1. Configuración de Llaves
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def consultar_gemini_directo(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        return "Error en la IA."
    except:
        return "Error de conexión con la IA."

def correr_bot():
    # 2. Buscar Noticias de NVIDIA
    url_news = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    resp_news = requests.get(url_news).json()
    articulos = resp_news.get('articles', [])[:3]
    texto = "\n".join([f"- {a['title']}" for a in articulos]) if articulos else "Sin noticias hoy."

    # 3. Análisis con IA
    prompt = f"Analiza brevemente estas noticias de NVIDIA y recomienda COMPRAR, VENDER o MANTENER:\n{texto}"
    analisis = consultar_gemini_directo(prompt)

    # 4. Enviar a Telegram
    mensaje_final = f"🤖 **Análisis de Inversión (NVIDIA)**\n\n{analisis}"
    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url_telegram, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje_final, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    correr_bot()
