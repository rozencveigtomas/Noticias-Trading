import requests
import google.generativeai as genai
import os

# Configuración de Secretos
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def analizar_noticias():
    try:
        # 1. Buscar noticias de NVIDIA
        url = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()
        articulos = response.get('articles', [])[:3]
        
        texto_noticias = "\n".join([f"- {a['title']}" for a in articulos]) if articulos else "No hay noticias nuevas."

        # 2. IA de Gemini (Usando el modelo Pro que es el más estable)
        genai.configure(api_key=GEMINI_API_KEY)
        # Cambiamos a gemini-pro para evitar el error 404
        model = genai.GenerativeModel('gemini-pro') 
        
        prompt = f"Analiza estas noticias de NVIDIA y dime si es momento de COMPRAR, VENDER o MANTENER. Sé muy breve:\n{texto_noticias}"
        respuesta = model.generate_content(prompt)

        # 3. Enviar a Telegram
        mensaje = f"🤖 **Análisis de IA (NVIDIA)**\n\n{respuesta.text}"
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        res = requests.post(api_url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})
        
        if res.status_code == 200:
            print("¡Mensaje enviado con éxito a Telegram!")
        else:
            print(f"Error en Telegram: {res.text}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    analizar_noticias()
