#Chatbot Con URLs

#Importar librerias
import json
import requests
import datetime
import re
from django.urls import reverse
import pandas as pd
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
import pickle
from django.shortcuts import render
#Crear un bot en Tetelegram
#1. Buscar en Telegram el usuario: BotFather
#2. Escribir: /newbot
#3. Poner un nombre para el bot: TiendaCafebot
#4. Poner un username para el bot: TiendaCafebot
#5. Copiar el Token en la nuestra aplicación

#Done! Congratulations on your new bot. You will find it at t.me/TiendaCafebot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#Use this token to access the HTTP API:
#1737830611:AAFUZbwuLX8bg2b32BY8Wn0ioPImhOdOESc
#Keep your token secure and store it safely, it can be used by anyone to control your bot.
#For a description of the Bot API, see this page: https://core.telegram.org/bots/api

#Variables para el Token y la URL del chatbot
#TOKEN = "1670746171:AAF81Z0_ufMXq5Bj-rIDyyhMLUra1Q2e3os" #TiendaCafebot
TOKEN="1838167615:AAHGo88g3pxVNMlBJO91G9QawYTkY2LmWEE"
URL = "https://api.telegram.org/bot" + TOKEN + "/"

def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

def update(offset):
    #Llamar al metodo getUpdates del bot, utilizando un offset
    respuesta = requests.get(URL + "getUpdates" + "?offset=" + str(offset) + "&timeout=" + str(100))
 
 
    #Decodificar la respuesta recibida a formato UTF8
    mensajes_js = respuesta.content.decode("utf8")
 
    #Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)
 
    #Devolver este diccionario
    return mensajes_diccionario
 
def info_mensaje(mensaje):
 
    #Comprobar el tipo de mensaje
    if "text" in mensaje["message"]:
        tipo = "texto"
    elif "sticker" in mensaje["message"]:
        tipo = "sticker"
    elif "animation" in mensaje["message"]:
        tipo = "animacion" #Nota: los GIF cuentan como animaciones
    elif "photo" in mensaje["message"]:
        tipo = "foto"
    else:
        # Para no hacer mas largo este ejemplo, el resto de tipos entran
        # en la categoria "otro"
        tipo = "otro"
 
    #Recoger la info del mensaje (remitente, id del chat e id del mensaje)
    persona = mensaje["message"]["from"]["first_name"]
    id_chat = mensaje["message"]["chat"]["id"]
    id_update = mensaje["update_id"]
 
    #Devolver toda la informacion
    return tipo, id_chat, persona, id_update
 
def leer_mensaje(mensaje):
 
    #Extraer el texto, nombre de la persona e id del último mensaje recibido
    texto = mensaje["message"]["text"]
    #Devolver las dos id, el nombre y el texto del mensaje
    return texto
 
def enviar_mensaje(idchat, texto):
    #Llamar el metodo sendMessage del bot, passando el texto y la id del chat
    requests.get(URL + "sendMessage?text=" + texto + "&chat_id=" + str(idchat))

#Variable para almacenar la ID del ultimo mensaje procesado
ultima_id = 0

