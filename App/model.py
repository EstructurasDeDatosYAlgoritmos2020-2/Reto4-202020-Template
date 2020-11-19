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

    addStation(citibike,origin)
    addStation(citibike,destination)
    addConnection(citibike,origin,destination,duration)

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