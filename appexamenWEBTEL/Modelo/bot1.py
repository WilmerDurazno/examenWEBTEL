#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

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

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hola!'),
    update.message.reply_text('Como puedo ayudarte!')



def consulta(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("1. prediccion de Diabetes")
    update.message.reply_text("2. Horario de Atencion")
    
def input_text(update,context):
    text=update.message.text

    print(text)



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def diabete(update, context):
    if(update.message.text.upper().find("CONSULTA")>0):
        update.message.reply_text("1. prediccion de Diabetes")
        update.message.reply_text("2. Horario de atencion")
    elif(update.message.text.upper().find("PREDICCION")>0):
        update.message.reply_text("edad (18-98)")
    elif(update.message.text.upper().find("EDAD")>0):
        update.message.reply_text("Genero (MALE-FEMALE)")
    elif(update.message.text.upper().find("MALE")>0):
        update.message.reply_text(" Producción Excesiva Orina=(Yes-No)")
    elif(update.message.text.upper().find("FEMALE")>0):
        update.message.reply_text(" Producción Excesiva Orina=(Yes-No)")
    elif(update.message.text.upper().find("ORINA")>0):
        update.message.reply_text(" Sed Excesiva=(Yes-No)")
    elif(update.message.text.upper().find("EXCESIVA")>0):
        update.message.reply_text("(mucha - poco) Debilidad=(Yes-No)")
    elif(update.message.text.upper().find("DEBILIDAD")>0):
        update.message.reply_text("Comer en Exceso=(Yes-No)")
    elif(update.message.text.upper().find("EXCESO")>0):
        update.message.reply_text("(mucho-poco)Sobrepeso =(Yes-No)")
    elif(update.message.text.upper().find("SOBREPESO")>0):
        update.message.reply_text("Pérdida Movimiento Muscular=(Yes-No)")
    elif(update.message.text.upper().find("MOVIMIENTO")>0):
        update.message.reply_text(" Irritabilidad=(Yes-No)")
    elif(update.message.text.upper().find("YES")>0):
        update.message.reply_text("Positivo para Contraer Diabetes")
    elif(update.message.text.upper().find("NO")>0):
        update.message.reply_text("Negativo para Contraer Diabetes")
    elif(update.message.text.upper().find("HORARIO")>0):
        update.message.reply_text("Se atiende las 24 horas de Lunes a Viernes")
    elif "comentario" in texto:
        twt=texto
        texto_respuesta=predecir(twt)
    else:
        twt=[texto]
        texto_respuesta=predecir(twt)
            

def predecir(request):
        try:
            #Formato de datos de entrada
            Age = int(request.POST.get('Age'))
            Gender = request.POST.get('Gender')
            Polyuria=request.POST.get('Polyuria')
            Polydipsia=request.POST.get('Polydipsia')
            sudden_weight_loss=request.POST.get('sudden_weight_loss')
            weakness=request.POST.get('weakness')
            Polyphagia=request.POST.get('Polyphagia')  #campos de mi formulario 
            Obesity=request.POST.get('Obesity')
            partial_paresis=request.POST.get('partial_paresis')
            Irritability=request.POST.get('Irritability')
            resul=predict(Age=Age,Gender=Gender,Polyuria=Polyuria,Polydipsia=Polydipsia,sudden_weight_loss=sudden_weight_loss,weakness=weakness
            , Polyphagia=Polyphagia , Obesity=Obesity, partial_paresis=partial_paresis, Irritability=Irritability)

        except Exception as e:
            resul='Datos inválidos Comprube Nuevamente'
            print(e)
        return render(request, "informe.html",{"e":resul}) 
    
def predict(Age=23,Gender='Male',Polyuria='No',Polydipsia='No',sudden_weight_loss='No',weakness='No',Polyphagia='No',Genital_thrush='Yes',visual_blurring='No',Itching='Yes',Irritability='Yes',delayed_healing='Yes',partial_paresis='No',muscle_stiffness='No',Alopecia='Yes',Obesity='No'):
        pipe=self.cargarModelo(self)
        cnames = ['Age','Gender','Polyuria','Polydipsia','sudden_weight_loss','weakness','Polyphagia','Genital_thrush','visual_blurring','Itching','Irritability','delayed_healing','partial_paresis','muscle_stiffness','Alopecia','Obesity']
        Xnew = [Age,Gender,Polyuria,Polydipsia,sudden_weight_loss,weakness,Polyphagia,Genital_thrush,visual_blurring,Itching,Irritability,delayed_healing,partial_paresis,muscle_stiffness,Alopecia,Obesity ]
        Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
        pred = (pipe.predict(Xnew_Dataframe) > 0.5).astype("int32")
        pred = pred.flatten()[0]# de 2D a 1D
        if pred==1:
            pred='Positivo la Persona puede contraer diabetes'
        else:
            pred='Negativo  NO puede contraer diabetes'
        return pred

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1838167615:AAHGo88g3pxVNMlBJO91G9QawYTkY2LmWEE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("consulta", consulta))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, diabete))


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