  
import datetime
from aula1Functions import subproblema1, subproblema3, subproblema4, subproblema5, aulas, validarVacio, hora 
#funcionalidad y desarrollo del proceso para 2 sesiones 
def process2(listaPython,isLab,nameLab,startTimeTest, endTimeTest,
                         dayTest, piso, capacity, buildCode,startTimeTest2, endTimeTest2, dayTest2):
    #cast de hora de variables ingresadas por el usuario
    startTimeCastTest=datetime.datetime.strptime(startTimeTest, "%H:%M").time()
    endTimeCastTest=datetime.datetime.strptime(endTimeTest, "%H:%M").time() 
    startTimeCastTest2=datetime.datetime.strptime(startTimeTest2, "%H:%M").time()
    endTimeCastTest2=datetime.datetime.strptime(endTimeTest2, "%H:%M").time() 
    answer1=subproblema1(listaPython, isLab,nameLab)
    answer2=subproblema2_2(answer1, dayTest, startTimeCastTest, endTimeCastTest,
                       dayTest2,startTimeCastTest2, endTimeCastTest2)
    answer3=subproblema3(answer1, piso, capacity, buildCode)  
    answer4=subproblema4(answer2, answer3)
    answer5= subproblema5(answer4,piso, answer1, answer2,capacity, buildCode)
    respAula= aulas(answer5)
    return(validarVacio(respAula))  

# primer subpproblema día y hora  para dos sesiones
def subproblema2_2(listaPython,dayTest,startTimeCastTest, endTimeCastTest,dayTest2,startTimeCastTest2, endTimeCastTest2):
    aulasAptas=[]
    for aula in listaPython:
        sessions_list=[]
        espacios=aula["groups"]
        for espacVal in espacios:
            sessions = espacVal['sessions']
            sessions_list.extend(sessions)
        if hora(sessions_list,dayTest,startTimeCastTest, endTimeCastTest) and hora(sessions_list,dayTest2,startTimeCastTest2, endTimeCastTest2) :
            aulasAptas.append(aula)
    return (aulasAptas)