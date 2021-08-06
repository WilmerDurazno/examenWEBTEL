#from rest_framework import generics #para microservicio en las siguientes prácticas
from django.shortcuts import render
from appexamenWEBTEL.Logica import modeloSNN #para utilizar el método inteligente

class Clasificacion():
    def determinarAprobacion(request):
        return render(request, "formulario.html")
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
            resul=modeloSNN.modeloSNN.predict(modeloSNN.modeloSNN,Age=Age,Gender=Gender,Polyuria=Polyuria,Polydipsia=Polydipsia,sudden_weight_loss=sudden_weight_loss,weakness=weakness
            , Polyphagia=Polyphagia , Obesity=Obesity, partial_paresis=partial_paresis, Irritability=Irritability)

        except Exception as e:
            resul='Datos inválidos Comprube Nuevamente'
            print(e)
        return render(request, "informe.html",{"e":resul})
    def inicio(request):
        return render(request,"index.html")
