from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Union
from disponibilityFunctions import processDisponibility
from aula1Functions import process, obtenerHorarios
from aula2Functions import process2
from aula3Functions import process3


app = FastAPI()
# funcion que habilita comunicación con la app web accediendo a las politicas de cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ruta para encontrar disponibilidad del aula 
@app.get("/disponibility")
async def get_aulas( idSchedule:int,dayTest:int, piso:str,  buildCode:str, morning:bool  ):
    listaPython = obtenerHorarios(idSchedule)
    respApi=processDisponibility(listaPython,piso,buildCode,dayTest, morning)
    return(respApi)
        
# ruta para encontrar aula con una sesion 
@app.get("/aulas1")
async def get_aulas(idSchedule:int,isLab:bool,startTimeTest:str, endTimeTest:str, dayTest:int, 
                    piso:Union[str, None] = None, capacity:Union[str, None] = None, buildCode:Union[str, None] = None,nameLab:Union[str, None] = None):
    listaPython = obtenerHorarios(idSchedule)
    respuestaApi=process(listaPython,isLab,nameLab,startTimeTest, endTimeTest, dayTest, piso, capacity, buildCode)
    return(respuestaApi)
# ruta para encontrar aula con dos sesiones 
@app.get("/aulas2")
async def get_aulas(idSchedule:int,isLab:bool,startTimeTest:str, endTimeTest:str, dayTest:int,
                    startTimeTest2:str, endTimeTest2:str, dayTest2:int,
                    piso:Union[str, None] = None, capacity:Union[str, None] = None, buildCode:Union[str, None] = None, nameLab:Union[str, None] = None ):
    listaPython = obtenerHorarios(idSchedule)
    respuestaApi=process2(listaPython,isLab,nameLab,startTimeTest, endTimeTest,
                         dayTest, piso, capacity, buildCode,startTimeTest2, endTimeTest2, dayTest2)
    return(respuestaApi) 
# ruta para encontrar aula con tres sesiones 
@app.get("/aulas3")
async def get_aulas(idSchedule:int,isLab:bool,startTimeTest:str, endTimeTest:str, dayTest:int,
                    startTimeTest2:str, endTimeTest2:str, dayTest2:int,
                    startTimeTest3:str, endTimeTest3:str, dayTest3:int,
                    piso:Union[str, None] = None, 
                    capacity:Union[int, None] = None, buildCode:Union[str, None] = None,nameLab:Union[str, None] = None):
    listaPython = obtenerHorarios(idSchedule)
    respuestaApi=process3(listaPython,isLab,nameLab,startTimeTest, endTimeTest,
                         dayTest, piso, capacity, buildCode,startTimeTest2, endTimeTest2, dayTest2,
                         startTimeTest3, endTimeTest3, dayTest3)
    return(respuestaApi) 

# definicion del puerto y direccion del servidor que la api va a ofertar el servicio
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)