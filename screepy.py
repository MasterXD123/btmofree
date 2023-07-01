import asyncio
import csv
import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.utils import escape_markdown
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Token de acceso del bot de Telegram
TOKEN = '1746465553:AAHx1a_0-QTc16vQ_y6lDzqnhC9sio2V3lM'

# ID del canal de Telegram donde se realizarán las publicaciones
CANAL_ID = '@Nodike'

async def cargar_publicaciones():
    with open('datos.csv', 'r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            if len(fila) < 3:
                # Saltar filas sin suficientes elementos
                continue

            texto = fila[0]
            imagen_url = fila[1]
            hora_publicacion = datetime.datetime.strptime(fila[2], '%d/%m/%Y-%H:%M')

            texto_con_formato = texto.replace("\\n", "\n")
            # texto_con_formato = escape_markdown(texto_con_formato)

            # Obtener la hora actual
            ahora = datetime.datetime.now()

            # Comprobar si la hora de publicación es mayor que la hora actual
            if hora_publicacion > ahora:
                # Calcular la diferencia de tiempo hasta la hora de publicación
                diferencia_tiempo = hora_publicacion - ahora

                # Esperar hasta la hora de publicación
                await asyncio.sleep(diferencia_tiempo.total_seconds())

            # Crear los botones de reacciones
            me_gusta_button = InlineKeyboardButton("👍", callback_data="me_gusta")
            me_encanta_button = InlineKeyboardButton("😍", callback_data="me_encanta")
            me_divierte_button = InlineKeyboardButton("😂", callback_data="me_divierte")
            no_me_gusta_button = InlineKeyboardButton("👎", callback_data="no_me_gusta")

            # Crear el botón de enlace
            enlace_button = InlineKeyboardButton("Ver más", url="https://www.tu-enlace-externo.com")

            # Crear el teclado personalizado con los botones de reacciones
            keyboard_reacciones = [me_gusta_button, me_encanta_button, me_divierte_button, no_me_gusta_button]
            # Crear el teclado personalizado con el botón de enlace
            keyboard_enlace = [enlace_button]
            # Crear el teclado personalizado con el botón de enlace y reacciones
            keyboard = [keyboard_reacciones, keyboard_enlace]

            custom_keyboard = InlineKeyboardMarkup(keyboard)

            # Crear la publicación en Telegram
            bot = Bot(TOKEN)
            await bot.send_photo(chat_id=CANAL_ID, photo=imagen_url, caption=texto_con_formato, reply_markup=custom_keyboard, parse_mode='MarkdownV2')

def programar_publicaciones():
    scheduler = AsyncIOScheduler()

    with open('datos.csv', 'r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            if len(fila) < 3:
                # Saltar filas sin suficientes elementos
                continue

            hora_publicacion = datetime.datetime.strptime(fila[2], '%d/%m/%Y-%H:%M')

            scheduler.add_job(cargar_publicaciones, 'date', run_date=hora_publicacion)

    scheduler.start()

async def main():
    await cargar_publicaciones()

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(programar_publicaciones, 'interval', minutes=10)
    scheduler.start()
    asyncio.run(main())
