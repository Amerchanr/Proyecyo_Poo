#aca se ejecutarean todas las funciones
#se importan las funciones y librerias necesarios
import sqlite3
from sqlite3 import Error
import clase_productos
from clase_productos import insertarNuevoProducto1
from clase_productos import leerProducto
from clase_productos import consultaProducto

#Se inicializa variable opcion para el correcto manejo de errores y la ejecucion del menu
opcion= None

#creacion y conexion con la bas ede datos
def conexionBD():
    try:
        # se crea repositorio fisico-objeto de conexcion a la base de datos 
        con=sqlite3.connect('basebancopruebas.db')
        print('la conexion fue exitosa')
        return con
    except Error:
        print(Error)
#cierre conexion

def cerrarDB(con):
    con.close()

#se establece conexion con la base de datos
micon=conexionBD()

#se crea variable global para ejecutar y poder salir del bucle    
a=True

print('bienvenido a su banca Virtual\nPara continuar escriba el numero de una de nuestras opciones que desea realizar')

#se hace un respecttivo menu
while a==True:

        
    print('''1. Crear un nuevo producto
2. Consultar INfo de un respectivo Producto
3. Nuevo Cliente
4. Actualizar direccion de cliente
5. Consultar Info vigente del cliente
6.  ''')

    #s garantiza que el usuario ingrese un numero entero para la eleccion de la opcion
    try:
        opcion= int(input('ingrese el numero de la opcion deseada'))
    
    except ValueError:
        print('debe ingresar un numero')


    if opcion is not None:

        if (opcion==1):
            miNuevoProducto=leerProducto()
            insertarNuevoProducto1(micon,miNuevoProducto)
        elif(opcion==2):
            consultaProducto(micon)
    else:
        print('ingrese un numero')
        
    a=False





