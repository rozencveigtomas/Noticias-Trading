import requests
import os

# Leemos los secretos
TOKEN = os.getenv("TELEGRAM_TOKEN")
ID = os.getenv("TELEGRAM_CHAT_ID")

def probar_telegram():
    print("--- INICIANDO PRUEBA DE CONEXIÓN ---")
    
    # 1. Verificamos si los secretos llegaron al código
    if not TOKEN:
        print("ERROR: No encuentro el TELEGRAM_TOKEN")
        return
    if not ID:
        print("ERROR: No encuentro el TELEGRAM_CHAT_ID")
        return
    
    # Ocultamos parte del token por seguridad en el log
    print(f"Usando Token: {TOKEN[:5]}... y Chat ID: {ID}")

    # 2. Intentamos enviar el mensaje
    mensaje = "🔔 Hola! Si lees esto, la conexión funciona."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    print("Enviando petición a Telegram...")
    respuesta = requests.post(url, data={'chat_id': ID, 'text': mensaje})
    
    # 3. LO MÁS IMPORTANTE: Imprimimos qué respondió Telegram
    print(f"Código de respuesta: {respuesta.status_code}")
    print(f"RESPUESTA DE TELEGRAM: {respuesta.text}")

if __name__ == "__main__":
    probar_telegram()
