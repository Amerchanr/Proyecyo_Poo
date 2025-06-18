#aca se ejecutarean todas las funciones
#se importan las funciones y librerias necesarios
import sqlite3
from sqlite3 import Error
import clase_productos
from clase_productos import menuProductos
import clase_cliente
from clase_cliente import insertarCliente
from clase_cliente import leerCliente
from clase_cliente import actualizarDireccion
from clase_cliente import consultarInformacionCliente
from clase_cliente import menuClinetes
from clase_ProdAdqu import menuProductosContratados




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
        con=sqlite3.connect('basemibanco.db')
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

    salirProductosAdq=True
    salirTransacciones=True
    

    #se garantiza que el usuario ingrese un numero entero para la eleccion de la opcion
   
    opcionPrincipal=(input('''
                            Menu Principal

                            1)Menu productos
                            2)Menu Clientes
                            3)Menu de Administración de productos Contratados
                            4)menu de Transacciones
                            5)Salir
                            Seleccione una opcion >>>>:  '''))

    if (opcionPrincipal=='1'):

        menuProductos(micon)
        
                    
    if (opcionPrincipal=='2'):
        menuClinetes(micon)


       
    if (opcionPrincipal=='3'):
        #print('hola')
        menuProductosContratados(micon)
        
    if (opcionPrincipal=='4'):
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
    if (opcionPrincipal=='5'):
        cerrarDB(micon)
        Salirprincipal=False
            
            
            
    else:
        print('Elija una opcion valida')
        





