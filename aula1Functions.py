
import requests
import json
import datetime
from typing import Union


###### definicion de funciones #######
# funcion para obtener las aulas del backend 
def obtenerHorarios(idSchedule):
    peticion  = f'https://localhost:7130/api/classroom/byCalendar/{idSchedule}'
    response = requests.get(peticion, verify=False)
    listaJson =  response.json()
    cadenaJson = json.dumps(listaJson)
    listaPython = json.loads(cadenaJson)
    return listaPython
    
#funcionalidad y desarrollo del proceso para 1 sesión 
def process(listaPython,isLab,nameLab,startTimeTest, endTimeTest, dayTest, piso, capacity, buildCode):
    #cast de hora de variables ingresadas por el usuario
    startTimeCastTest=datetime.datetime.strptime(startTimeTest, "%H:%M").time()
    endTimeCastTest=datetime.datetime.strptime(endTimeTest, "%H:%M").time() 
    answer1=subproblema1(listaPython, isLab, nameLab)
    answer2=subproblema2(answer1, dayTest, startTimeCastTest, endTimeCastTest)
    answer3=subproblema3(answer1, piso, capacity, buildCode)  
    answer4=subproblema4(answer2, answer3)
    answer5= subproblema5(answer4,piso, answer1, answer2,capacity, buildCode)
    respAula= aulas(answer5)
    return(validarVacio(respAula)) 
#filtro que verifica si una aula es labotario para reducir el numero de aulas con las que iterar
def subproblema1(lista, isLab, nameLab):
    aulaLab=[]
    if(nameLab == "null"):
        for aula in lista:
            if aula['isLab']== isLab:
                aulaLab.append(aula)
        return aulaLab
    else:
        for aula in lista:
            if aula['isLab']== isLab and aula['name']== nameLab:
                aulaLab.append(aula)
        return aulaLab

# funcion que verifica día y hora de inicio y final a ver si se puede ingresar el aula 
def hora (sessionsList, dayTest, startTimeCastTest, endTimeCastTest ):
    listaReview=[]
    for sessions in sessionsList:
        startTime_=sessions['startTime']
        endTime_=sessions['endTime']
        startTimeCast=datetime.datetime.strptime(startTime_, "%H:%M").time()
        endTimeCast=datetime.datetime.strptime(endTime_, "%H:%M").time()
        if sessions['day']== dayTest:
            if startTimeCast >= startTimeCastTest and endTimeCast <= endTimeCastTest or startTimeCast <= startTimeCastTest < endTimeCast and startTimeCast <= endTimeCastTest <= endTimeCast or startTimeCast < endTimeCastTest < endTimeCast or startTimeCast < startTimeCastTest < endTimeCast:
                listaReview.append(False)
            else:
                listaReview.append(True)
    validation = all(listaReview)
    if validation:
        return(True)
    else:
        return (False)
# primer subpproblema día y hora  
def subproblema2(listaPython,dayTest,startTimeCastTest, endTimeCastTest):
    aulasAptas=[]
    for aula in listaPython:
        sessions_list=[]
        espacios=aula["groups"]
        for espacVal in espacios:
            sessions = espacVal['sessions']
            sessions_list.extend(sessions)
        if hora(sessions_list,dayTest,startTimeCastTest, endTimeCastTest):
            aulasAptas.append(aula)
    return (aulasAptas)
# segundo subproblema ubicacion y capacidad del aula 
def subproblema3(inputList, pisoTest, capacity, buildCode):
    aulasObtenidas=[]
    if(pisoTest=='null' and buildCode== 'null' and capacity=='null' ):
        return (inputList)
    if(pisoTest=='null' and buildCode== 'null' ):
        for aula in inputList:
            if  aula['capacity']>= int(capacity):
                aulasObtenidas.append(aula)
        return (aulasObtenidas)
    if(capacity=='null'):
        for aula in inputList:
            if aula['floor']== pisoTest and aula["building"]["code"]== buildCode:
                aulasObtenidas.append(aula)
        return (aulasObtenidas)
    else: 
        for aula in inputList:
            if  aula['capacity']>= int(capacity) and aula['floor']== pisoTest and aula["building"]["code"]== buildCode:
                aulasObtenidas.append(aula)
        return (aulasObtenidas)
#tercera funcion que une respuestas de subproblema 2 y subproblema 3 y saca respuesta final
def subproblema4(answer2, answer3):
    aulasObtenidas=[]
    for aula1 in answer2:
        for aula2 in answer3:
            if aula1['id'] == aula2['id']:
                aulasObtenidas.append(aula1)
    return (aulasObtenidas)
# validar las alertas y que devuelve cuando no existen las aulas con las especificaciones concretas del usuario
def validarVacio(lista):
    if lista==[]:
        return{
        "status": False,
        "message": "No se encuentran aulas disponibles, cambie los parámetros de búsqueda"
        }
    else:
        return{
        "status": True,
        "aulas": lista
        }  
# en caso de que no se encuentren aulas, se buscan aulas con los mismos parametros de entrada
#pero en los pisos mas cercanos al especificado del edificio  
def subproblema5(lista,piso, answer1, answer2,capacity, buildCode):
    if piso== "null":
        return(lista)
    if lista==[]:
        siguiente = str(int(piso[1:]) + 1)
        anterior = str(int(piso[1:]) - 1)
        siguientePiso = 'P' + siguiente
        anteriorPiso = 'P' + anterior
        resp=subproblema3(answer1, siguientePiso,capacity, buildCode)
        resp2=subproblema3(answer1, anteriorPiso, capacity, buildCode)
        final=subproblema4(answer2, resp)
        final1=subproblema4(answer2, resp2)
        ultimate=final+final1
        return (ultimate)
    else:
        return lista
    
#quitar grupos y unicamente obtener la ifnromación del aula 

def aulas (listaAulas):
    aulasResp=[]
    for aula in listaAulas:
        del aula["groups"]
        aulasResp.append(aula)
    return aulasResp