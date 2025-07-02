#aca se ejecutarean todas las funciones
#se importan las funciones y librerias necesarios
import sqlite3
from sqlite3 import Error
from clase_productos import *
from transacciones import *
from clase_cliente import *
from clase_ProdAdqu import *
from tablas import *





#creacion y conexion con la bas ede datos
def conexionBD():
    try:
        # se crea repositorio fisico-objeto de conexcion a la base de datos 
        con=sqlite3.connect('basemibanco.db')
        print('la conexion fue exitosa')
        return con
    except Error:
        print(Error)
#cierre conexion

def cerrarBD(con):
    con.close()


print('bienvenido a su banca Virtual\nPara continuar escriba el numero de una de nuestras opciones que desea realizar')

#se hace un respecttivo menu principal y de cada opcion



# Menu principal------------------------------------------------------------------------------------

def menu(con):
    salirPrincipal = False
    while not salirPrincipal:
        opPrincipal = input('''
                            MENU PRINCIPAL

                            1. Menu de Producto
                            2. Menu de Clientes
                            3. Menu de Productos constratados
                            4. Menus de transacciones
                            5. Salir

                            Seleccione un a opccion>>>: 

                            ''')
        if(opPrincipal == '1'):
            menuProductos(con)
        elif (opPrincipal == '2'):
            menuClinetes(con)
        elif (opPrincipal == '3'):
            menuProductosContratados(con)
        elif (opPrincipal == '4'):
            menuTransacciones(con)
        elif (opPrincipal == '5'):
            salirPrincipal = True
        else:
            print("Elija opcion válida.")

# Main------------------------------------------------------------------------------------

def main ():
    #se establece conexion con la base de datos
    Micon = conexionBD()
    crearTablas(Micon)
    menu(Micon)
    cerrarBD(Micon)

main()
