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
from DISClib.Algorithms.Graphs import dfs

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
                    'graph': None,
                    'Num_Of_Total_Trips': None,
                    'Edges_Map': None,
                    }

        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1000,
                                              comparefunction=compareStations)
        analyzer['Num_Of_Total_Trips'] = 0  

        analyzer['Edges_Map'] = m.newMap(numelements=750,
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
    addEdgeToMap(citibike,origin,birth,0)
    addEdgeToMap(citibike,destination,birth,1)

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
    citibike['Num_Of_Total_Trips'] = citibike['Num_Of_Total_Trips'] + numFileTrips

def addEdgeToMap(citibike,station,birth,criteria):
    """
    RETO 4 | REQ 5
           | REQ 3 

    A cada estación añade el número de personas en un rango 
    de edad que llegan y salen de la misma.

    Cálcula el total de viajes de sálida y llegada.
    """
    entry = m.get(citibike['Edges_Map'],station) 
    if entry is None:
        edge_entry = newStationEntry()  
        m.put(citibike['Edges_Map'],station,edge_entry)
    else:
        edge_entry = me.getValue(entry)

    if criteria == 0:
        trip_condition = 'Departure_Ages'
        total_trips = 'Total_Departure_Trips'
    if criteria == 1:
        trip_condition = 'Arrival_Ages'
        total_trips = 'Total_Arrival_Trips'

    age = 2020 - int(birth)
    key = ageRange(age)
    if edge_entry[trip_condition][key] is None:
        edge_entry[trip_condition][key] = 1
    else:
        edge_entry[trip_condition][key] = edge_entry[trip_condition][key] + 1

    edge_entry[total_trips] = edge_entry[total_trips] + 1

def newStationEntry():
    """
    Crea un entry en el mapa para una estación.
    Tiene tres llaves:
        Rango de edades de viajes que salen del vértice.
        Rango de edades de viajes que llegan al vértice.
        Número total de viajes.
    """
    entry = {'Arrival_Ages':None,'Departure_Ages':None,'Total_Arrival_Trips':0,'Total_Departure_Trips':0}

    entry['Arrival_Ages'] = {'Menor de 10': None, '11-20': None, '21-30': None, '31-40': None,
                            '41-50': None, '51-60': None, 'Mayor de 60': None}
    entry['Departure_Ages'] = {'Menor de 10': None, '11-20': None, '21-30': None, '31-40': None,
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
        
        sameSCC = m.newMap(numelements=7500,
                        maptype='CHAINING',
                        loadfactor=2,
                        comparefunction=compareStations)

        sc = scc.KosarajuSCC(graph)  
        initial_sc_number = m.get(sc['idscc'],initial_station)
        all_stations = m.keySet(sc['idscc'])

        accum_time = 0

        iterator = it.newIterator(all_stations)
        while it.hasNext(iterator):
            station = it.next(iterator)
            sc_number = m.get(sc['idscc'],station)

            if sc_number == initial_sc_number:
                m.put(sameCC,station,None)
    


        search = dfs.DepthFirstSearch()





        adjacents = gr.adjacents(sc,initial_station)



        iterator = it.newIterator(adjacents)
        while it.hasNext(iterator):
            adja = it.next(iterator)
            edge = gr.getEdge(sc,initial_station,adja)
        
def criticalStations(citibike):
    """
    RETO 4 | REQ 3
    Retorna:
        La estación de donde salen más viajes.
        La estación a donde llegan más viajes.

    """
    
    stations_keys = m.keySet(citibike['Edges_Map'])
    max_value1 = 0
    max_value2= 0
    min_value = 10000

    iterator1 = it.newIterator(stations_keys)
    while it.hasNext(iterator1):
        station = it.next(iterator1)
        sta = m.get(citibike['Edges_Map'],station)

        total_arrival_trips = sta['value']['Total_Arrival_Trips']
        total_departure_trips = sta['value']['Total_Departure_Trips']

        if total_arrival_trips > max_value1:
            max_value1 = total_arrival_trips
            most_arrival = sta

        if total_departure_trips > max_value2:
            max_value2 = total_departure_trips
            most_departure = sta

        if (total_departure_trips + total_arrival_trips) < min_value:
            min_value = (total_departure_trips + total_arrival_trips)
            least_used = sta
        
    return most_departure, most_arrival, least_used
        



def routeRecommenderByAge(citibike,age):
    """
    RETO 4 | REQ 5
    Retorna la ruta más transitada por 
    las personas en el rango de edad ingresado
    """
    key = ageRange(int(age))

    if key is not None:

        stations_keys = m.keySet(citibike['Edges_Map'])

        max_value1 = 0
        max_value2 = 0
        iterator1 = it.newIterator(stations_keys)
        while it.hasNext(iterator1):
            station = it.next(iterator1)
            sta = m.get(citibike['Edges_Map'],station)

            departure_trips_by_age = sta['value']['Departure_Ages'][key]

            if departure_trips_by_age is not None:
                if departure_trips_by_age > max_value1:
                    max_value1 = departure_trips_by_age
                    departure_station = sta
            
            arrival_trips_by_age = sta['value']['Arrival_Ages'][key]

            if arrival_trips_by_age is not None:
                if arrival_trips_by_age > max_value2:
                    max_value2 = arrival_trips_by_age
                    arrival_station = sta
                
        paths = djk.Dijkstra(citibike['graph'],departure_station['key'])
        pathTo = djk.pathTo(paths,arrival_station['key'])
        cost = djk.distTo(paths,arrival_station['key'])

        return departure_station, arrival_station, pathTo , key , cost
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
    if age >= 11 and age <= 20:
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