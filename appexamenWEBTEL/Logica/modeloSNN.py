from django.urls import reverse
import pandas as pd
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from appexamenWEBTEL.Logica import modeloSNN
import pickle

class modeloSNN():
    """Clase modelo Preprocesamiento y SNN"""
    #Función para cargar preprocesador
    def cargarPipeline(self,nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    #Función para cargar red neuronal
    def cargarNN(self,nombreArchivo):
        model = load_model(nombreArchivo+'.h5')
        print("Red Neuronal Cargada desde Archivo")
        return model
    #Función para integrar el preprocesador y la red neuronal en un Pipeline
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
    #La siguiente función permite predecir si se aprueba o no un crédito a un nuevo cliente.
    #En la función se define el valor por defecto de las variables, se crea el dataframe con los nuevos valores y
    #los nombres de las variables.
    #El método "predict" ejecuta el Pipeline: los pasos de transformación y la clasificación (mediante la red neuronal).
    #Así se predice si el cliente es bueno (1) o malo (0).
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
