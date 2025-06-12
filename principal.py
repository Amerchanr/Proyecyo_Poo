#aca se ejecutarean todas las funciones
#se importan las funciones y librerias necesarios
import sqlite3
from sqlite3 import Error
import clase_productos
from clase_productos import insertarNuevoProducto1
from clase_productos import leerProducto
from clase_productos import consultaProducto


#se crea variable global para ejecutar y poder salir del bucle del menu  principal y menus adicionales  
Salirprincipal=True
salirProductos=True
salirClietes=True
salirProductosAdq=True
salirTransacciones=True

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


print('bienvenido a su banca Virtual\nPara continuar escriba el numero de una de nuestras opciones que desea realizar')

#se hace un respecttivo menu principal y de cada opcion
while Salirprincipal==True:
#se vuelven a llamar las variables globales con el fin
#de que si el usuario entra a na opcion y vuelve a salir
#pueda volver a entrar a la opcion
    salirProductos=True
    salirClietes=True
    salirProductosAdq=True
    salirTransacciones=True
    

    #se garantiza que el usuario ingrese un numero entero para la eleccion de la opcion
    try:
        opcionPrincipal=int(input('''
                                Menu Principal

                                1)Menu productos
                                2)Menu Clientes
                                3)Menu de Administración de productos Contratados
                                4)menu de Transacciones
                                5)Salir
                                Seleccione una opcion >>>>:  '''))
    
    except ValueError:
        print('debe ingresar un numero')



    if (opcionPrincipal==1):
        while salirProductos==True:
            try:                    
                opcionProductos=int(input('''
                                                Menu Productos
                                                1)Crear Nuevo Producto
                                                2)Consuultar Producto
                                                3)Volver al menu Principal
                                                Seleccione una opcion >>>>:  '''))
            except ValueError:
                print('debe ingresar un numero')
            if (opcionProductos==1):
                miNuevoProducto=leerProducto()
                insertarNuevoProducto1(micon,miNuevoProducto)
            elif(opcionProductos==2):
                consultaProducto(micon)
            elif(opcionProductos==3):
                salirProductos=False
                    
    if (opcionPrincipal==2):
        while salirClietes==True:
            try:                    
                opcionClientes=int(input('''
                                                Menu Productos
                                                1)Crear Nuevo Cliente
                                                2)Actualizar Direccion de Cliente
                                                3)Consultar Informacion Vigente
                                                4)Volver al menu Principal
                                                Seleccione una opcion >>>>:  '''))
            except ValueError:
                print('debe ingresar un numero')
            if (opcionClientes==1):
                print('ingresar cliente')
            elif(opcionClientes==2):
                print('Actualizar direccion')
            elif(opcionClientes==3):
                print('Consultar Informacion vigente')
            elif(opcionClientes==4):
                salirClietes=False
    if (opcionPrincipal==3):
        while salirProductosAdq==True:
            try:                    
                opcionProductosAdq=int(input('''
                                                Menu Productos Adquirido
                                                1)Aquirir un Nuevo Producto
                                                2)Consultar Producto Adquirido
                                                3)Volver al menu Principal
                                                Seleccione una opcion >>>>:  '''))
            except ValueError:
                print('debe ingresar un numero')
            if (opcionProductosAdq==1):
                print('Aquirir un Nuevo Producto')
            elif(opcionProductosAdq==2):
                print('Consultar Producto Adquirido')
            elif(opcionProductosAdq==3):
                salirProductosAdq=False
    if (opcionPrincipal==4):
        while salirTransacciones==True:
            try:                    
                opcionClientes=int(input('''
                                                Menu Transaccones
                                                1)Pagar Cuota 
                                                2)opcion 2
                                                3)opcion 3
                                                4)opcion 4 
                                                5)Volver al menu Principal
                                                Seleccione una opcion >>>>:  '''))
            except ValueError:
                print('Pagar Cuota ')
            if (opcionClientes==1):
                print('ingresar cliente')
            elif(opcionClientes==2):
                print('Actualizar direccion')
            elif(opcionClientes==3):
                print('Consultar Informacion vigente')
            elif(opcionClientes==4):
                print('Consultar Informacion vigente')
            elif(opcionClientes==5):
                salirTransacciones=False
    if (opcionPrincipal==5):
        Salirprincipal=False
            
            
            
    else:
        print('ingrese un numero')
        





