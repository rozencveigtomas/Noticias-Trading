import requests
import google.generativeai as genai
import os

# Secretos de GitHub
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def analizar_noticias():
    try:
        # 1. Obtener noticias
        url = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()
        articulos = response.get('articles', [])[:3]
        texto_noticias = "\n".join([f"- {a['title']}" for a in articulos]) if articulos else "Sin noticias hoy."

        # 2. Configuración de IA con la nueva ruta de modelos
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Esta es la ruta completa que evita el error 404 en la v1beta
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = f"Analiza estas noticias de NVIDIA y dime si es momento de COMPRAR, VENDER o MANTENER. Sé breve:\n{texto_noticias}"
        respuesta = model.generate_content(prompt)

        # 3. Envío a Telegram
        mensaje = f"🤖 **Análisis IA**\n\n{respuesta.text}"
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(api_url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})
        print("¡Proceso terminado con éxito!")

    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    analizar_noticias()
