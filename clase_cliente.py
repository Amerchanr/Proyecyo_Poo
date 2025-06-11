
import sqlite3
from sqlite3 import Error

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


def crearTablaClientes(con):
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
    cad='''CREATE TABLE IF NOT EXISTS CLIENTES (NoIdentificacion integer NOT NULL,
                                        Nombre txt NOT NULL,
                                        Apellidoo txt NOT NULL,
                                        Direccion txt NOT NULL,
                                        telefono integer NOT NULL,
                                        correoElectronico txt NOT NULL) '''
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute(cad)
    #aseguramos la persistencia con un commit
    con.commit()

    
def crearTablaClientes1(con):
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute('''CREATE TABLE IF NOT EXISTS CLIENTES (
                                        NoIdentificacion integer NOT NULL,
                                        Nombre txt NOT NULL,
                                        Apellidoo txt NOT NULL,
                                        Direccion txt NOT NULL,
                                        telefono integer NOT NULL,
                                        correoElectronico txt NOT NULL) ''')
    #aseguramos la persistencia con un commit
    con.commit()


    
    
def insertarNuevoProducto1(con,miproducto):
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
    cad='''INSERT INTO CLIENTES VALUES(?,?,?,?,?,?                                       
                                        )'''
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute(cad,miproducto)
    #aseguramos la persistencia con un commit
    con.commit()
    
    
def leerProducto():
    NoIdentificacion=input("INGRESE SU NUMERO DE IDENTIFICAACION:")
    Nombre=input("INGRESE SU NOMBRE")
    Apellidoo=input("INGRESE SU APELLIDO")
    Direccion=input("INGRESE SU DIRECCION")
    telefono=input("INGRESE SU TELEFONO")
    correoElectronico=input("INGRESE SU CORREO ELECTRONICO")
    producto=(NoIdentificacion,Nombre,Apellidoo,Direccion,telefono,correoElectronico)
    
    print("la tupla es:",producto)
    return producto


def main():
    micon=conexionBD()
    #crearTablaClientes(micon))
    MiprodCreado=leerProducto()
    insertarNuevoProducto1(micon,MiprodCreado)
    cerrarDB(micon)

        
def borrar_tabla(con):
    cursorObj=con.cursor()
    cad="DROP TABLE IF EXISTS CLIENTES"
    cursorObj.execute(cad)
    print("Tabla borrada exitosamente")
micon=conexionBD()

borrar_tabla(micon)
