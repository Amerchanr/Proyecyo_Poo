import sqlite3
from sqlite3 import Error
from lectura_datos import *
from clase_productos import *



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


class concafecha:
    def __init__(self):
        self.__dia=None
        self.__mes=None
        self.__año=None
    def setFech(self,dia,mes,año): 
        self.__dia=input('ingrese el dia en formato DD')
        self.__mes=input('ingrese el mes en formato MM')
        self.__año=input('ingrese el año en formato AAAA')
    def getFech(self):
        
        return f"{self.__dia}/{self.__mes}/{self.__año}"


#Productos existente ------------------------------------------------------------------------------------------------------------------------------------------------------

class ProductosAdquiridos(concafecha,Lectura_datos,Productos):
    # Funcion de consulta d eproducto 
    def consultarProductosExistentes(self,con):
        
        idCuentaCredito=str(leer_entero('ingrese el numero de cuenta del producto adquirido'))
        
        #creamos el objeto para recorrer la base de datos
        cursorObj=con.cursor()
        #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
        cad="SELECT idCuentaCredito,idProducto,idCliente,capitalInicial,plazoMeses,fechaEntrega,saldoCapital,sumatoriaInteresesPagados,plazoPendiente FROM ProductosContratados WHERE idCuentaCredito="+idCuentaCredito
        #ejecutamos la cadena con el metodo execute del objeto cursorObj
        cursorObj.execute(cad)
        filas=cursorObj.fetchall()
        if filas==[]:
            print('el Id del producto consultado no existe')
        for row in filas:
            idcuenta=row[0]
            idprodu=row[1]
            idcliente=row[2]
            capinit=row[3]
            plazoM=row[4]
            fechaEnt=row[5]
            saldocap=row[6]
            sumintpag=row[7]
            plazopend=row[8]
            print("idCuentaCredito: ",idcuenta,"\nidProducto: ",idprodu,"\nidCliente: ",idcliente,"\ncapitalInicial : ",capinit,"\nplazoMeses : ",plazoM,"\nfechaEntrega : ",fechaEnt,"\nsaldoCapital : ",saldocap,"\nsumatoriaInteresesPagados : ",sumintpag,"\nplazoPendiente : ",plazopend)

    # Funcion de consulta para que el producto sea verificado si esta o no esta 

    def leerProductoContratado(self,con):
        cursor = con.cursor()
        print('Las opciones de productos que podemos ofrecer son')
        consultarProducto1(con)
        # Leer ID del producto
        
        idProducto = leer_entero("Número de producto a contratar: ")
        
        cursor.execute("SELECT tipoProducto, remuneracion FROM Productos WHERE noIdProducto=?", (idProducto,))
        row = cursor.fetchone()
        if not row:
            print(" Producto no encontrado.")
            return

        tipo = int(row[0])
        interes = float(row[1])
        tipoTexto = "CRÉDITO" if tipo == 1 else "AHORROS"
        print(f"Tipo de producto detectado: {tipoTexto}")

        # Leer ID del cliente y verificar existencia
        idCliente = input("ID del cliente: ")
        cursor.execute("SELECT * FROM Clientes WHERE noIdCliente=?", (idCliente,))
        cliente = cursor.fetchone()
        if not cliente:
            print(" Cliente no registrado. Debe crear el cliente primero.")
            return

        # Continuar con el registro según tipo
        try:
            if tipo == 1:
                capital = float(input("Capital inicial: "))
                plazo = int(input("Plazo en meses: "))
                fecha = concafecha()
                fecha.setFech()
                saldo = capital
                plazoPendiente = plazo
            else:
                capital=int(0)
                while capital<100000:
                    
                    print('el monto minimo inicial de ahorro es de 100000')
                    capital = float(input("Monto inicial de ahorro: "))
                
                plazo = 0
                
                fecha = concafecha()
                saldo = capital
                plazoPendiente = 0
        except ValueError:
            print(" Error: valores inválidos en capital o plazo.")
            return

        # Insertar en base de datos y obtener ID generado
        cursor.execute('''
            INSERT INTO ProductosContratados
            (idProducto, idCliente, capitalInicial, plazoMeses, fechaEntrega, saldoCapital, sumatoriaInteresesPagados, plazoPendiente)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (idProducto, idCliente, capital, plazo, fecha, saldo, 0, plazoPendiente))
        con.commit()
        idCuenta = cursor.lastrowid

        print(" Producto contratado registrado correctamente.")
        print(f" Su número de cuenta u obligación es: {idCuenta}")


    #Menu del producto adquirido
    def MenuAdquirirProducto(self,con):
        salirProductosContratados = False
        while not salirProductosContratados:
            opPrincipal = input('''
                                MENU Aquirir un Producto

                                1. Ya soy cliente
                                2. No soy cliente
                                3. Volver a  menú Productos Adquiridos
                                

                                Seleccione un a opccion>>>: 

                                ''')
            if(opPrincipal == '1'):
                leerProductoContratado(con)
            elif (opPrincipal == '2'):
                cliente=leerCliente1()
                insertarCliente1(con,cliente)
                leerProductoContratado(con)
            elif (opPrincipal == '3'):
                salirProductosContratados = True
            else:
                print("Opción no válida.")


    # Se proporciona las definiciones de los catos de cliente
    def leerCliente1(self):
        noIdCliente = leer_entero("ID cliente (número): ")
        nombre = leer_texto("Nombre: ")
        apellido = leer_texto("Apellido: ")
        direccion = leer_no_vacio("Dirección: ")
        telefono = leer_entero("Teléfono (número): ")
        correo = leer_correo("Correo: ")
        return noIdCliente, nombre, apellido, direccion, str(telefono), correo
    def insertarCliente1(self,con, cliente):
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO Clientes VALUES (?, ?, ?, ?, ?, ?)", cliente)
            con.commit()
            print("Cliente creado correctamente.")
        #esta ecepcion me permite que si hay un cliente que escriba un id ya existente , no lo permita
        #y el programa no seje de funcionar, en cambio le anuncie al cliente que  el id ya existe
        except sqlite3.IntegrityError:
            print("Ya existe un cliente con ese ID.")

    #Menu productos  

    def menuProductosContratados(self,con):
        salirProductosContratados = False
        while not salirProductosContratados:
            opPrincipal = input('''
                                MENU Productos Adquiridos 

                                1. Aquirir un Producto 
                                2. Consultar productos existentes
                                3. Volver a  menú Principal
                                

                                Seleccione un a opccion>>>: 

                                ''')
            if(opPrincipal == '1'):
                MenuAdquirirProducto(con)
            elif (opPrincipal == '2'):
                consultarProductosExistentes(con)

            elif (opPrincipal == '3'):
                salirProductosContratados = True
            else:
                print("Opción no válida.")
    def BorrarProducto(self,con):
        NoIdProducto=input("Codigo del producto:")
        #creamos el objeto para recorrer la base de datos
        cursorObj=con.cursor()
        #CREAMOS LA CADENA CON EL SQL QUE QUEREMOS EJECUTAR
        cad="DELETE FROM ProductosContratados  WHERE idCuentaCredito="+NoIdProducto
        #ejecutamos la cadena con el metodo execute del objeto cursorObj
        cursorObj.execute(cad)
        #aseguramos la persistencia con un commit
        con.commit()

    

                

