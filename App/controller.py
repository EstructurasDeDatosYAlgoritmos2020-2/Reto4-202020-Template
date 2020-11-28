"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
import os
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicialización  del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(analyzer):
    """
    Función que carga todos los archivos .csv
    encontrados en Data.
    Llama a la función loadFile para cargarlos
    individualmente.
    """
   
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer,filename)
            
def loadFile(citibike, tripfile):
    """
    Carga uno por uno los archivos encontrados 
    en la carpeta Data.

    Llama a la función en model para contar 
    el total de viajes en bici realizados.
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile,encoding ="utf-8"),delimiter=",")

    num_trips = 0
    for trip in input_file:
        model.addTrip(citibike,trip)
        num_trips = num_trips + 1
    model.addNumTripsToTotal(citibike,num_trips)  
# ___________________________________________________
#  Funciones para consultas de requerimientos
# ___________________________________________________

def numConnectedComponents(citibike,station1,station2):
    """
    RETO4 | REQ1
    Llama a la función en el model
    que retorna los componentes fuertemente 
    conectados.
    """
    return model.numSCC(citibike['graph']) , model.sameCC(citibike['graph'],station1,station2)

def touristroutes(citibike,initial_station,time1,time2):
    """
    RETO4 | REQ 2
    Llama a la función en el model que retorna
    las rutas turísticas posibles.
    """
    return model.touristroutes(citibike['graph'],initial_station,time1,time2)

def criticalStations(citibike):
    """
    RETO4 | REQ 3
    Llama a la función en el model que retorna las 
    estaciones críticas.
    """
    return model.criticalStations(citibike)

def routeRecommenderByAge(citibike,age):
    """
    RETO4 | REQ 5
    Llama a la función en el model que retorna
    la ruta más transitada por las personas en el 
    rango de edad ingresado
    """ 
    return model.routeRecommenderByAge(citibike,age)

def getToStationFromCoordinates(citibike,Lat1,Lon1,Lat2,Lon2):
    """
    RETO4 | REQ 6
    Llama a la función en el model que:
        Dada una latitud y longitud inicial,
        se halla la estación de Citibike más cercana.

        Dada una coordenada de destino, se halla
        la estación de Citibike más cercana.

        Se calcula la ruta de menor tiempo entre estas 
        dos estaciones.
    """
    return model.getToStationFromCoordinates(citibike,Lat1,Lon1,Lat2,Lon2)

# ___________________________________________________
#  Funciones para consultas generales
# ___________________________________________________

def numStations(citibike):
    """
    Llama la función en model que retorna
    el número de estaciones (vértices).
    """
    return model.numStations(citibike)

def numConnections(citibike):
    """
    Llama la función en model que retorna
    el número de conexiones (arcos) entres
    estaciones.
    """
    return model.numConnections(citibike)

