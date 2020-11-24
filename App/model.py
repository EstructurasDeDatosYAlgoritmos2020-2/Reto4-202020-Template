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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me

from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import edge as e

from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador.
    """
    try:
        analyzer = {
                    '': None,
                    'graph': None,
                    '': None,
                    '': None
                    }

#        analyzer[''] = m.newMap(numelements=14000,
#                                     maptype='PROBING',
#                                     comparefunction=compareStopIds)#

        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStations)
        analyzer['Num Of Total Trips'] = 0  
        analyzer['Arrival Ages'] = m.newMap(numelements=100,
                                                maptype='CHAINING',
                                                loadfactor=2,
                                                comparefunction=compareStations)

        analyzer['Departure Ages'] = m.newMap(numelements=100,
                                                maptype='CHAINING',
                                                loadfactor=2,
                                                comparefunction=compareStations)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    """
    Añade un viaje al grafo.
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    birth = trip['birth year']

    addStation(citibike,origin)
    addStation(citibike,destination)
    addConnection(citibike,origin,destination,duration)
    addAge(citibike, origin,destination,birth)

def addStation(citibike, station_id):
    """
    Agrega el ID de una estación como vértice del grafo si
    es que este no existe.
    """
    if not gr.containsVertex(citibike['graph'],station_id):
        gr.insertVertex(citibike['graph'],station_id)

def addConnection(citibike,origin,destination,duration):
    """
    Adiciona un arco entre dos estaciones.
    Si el arco ya existe, se actualiza su peso promedio.
    """
    edge = gr.getEdge(citibike['graph'],origin,destination)
    if edge is None:
        gr.addEdge(citibike['graph'],origin,destination,duration)
    else:
        e.updateAverageWeight(edge,duration)

def addNumTripsToTotal(citibike,numFileTrips):
    """
    Calcula el total de viajes en bici realizados.
    """
    citibike['Num Of Total Trips'] = citibike['Num Of Total Trips'] + numFileTrips

def addAge(citibike,origin,destination,birth):
    """
    RETO 4 | REQ 5 
    A cada estación añade el número de personas en un rango 
    de edad que llegan y salen de la misma.
    """
    entry1 = m.get(citibike['Arrival Ages'],destination) 
    entry2 = m.get(citibike['Departure Ages'],origin)

    if entry1 is None:
        arrival_age_entry = newStationAgeEntry()  
        m.put(citibike['Arrival Ages'],destination,arrival_age_entry)
    else:
        arrival_age_entry = me.getValue(entry1)

    if entry2 is None:
        departure_age_entry = newStationAgeEntry()  
        m.put(citibike['Departure Ages'],origin,departure_age_entry)
    else:
        departure_age_entry = me.getValue(entry2)    

    age = 2020 - int(birth)    
    key = ageRange(age)
    

    if arrival_age_entry[key] is None:
        arrival_age_entry[key] = 1
    else:
        arrival_age_entry[key] = arrival_age_entry[key] + 1
    
    if departure_age_entry[key] is None:
        departure_age_entry[key] = 1
    else:
        departure_age_entry[key] = departure_age_entry[key] + 1

def newStationAgeEntry():
    """
    Crea un entry en el mapa para una estación 
    cuyas llaves serán los distintos rangos de edades.
    """
    entry = {'Menor de 10': None, '11-20': None, '21-30': None, '31-40': None,
            '41-50': None, '51-60': None, 'Mayor de 60': None}
    return entry

# ==============================
# Funciones de consulta requisitos
# ==============================

def numSCC(graph):
    """
    RETO4 | REQ1
    Retorna el número de componentes fuertemente conectados.
    """
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(graph,station1, station2):
    """
    RETO4 | REQ1
    Consulta si dos vértices pertenecen al mismo componente
    fuertemente conectado.
    """
    sc = scc.KosarajuSCC(graph)

    if gr.containsVertex(graph,station1) and gr.containsVertex(graph,station2):   
        return scc.stronglyConnected(sc, station1, station2)
    else:
        return None

def touristroutes(graph,initial_station,time1,time2):
    """
    RETO4 | REQ2
    Retorna las rutas turísticas posibles
    dado un límite de tiempo y una estación inicial.
    """
    if gr.containsVertex(graph,initial_station):

        sc = scc.KosarajuSCC(graph)

        accum_time = 0
        initial_sc_number = m.get(sc['idscc'],initial_station)
        all_stations = m.keySet(sc['idscc'])

        sameSCC = m.newMap(numelements=75000)
        for station in all_stations:
            sc_number = m.get(sc['idscc'],station)

            if sc_number == initial_sc_number:
                qweqwwq





        adjacents = gr.adjacents(sc,initial_station)



        iterator = it.newIterator(adjacents)
        while it.hasNext(iterator):
            adja = it.next(iterator)
            edge = gr.getEdge(sc,initial_station,adja)
        

def routeRecommenderByAge(citibike,age):
    """
    RETO 4 | REQ 5
    Retorna la ruta más transitada por 
    las personas en el rango de edad ingresado
    """
    key = ageRange(int(age))

    if key is not None:

        arrival_keys = m.keySet(citibike['Arrival Ages'])
        departure_keys = m.keySet(citibike['Departure Ages'])

        max_value1 = 0
        max_value2 = 0

        for station in arrival_keys:
            sta = m.get(citibike['Arrival Ages'],station)
            trips_by_age = sta['value'][age]

            if trips_by_age > max_value1:
                max_value1 = trips_by_age
                winner_arrival_station = sta
        
        for station in departure_keys:
            sta = m.get(citibike['Departure Ages'],station)
            trips_by_age = sta['value'][age]

            if trips_by_age > max_value1:
                max_value1 = trips_by_age
                winner_departure_station = sta

        paths = djk.Dijkstra(citibike['graph'],winner_departure_station['key'])
        pathto = djk.pathTo(citibike['graph'],winner_arrival_station['key'])

        return winner_departure_station, winner_arrival_station, pathto , key
    
    else:
        return None

# ==============================
# Funciones de consulta generales
# ==============================

def numStations(citibike):
    """
    Retorna el número de vértices (estaciones).
    """
    return gr.numVertices(citibike['graph'])

def numConnections(citibike):
    """
    Retorna el número de conexiones (arcos)
    entre estaciones.
    """
    return gr.numEdges(citibike['graph'])

# ==============================
# Funciones Helper
# ==============================

def ageRange(age):
    """
    Función auxiliar para retornar un rango de edad.
    """
    if age <= 10:
        key =  'Menor de 10'  
    elif age >= 11 and age <= 20:
        key = '11-20'
    elif age >= 21 and age <= 30:
        key = '21-30'
    elif age >= 31 and age <= 40:
        key = '31-40'
    elif age >= 41 and age <= 50:
        key = '41-50'
    elif age >= 51 and age <= 60:
        key = '51-60'
    elif age > 60:
        key = 'Mayor de 60'
    else:
        key = None

    return key

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(sta1,sta2):
    """
    Función de comparación entre dos estaciones.
    Usada en el grafo principal.
    """
    station2code = sta2['key']
    if (sta1 == station2code):
        return 0
    elif (sta1 > station2code):
        return 1
    else:
        return -1