def cargarPipeline(self,nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline

def cargarNN(self,nombreArchivo):
        model = load_model(nombreArchivo+'.h5')
        print("Red Neuronal Cargada desde Archivo")
        return model

def cargarModelo(self):
        #Se carga el Pipeline de Preprocesamiento
        nombreArchivoPreprocesador='Recursos/pipePreprocesadores'
        pipe=self.cargarPipeline(self,nombreArchivoPreprocesador)
        print('Pipeline de Preprocesamiento Cargado')
        cantidadPasos=len(pipe.steps)
        print("Cantidad de pasos: ",cantidadPasos)
        print(pipe.steps)
        #Se carga la Red Neuronal
        modeloOptimizado=self.cargarNN(self,'Recursos/modeloRedNeuronalOptimizada')
        #Se integra la Red Neuronal al final del Pipeline
        pipe.steps.append(['modelNN',modeloOptimizado])
        cantidadPasos=len(pipe.steps)
        print("Cantidad de pasos: ",cantidadPasos)
        print(pipe.steps)
        print('Red Neuronal integrada al Pipeline')
        return pipe
def predict(self,Age=23,Gender='Male',Polyuria='No',Polydipsia='No',sudden_weight_loss='No',weakness='No',Polyphagia='No',Genital_thrush='Yes',visual_blurring='No',Itching='Yes',Irritability='Yes',delayed_healing='Yes',partial_paresis='No',muscle_stiffness='No',Alopecia='Yes',Obesity='No'):
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
def predecir(request):
        try:
            #Formato de datos de entrada
            Age = int(request.POST.get('Age'))
            Gender = request.POST.get('Gender')
            #TASAPAGO = float(request.POST.get('TASAPAGO'))
            #EDAD = int(''+request.POST.get('EDAD'))
            #CANTIDADPERSONASAMANTENER= int(''+request.POST.get('CANTIDADPERSONASAMANTENER'))
            Polyuria=request.POST.get('Polyuria')
            Polydipsia=request.POST.get('Polydipsia')
            sudden_weight_loss=request.POST.get('sudden_weight_loss')
            weakness=request.POST.get('weakness')
            Polyphagia=request.POST.get('Polyphagia')  #campos de mi formulario 
            Obesity=request.POST.get('Obesity')
            partial_paresis=request.POST.get('partial_paresis')
            Irritability=request.POST.get('Irritability')


            #Consumo de la lógica para predecir si se aprueba o no el crédito
            #llama a los datos y hace la prediccion muestra los resultados si la persona tiene o no Diabetes
            resul=predict(Age=Age,Gender=Gender,Polyuria=Polyuria,Polydipsia=Polydipsia,sudden_weight_loss=sudden_weight_loss,weakness=weakness
            , Polyphagia=Polyphagia , Obesity=Obesity, partial_paresis=partial_paresis, Irritability=Irritability)

        except Exception as e:
            resul='Datos inválidos Comprube Nuevamente'
            print(e)
        return resul

 
while(True):
    mensajes_diccionario = update(ultima_id)
    print(mensajes_diccionario)
    for i in mensajes_diccionario["result"]:
 
        #Guardar la informacion del mensaje
        tipo, idchat, nombre, id_update = info_mensaje(i)
 
        print(idchat)
    
        #Generar una respuesta dependiendo del tipo de mensaje
        if tipo == "texto":
            texto = leer_mensaje(i)
            print(texto)
            if "Hola" in texto:
                texto_respuesta = "Hola, " + nombre + "!"
            elif "Adios" in texto:
                texto_respuesta = "Hasta pronto " + nombre + "!"
            elif "Hacer consulta" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "Deseo café" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "deseo cafe" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "deseo café" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "me das un cafe" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "me das un café" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "Me das un cafe" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif "Me das un café" in texto:
                texto_respuesta = "Tenemos un rico café, cuesta $2"
            elif es_correo_valido(texto.lower()):
                print(texto)
                texto_respuesta = "Gracias por tu correo, nos pondremos en contacto contigo"
                
            elif "comentario"in texto:
                twt=texto
                texto_respuesta=predecir(twt)
            else:
                twt=[texto]
                texto_respuesta=predecir(twt)
            
        elif tipo == "sticker":
            texto_respuesta = "Hola "+ nombre +", Bonito sticker!"
        elif tipo == "animacion":
            texto_respuesta = "Hola "+ nombre +", Me gusta este GIF!"
        elif tipo == "foto":
            texto_respuesta = "Hola "+ nombre +", Bonita foto!"
        elif tipo == "otro":
            texto_respuesta = "Es otro tipo de mensaje"
 
        print(texto_respuesta)
        #Si la ID del mensaje es mayor que el ultimo, se guarda la ID + 1
        if id_update > (ultima_id-1):
            ultima_id = id_update + 1
 
        #Enviar la respuesta
        enviar_mensaje(idchat, texto_respuesta)
 
    #Vaciar el diccionario
    mensajes_diccionario = []