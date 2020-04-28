#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import configparser, argparse
import logging
import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from webscreenshot.webscreenshot import *
from gtts import gTTS
#from selenium import webdriver

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import urllib.request, json, requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def datos_ciudad(ciudad):
	if (ciudad=="santacruz"):
		return ("sc")
	
	if (ciudad=="lapaz"):
		return ("lp")
		
	if (ciudad=="cochabamba"):
		return ("cb")
		
	if (ciudad=="oruro"):
		return ("or")
		
	if (ciudad=="potosi"):
		return ("pt")
		
	if (ciudad=="tarija"):
		return ("tj")
		
	if (ciudad=="chuquisaca"):
		return ("ch")
		
	if (ciudad=="beni"):
		return ("bn")
		
	if (ciudad=="pando"):
		return ("pn")
		
	if (ciudad=="bolivia"):
		return ("bolivia")
		
	if (ciudad=="mapa"):
		return ("mapa")

def obtener_datos(ciudad):
	url=urllib.request.urlopen("https://boliviasegura.agetic.gob.bo/wp-content/json/api.php")
	dato=url.read()
	resultado=json.loads(dato.decode("utf-8"))
	if (ciudad=="mapa"):
	    imagen = Image.open('mapa.png')
	    dibujo = ImageDraw.Draw(imagen)
	    fuente = ImageFont.truetype('FreeMonoBold.ttf', size=20)
	    
	    valor=resultado["departamento"]["pn"]["contador"]["confirmados"]
	    (x, y) = (131, 51)
	    color = 'rgb(237, 28, 36)'
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["sc"]["contador"]["confirmados"]
	    (x, y) = (317, 259)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["lp"]["contador"]["confirmados"]
	    (x, y) = (95, 192)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["cb"]["contador"]["confirmados"]
	    (x, y) = (167, 267)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["or"]["contador"]["confirmados"]
	    (x, y) = (105, 321)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["pt"]["contador"]["confirmados"]
	    (x, y) = (132, 390)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["tj"]["contador"]["confirmados"]
	    (x, y) = (227, 440)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["ch"]["contador"]["confirmados"]
	    (x, y) = (237, 397)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	    
	    valor=resultado["departamento"]["bn"]["contador"]["confirmados"]
	    (x, y) = (193, 125)
	    dibujo.text((x, y), str(valor), fill=color, font=fuente)
	     
	    valor=resultado["contador"]["confirmados"]
	    (x, y) = (225, 10)
	    dibujo.text((x, y), "Total Confirmados :"+str(valor), fill=color, font=fuente)
	    
	    valor=resultado["contador"]["decesos"]
	    (x, y) = (225, 30)
	    dibujo.text((x, y), "Total Muertos     :"+str(valor), fill=color, font=fuente)
	    
	    valor=resultado["contador"]["recuperados"]
	    (x, y) = (225, 50)
	    dibujo.text((x, y), "Total Recuperados :"+str(valor), fill=color, font=fuente)
	    
	    valor=resultado["contador"]["sospechosos"]
	    (x, y) = (225, 70)
	    dibujo.text((x, y), "Total Sospechosos :"+str(valor), fill=color, font=fuente)
	    
	    valor=resultado["fecha"]
	    (x, y) = (20, 510)
	    dibujo.text((x, y), "Actualizado:"+str(valor), fill=color, font=fuente)
	    
	    imagen.save('mapa_temporal.png')
	    
	    return ("mapa")

	if (ciudad=="bolivia"):
	    confirmados=resultado["contador"]["confirmados"]
	    muertos=resultado["contador"]["decesos"]
	    sospechosos=resultado["contador"]["sospechosos"]
	    recuperados=resultado["contador"]["recuperados"]
	    descartados=resultado["contador"]["descartados"]
	    fechahora=resultado["fecha"]
	    return ("Actualizado: "+fechahora+"\n\n<b>Confirmados:          </b>"+str(confirmados)+"🤒\n"+"<b>Muertos:                    </b>"+str(muertos)+"😵\n"+"<b>Recuperados:           </b>"+str(recuperados)+"😷\n"+"<b>Sospechosos:           </b>"+str(sospechosos)+"🤧\n"+"<b>Descartados:           </b>"+str(descartados)+"🥳")
	else:
	    confirmados=resultado["departamento"][ciudad]["contador"]["confirmados"]
	    muertos=resultado["departamento"][ciudad]["contador"]["decesos"]
	    sospechosos=resultado["departamento"][ciudad]["contador"]["sospechosos"]
	    recuperados=resultado["departamento"][ciudad]["contador"]["recuperados"]
	    descartados=resultado["departamento"][ciudad]["contador"]["descartados"]
	    fechahora=resultado["fecha"]
	    return ("Actualizado: "+fechahora+"\n\n<b>Confirmados:          </b>"+str(confirmados)+"🤒\n"+"<b>Muertos:                    </b>"+str(muertos)+"😵\n"+"<b>Recuperados:           </b>"+str(recuperados)+"😷\n"+"<b>Sospechosos:           </b>"+str(sospechosos)+"🤧\n"+"<b>Descartados:           </b>"+str(descartados)+"🥳")
		
