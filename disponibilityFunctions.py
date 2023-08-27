from datetime import datetime, timedelta
from aula1Functions import  subproblema3,  aulas, validarVacio
###### definicion de funciones #######
# funcionalidad y desarrollo del proceso para obtener disponibilidad 
def processDisponibility(input,piso,buildCode,dayTest, morning):
    aulaList=subproblema3(input, piso, 0, buildCode)  
    sesionesAulas= sesiones(aulaList)
    if(morning== True):
        slots= slotsMorningAulas(sesionesAulas, dayTest)
        agregar_mensaje_lista_vacia(slots)
        respJson= disponibilityJson(slots)
        union=unirDisponibilidad(respJson, aulaList)
        respuesta=aulas(union)
        return (validarVacio(respuesta))
    else:
        slots= slotsAfternoonAulas(sesionesAulas, dayTest)
        agregar_mensaje_lista_vacia(slots)
        respJson= disponibilityJson(slots)
        union=unirDisponibilidad(respJson, aulaList)
        respuesta=aulas(union)
        return (validarVacio(respuesta))
# primer subpproblema obtener sesiones 
def sesiones(listaPython):
    sesionesAulas=[]
    for aula in listaPython:
        sessions_list=[]
        espacios=aula["groups"]
        for espacVal in espacios:
            sessions = espacVal['sessions']
            sessions_list.extend(sessions)
        sesionesAulas.append(sessions_list)
    return (sesionesAulas) 
# funcion que realiza cast de las horas de cada sesión 
def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M')
#función que devuelve intervalos de tiempo disponibles en el día  
def get_available_slots_morning(schedule, day):
    day_schedule = [slot for slot in schedule if slot['day'] == day]
    day_schedule.sort(key=lambda x: parse_time(x['startTime']))
    
    available_slots = []
    previous_end = parse_time('07:00')
    
    for slot in day_schedule:
        start_time = parse_time(slot['startTime'])
        end_time = parse_time(slot['endTime'])
        
        if start_time > previous_end:
            available_slots.append((previous_end, start_time))
        
        previous_end = end_time if end_time > previous_end else previous_end
    
    if previous_end < parse_time('13:00'):
        available_slots.append((previous_end, parse_time('13:00')))
    
    return available_slots
#funcion que obtiene slots de tiempo durante la mañana para varias aulas 
def slotsMorningAulas (sessionList, day_input):
    respuesta=[]
    for session in sessionList:
        respuesta1=[]
        available_slots = get_available_slots_morning(session, day_input)
        for start, end in available_slots:
            respuesta1.append(f"{start.time().strftime('%H:%M')} - {end.time().strftime('%H:%M')}")
        respuesta.append(respuesta1)
    return(respuesta)
#función que devuelve intervalos de tiempo disponibles en la tarde 
def get_available_slots_afternoon(schedule, day):
    day_schedule = [slot for slot in schedule if slot['day'] == day]
    day_schedule.sort(key=lambda x: parse_time(x['startTime']))
    
    available_slots = []
    previous_end = parse_time('14:00')
    
    for slot in day_schedule:
        start_time = parse_time(slot['startTime'])
        end_time = parse_time(slot['endTime'])
        
        if start_time > previous_end:
            available_slots.append((previous_end, start_time))
        
        previous_end = end_time if end_time > previous_end else previous_end
    
    if previous_end < parse_time('20:00'):
        available_slots.append((previous_end, parse_time('20:00')))
    
    return available_slots
#funcion que obtiene slots de tiempo durante la tarde para varias aulas 
def slotsAfternoonAulas (sessionList, day_input):
    respuesta=[]
    for session in sessionList:
        respuesta1=[]
        available_slots = get_available_slots_afternoon(session, day_input)
        for start, end in available_slots:
            respuesta1.append(f"{start.time().strftime('%H:%M')} - {end.time().strftime('%H:%M')}")
        respuesta.append(respuesta1)
    return(respuesta)

#definicion del atrubuto disponibility
def dispoDefine(disp):
    return{
        "disponibility": disp
    }
# adicion del atributo disponibility a todos los objetos
def disponibilityJson(listaDisp):
    listajson=[]
    for dispo in listaDisp:
        listajson.append(dispoDefine(dispo))
    return listajson
# une la lista de disponibilidad y la lista de aulas 
def unirDisponibilidad(listaDisp, listaAulas):
    for i in range(len(listaDisp)):
        diccionario1 = listaDisp[i]
        diccionario2 = listaAulas[i]
        diccionario2.update(diccionario1)
    return(listaAulas)

# Verifica si la sublista está vacía
def agregar_mensaje_lista_vacia(lista_de_listas):
    for sublista in lista_de_listas:
        if sublista == []:  
            sublista.append("NO DISPONIBLE")

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
