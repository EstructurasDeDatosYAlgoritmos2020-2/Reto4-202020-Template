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
assert config

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
    print('Estaciones cargadas: ' + str(controller.numStations(cont)))
    print('Número de conexiones (arcos) entre estaciones cargadas: ' + str(controller.numConnections(cont)))
    
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def printOptionThree(clusters):
    """
    """
    print('Se encontraron: ' + str(clusters[0]) + ' componentes conectados.')
    if clusters[1]  :
        print('Las estaciones ingresadas se encuentran en el mismo cluster.')
    else:
        print('Las estaciones ingresadas NO se encuentran en el mismo cluster.')

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de Sistema CitiBike.")
    print("3- Requerimento 1: Cantidad de clusters de viajes.")
#    print("4- Requerimento 2: Ruta turísitica circular.")
#    print("5- Requerimento 3: Estaciones Críticas.")
#    print("6- Requerimento 4: Ruta turística por resistencia.")
#    print("7- Requerimento 5: Recomendador de rutas.")
#    print("8- Requerimento 6: Ruta de interés turístico.")
#    print("9- Bono 1: Identificación de estaciones para publicidad.")
#    print("10- Bono 2: Identificación de biclicletas para mantenimiento.")

    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de sistema Citibike ...")
        controller.loadTrips(cont)
        printOptionTwo(cont)
       
    elif int(inputs[0]) == 3:
        print("\nRequerimiento No 1 del Reto 4: ")
        sta1 = input("\nIngrese el ID de la estación 1: ")
        sta2 = input("\nIngrese el ID de la estación 2: ")
        clusters = controller.numConnectedComponents(cont,sta1,sta2)
        printOptionThree(clusters)

    elif int(inputs[0]) == 4:
        print("\nRequerimiento No 2 del Reto 4: ")
    elif int(inputs[0]) == 5:
        print("\nRequerimiento No 3 del Reto 4: ")
    elif int(inputs[0]) == 6:
        print("\nRequerimiento No 4 del Reto 4: ")
    elif int(inputs[0]) == 7:
        print("\nRequerimiento No 5 del Reto 4: ")
#    elif int(inputs[0]) == 8:
#        print("\nRequerimiento No 6 del Reto 4: ")

    else:
        sys.exit(0)
sys.exit(0)
