import requests
import google.generativeai as genai
import os

# GitHub leerá esto de los "Secrets" que configuraremos ahora
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def analizar_noticias():
    try:
        # 1. Buscar noticias (Ejemplo con NVIDIA)
        url = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()
        articulos = response.get('articles', [])[:3]
        
        if not articulos:
            texto_noticias = "No se encontraron noticias hoy."
        else:
            texto_noticias = "\n".join([f"- {a['title']}" for a in articulos])

        # 2. IA de Gemini analiza
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        prompt = f"Analiza estas noticias de NVIDIA y dime si es momento de COMPRAR, VENDER o MANTENER. Sé muy breve y directo:\n{texto_noticias}"
        respuesta = model.generate_content(prompt)

        # 3. Enviar a Telegram
        mensaje = f"🤖 **Reporte de IA para NVIDIA**\n\n{respuesta.text}"
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(api_url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})
        print("Mensaje enviado con éxito.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analizar_noticias()
