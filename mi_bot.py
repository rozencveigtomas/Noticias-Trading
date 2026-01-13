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
        # 1. Buscar noticias
        url = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&apiKey={NEWS_API_KEY}"
        response = requests.get(url).json()
        articulos = response.get('articles', [])[:3]
        texto_noticias = "\n".join([f"- {a['title']}" for a in articulos]) if articulos else "Sin noticias."

        # 2. Configuración de la IA (Solución al error 404)
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Usamos gemini-1.5-flash que es el más actual y gratuito
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"Analiza estas noticias de NVIDIA y dime si es momento de COMPRAR, VENDER o MANTENER. Sé muy breve:\n{texto_noticias}"
        
        # Intentamos generar el contenido
        respuesta = model.generate_content(prompt)

        # 3. Enviar a Telegram
        mensaje = f"🤖 **Reporte IA NVIDIA**\n\n{respuesta.text}"
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        res = requests.post(api_url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})
        
        if res.status_code == 200:
            print("¡Mensaje enviado!")
        else:
            print(f"Error Telegram: {res.text}")

    except Exception as e:
        # Esto nos dirá exactamente qué modelo sí está disponible si vuelve a fallar
        print(f"Error: {e}")

if __name__ == "__main__":
    analizar_noticias()
