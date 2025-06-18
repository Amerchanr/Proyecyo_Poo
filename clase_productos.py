##ejemplo estructurado
import sqlite3
from sqlite3 import Error


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


def consultaProducto(con):
    NoIdProducto=input("Codigo del producto que desea consultar:")
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
    cad="SELECT NoIdProducto,NombreProducto,TipoProducto,Remuneracion FROM PRODUCTOS WHERE NoIdProducto="+NoIdProducto
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute(cad)
    filas=cursorObj.fetchall()
    for row in filas:
        id1=row[0]
        tipo=row[2]
        nombre=row[1]
        remuneracion=row[3]
        print("NoIdProducto: ",id1,"\nNombreProducto: ",nombre,"\nTipoProducto: ",tipo,"\nRemuneracion: ",remuneracion)
def consultarProducto1(con):
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
    cad="SELECT * FROM PRODUCTOS"
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute(cad)
    filas=cursorObj.fetchall()
    for row in filas:
        id1=row[0]
        tipo=row[2]
        nombre=row[1]
        print("el ide del producto es:" ,id1)
        print("el nombre del producto es:" ,nombre)


    
def insertarNuevoProducto1(con,miproducto):
    #garantizamos que si el usuario ingresa un NoIdProducto o NombreProducto
    #que ya se encuentre en la base de datos no se detenga el programa
    try:
        #creamos el objeto para recorrer la base de datos
        cursorObj=con.cursor()
        #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
        cad='''INSERT INTO PRODUCTOS VALUES(?,?,?,?                                       
                                        )'''
        #ejecutamos la cadena con el metodo execute del objeto cursorObj
        cursorObj.execute(cad,miproducto)
        #aseguramos la persistencia con un commit
        con.commit()
    except sqlite3.IntegrityError:
        print("Ya existe un producto con ese ID. o Nombre No se puede duplicar.")
    
    
def leerProducto():
    #Garantizamos que el usuario ingrese el tipo de dato que necesitamos
    while True:
        try:
            NoIdProducto=int(input("Ingrese el Codigo del producto en formato numerico:"))
            break
        except ValueError:
            print('El ID del producto debe ser un numero entero')
            
    NombreProducto=str(input("Ingrese el nombre del producto"))

    TipoProducto=int(input("tipo producto 1 para credito 2 para Cuenta de Ahorro"))
    
    if TipoProducto==1:
        print('ha elegido credito')
    elif TipoProducto==2:
        print('ha elegido cuenta de ahorro')
    while TipoProducto not in [1,2]:
        print('seleccione 1 o 2 dependiendo el tipo de producto')
        TipoProducto=int(input("tipo producto 1 para credito 2 para Cuenta de Ahorro"))
        if TipoProducto==1:
            print('ha elegido credito')
        elif TipoProducto==2:
            print('ha elegido cuenta de ahorro')

    while True:
        try:
            Remuneracion=float(input("Ingrese la tasa de interes en formato numerico"))
            break
        except ValueError:
            print('El valor de la remuneracion del producto debe ser un numerico ')
    producto=(NoIdProducto,NombreProducto,TipoProducto,Remuneracion)
    print("la datos ingresados es:",producto)
    return producto
def borrar_tabla(con):
    cursorObj=con.cursor()
    cad="DROP TABLE IF EXISTS PRODUCTOS"
    cursorObj.execute(cad)
    print("Tabla borrada exitosamente")

    
def menuProductos(con):
#se vuelven a llamar las variables que permite salir con el fin
#de que si el usuario entra a na opcion y vuelve a salir
#pueda volver a entrar a la opcion
    salirProductos=True
    while salirProductos==True:
                            
        opcionProductos=(input('''
                                        Menu Productos
                                        1)Crear Nuevo Producto
                                        2)Consuultar Producto
                                        3)Volver al menu Principal
                                        Seleccione una opcion >>>>:  '''))
            
        if (opcionProductos=='1'):
            miNuevoProducto=leerProducto()
            insertarNuevoProducto1(con,miNuevoProducto)
        elif(opcionProductos=='2'):
            consultaProducto(con)
        elif(opcionProductos=='3'):
            salirProductos=False
        else:
            print('Ingrese una opcion valida')            
    

#micon=conexionBD()
#consultarProducto1(micon)
#menuProductos(micon)
#borrar_tabla(micon)
#cerrarDB(micon)
#crearTablaProductos1(micon)