def responder(update, context):
    """Responder al mensaje dependiendo de la ciudad"""
    minuscula=update.message.text
    minuscula=(minuscula.lower())
    minuscula=''.join(minuscula.split())
    ciudad=datos_ciudad(minuscula)
    usuario = update.message.from_user
    if (ciudad=="mapa"):
	    obtener_datos(ciudad)
	    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('mapa_temporal.png','rb'))
    else:
	    update.message.reply_text(obtener_datos(ciudad), parse_mode=ParseMode.HTML)
    ahora = datetime.datetime.now()
    print(str(ahora.strftime("%Y-%m-%d %H:%M:%S"))+' Se respondio con Exito, Comando: '+ciudad+"   Usuario:"+usuario.first_name+" "+usuario.last_name)


def error(update, context):
    update.message.reply_text("Lista de comandos/palabras soportadas: \n Bolivia \n Mapa \n Santa cruz \n Cochabamba \n Oruro \n Potosi \n Sucre \n Beni \n Pando \n Chquisaca \n La Paz \n /pais NombreDelPais ", parse_mode=ParseMode.HTML)
    """Log Errors caused by Updates."""
    #logger.warning('Update "%s" caused error "%s"', update, context.error)
    
def resultado_pais(update, context):
    url=urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json")
    dato=url.read()
    resultado=json.loads(dato.decode("utf-8"))
    pais=context.args[0].capitalize()
    opcion=str(context.args[1])
    if (opcion!="audio"):
	    opcion=opcion.capitalize();
	    pais=pais+" "+opcion
	    
    fecha=resultado[pais][-1]["date"]
    confirmados=resultado[pais][-1]["confirmed"]
    muertos=resultado[pais][-1]["deaths"]
    recuperados=resultado[pais][-1]["recovered"]
    mensaje="Actualizado: "+fecha+"\n\n<b>Confirmados:          </b>"+str(confirmados)+"🤒\n"+"<b>Muertos:                    </b>"+str(muertos)+"😵\n"+"<b>Recuperados:           </b>"+str(recuperados)+"😷\n"
    update.message.reply_text(mensaje, parse_mode=ParseMode.HTML)
    usuario = update.message.from_user
    print('Se respondio con Exito, Pais: '+pais+"   Usuario:"+usuario.first_name+" "+usuario.last_name)
    
    if (opcion == "audio"):
	    texto = 'Cantidad de casos confirmados '+str(confirmados)+' Cantidad de Muertos '+str(muertos)+' Cantidad de Recuperados '+str(recuperados)
	    idioma = 'es'
	    temp = gTTS(text=texto, lang=idioma, slow=False) 
	    temp.save("audio_temporal.mp3")
	    context.bot.send_voice(chat_id=update.effective_chat.id, voice=open('audio_temporal.mp3', 'rb'))
	    print('Se envio Audio')
	    
def resultado_titulares(update, context):
    # url list to screenshot
    url_list = ['https://www.boliviasegura.gob.bo/ultimas-noticias']

    # defining options manually
    options = argparse.Namespace(URL=None, ajax_max_timeouts='1400,1800', cookie=None, crop=None, format='png', header=None, http_password=None, http_username=None, imagemagick_binary=None, input_file=None, label=True, label_bg_color='NavajoWhite', label_size=60, log_level='DEBUG', multiprotocol=False, no_xserver=False, output_directory='/home/pi/covid19bolbot', port=None, proxy=None, proxy_auth=None, proxy_type=None, quality=75, renderer='phantomjs', renderer_binary=None, ssl=False, timeout=30, verbosity=2, window_size='1920,1080', workers=4)

    # actually launching the function
    take_screenshot(url_list, options)

    img = Image.open("https_www.boliviasegura.gob.bo_ultimas-noticias.png")
    area = (200, 100, 1720, 1070)
    cropped_img = img.crop(area)

    cropped_img.save("cortada.png")
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('cortada.png','rb'))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("pais", resultado_pais))
    dp.add_handler(CommandHandler("titulares", resultado_titulares))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, responder))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
