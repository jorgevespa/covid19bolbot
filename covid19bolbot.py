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

import configparser
import logging
import os
import time

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request, json

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

def obtener_datos(ciudad):
	url=urllib.request.urlopen("https://www.boliviasegura.gob.bo/wp-content/json/api.php")
	dato=url.read()
	resultado=json.loads(dato.decode("utf-8"))
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
    update.message.reply_text(obtener_datos(ciudad), parse_mode=ParseMode.HTML)


def error(update, context):
    """Log Errors caused by Updates."""
    #logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text("Debes escribir el nombre del departamento, del cual quieres obtener los datos o Bolivia para ver el resumen en total.", parse_mode=ParseMode.HTML)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

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
