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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config   # nosec

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Funciones para imprimir la información
# ___________________________________________________

def printOptionTwo(cont):
    """
    Imprime la carga de datos.
    """
    print('\nEstaciones (vértices) cargadas: ' + str(controller.numStations(cont)))
    print('Conexiones (arcos) entre estaciones cargadas: ' + str(controller.numConnections(cont)))
    print('Viajes en bici cargados: ' + str(cont['Num_Of_Total_Trips']))

    print('\nEl limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def printOptionThree(clusters):
    """
    RETO4 | REQ1
    Imprime el requerimiento 1.
    """
    print('Se encontraron: ' + str(clusters[0]) + ' componentes fuertemente conectados.')
    if clusters[1] == True:
        print('Las estaciones ingresadas se encuentran en el mismo cluster.')
    elif clusters[1] == False:
        print('Las estaciones ingresadas NO se encuentran en el mismo cluster.')
    else:
        print('Una o ambas estaciones ingresadas no existen.')

def printOptionFour():
    """
    RETO4 | REQ2
    Imprime el requerimiento 2.
    """
    print("Se encontraron un total de " + + "rutas posibles.")

def printOptionFive(critical_stations):
    """
    RETO4 | REQ3
    Imprime el requerimiento 3.
    """
    most_arrival, most_departure , least_used = critical_stations

    print('\nLas estaciones de las que más viajes salen hacia otras estaciones son: ')
    for station in most_departure: 
        print(str(station['key'])+' con: '+ str(station['value']['Total_Departure_Trips']) +' viajes.')

    print('\nLas estaciones a las que más bicis llegan provenientes de otras estaciones son: ')
    for station in most_arrival:
        print(str(station['key'])+' con: '+ str(station['value']['Total_Arrival_Trips']) +' viajes.')

    print('\nLas estaciones menos utilizadas son: ')
    for station in least_used:
        print(str(station['key'])+' con: '+ str(station['value']['Total_Trips']) +' viajes en total.')


def printOptionSeven(route):
    """
    RETO4 | REQ5
    Imprime el requerimiento 5.
    """
    if route is not None:
        departure_station, arrival_station, pathTo , age_range , cost = route
        print('\nLa edad ingresada se encuentra en el rango de: '+ str(age_range) + ' años.')
        print('Estación inicial más común para la edad ingresada: '+ str(departure_station['key']) +
                                                ' con: '+str(departure_station['value']['Departure_Ages'][age_range])+' viajes.')
        print('Estación final más común para la edad ingresada: '+ str(arrival_station['key']) +
                                                ' con: '+str(arrival_station['value']['Arrival_Ages'][age_range])+' viajes.')
        print('La ruta más corta entre estas dos estaciones, tiene un costo de: '+ str(cost) +' segundos, el recorrido es: ')
        while (not stack.isEmpty(pathTo)):
            station = stack.pop(pathTo)
            print(str(station['vertexA'])+' - ' + str(station['vertexB']))
    else:
        print('La edad ingresada no es válida.')

def printOptionEight(routeFromPosition):
    """
    RETO4 | REQ6
    """
    CloserStation1, CloserStation2, PathToFinalStation, Cost = routeFromPosition

    print('\nLa estación más cercana al punto inicial ingresado es la: '+ str(CloserStation1['key'])+
        ', a:  '+ str(CloserStation1['Distance_From_Initial_Point'])+' kilómetros de distancia.')
    
    print('\nLa estación más cercana al punto final ingresado es la: '+ str(CloserStation2['key'])+
        ', a:  '+ str(CloserStation2['Distance_From_Final_Point'])+' kilómetros de distancia.')
    
    print('La ruta más corta entre estas dos estaciones, tiene un costo de: '+ str(Cost) +' segundos, el recorrido es: ')
        while (not stack.isEmpty(pathTo)):
            station = stack.pop(pathTo)
            print(str(station['vertexA'])+' - ' + str(station['vertexB']))

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información del Sistema CitiBike.")
    print("3- Requerimento 1: Cantidad de clusters de viajes.")
#    print("4- Requerimento 2: Ruta turísitica circular.")
    print("5- Requerimento 3: Estaciones Críticas.")
#    print("6- Requerimento 4: Ruta turística por resistencia.")
    print("7- Requerimento 5: Recomendador de rutas.")
    print("8- Requerimento 6: Ruta de interés turístico.")
#    print("9- Bono 1: Identificación de estaciones para publicidad.")
#    print("10- Bono 2: Identificación de biclicletas para mantenimiento.")

    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')   # nosec

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información del sistema Citibike ...")
        controller.loadTrips(cont)
        printOptionTwo(cont)
       
    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del Reto 4: ")
        sta1 = input("\nIngrese el ID de la estación 1: ") 
        sta2 = input("Ingrese el ID de la estación 2: ")    
        clusters = controller.numConnectedComponents(cont,sta1,sta2)
        printOptionThree(clusters)

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del Reto 4: ")
        sta = input("\nIngrese el ID de la estación de inicio.") 
        print("Ingrese el total de tiempo disponible: ")
        t1 = input("Rango inferior: ") 
        t2 = input("Rango superior: ") 
        routes = controller.touristroutes(cont,sta,t1,t2)
        printOptionFour(routes)

    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del Reto 4: ")
        critical_stations = controller.criticalStations(cont)
        printOptionFive(critical_stations)
#    elif int(inputs[0]) == 6:
#        print("\nRequerimiento No 4 del Reto 4: ")

    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del Reto 4: ")
        age = input("Ingrese su edad: ") 
        route = controller.routeRecommenderByAge(cont,age)
        printOptionSeven(route)
    elif int(inputs[0]) == 8:
        print("\nRequerimiento No 6 del Reto 4: ")

        print("\nIngrese la Latitud y Longitud de la posición de inicio:")
        Lat1 = input("Latitud: ")
        Long1 = input("Longitud: ")
        print("\nIngrese la Latitud y Longitud de la posición final:")
        Lat2 = input("Latitud: ")
        Long2 = input("Longitud: ")
        routeFromPosition = controller.getToStationFromCoordinates(cont,Lat1,Long1,Lat2,Long2)
        printOptionEight(routeFromPosition)

    else:
        sys.exit(0)
sys.exit(0)

