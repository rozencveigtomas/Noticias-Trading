import requests
import os

# 1. Configuración de Llaves
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def consultar_gemini_directo(prompt):
    """Conecta directamente a la API de Google sin usar librerías externas."""
    # Usamos el modelo gemini-1.5-flash que es rápido y gratuito
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error en Google: {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

def correr_bot():
    print("--- Iniciando Bot (Modo Directo) ---")
    
    # 2. Buscar Noticias
    try:
        print("Consultando noticias...")
        url_news = f"https://newsapi.org/v2/everything?q=NVIDIA&language=es&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        resp_news = requests.get(url_news).json()
        articulos = resp_news.get('articles', [])[:3]
        
        if articulos:
            texto = "\n".join([f"- {a['title']}" for a in articulos])
        else:
            texto = "No encontré noticias recientes."
            
    except Exception as e:
        print(f"Falló NewsAPI: {e}")
        texto = "No se pudieron obtener noticias."

    # 3. Análisis con IA (Llamada directa)
    print("Consultando IA...")
    prompt = f"Actúa como analista financiero. Basado en estas noticias de NVIDIA: \n{texto}\n ¿Debo COMPRAR, VENDER o MANTENER? Responde en 2 lineas."
    analisis = consultar_gemini_directo(prompt)

    # 4. Enviar a Telegram
    print("Enviando a Telegram...")
    mensaje_final = f"🤖 **Reporte Financiero**\n\n{analisis}"
    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url_telegram, data={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje_final, 'parse_mode': 'Markdown'})
    
    print("¡Terminado!")

if __name__ == "__main__":
    correr_bot()
