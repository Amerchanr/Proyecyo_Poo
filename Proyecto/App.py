import sqlite3
from sqlite3 import Error
from datetime import datetime
from abc import ABC, abstractmethod

# ==================== UTILIDADES ====================
# Funciones auxiliares para validación de entrada y manejo de errores
def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto and texto.replace(" ", "").isalpha():
            return texto
        print("Error: Solo letras y espacios permitidos.")

def leer_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Error: No puede estar vacío.")

def leer_correo(mensaje):
    while True:
        correo = input(mensaje).strip()
        partes = correo.split("@")
        if len(partes) == 2 and "." in partes[1]:
            return correo
        print("Error: Correo inválido.")
def leee_num(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número.")
def concafecha(mensaje):
    print(mensaje)
    dia=input('ingrese el dia en formato DD')
    mes=input('ingrese el mes en formato MM')
    año=input('ingrese el año en formato AAAA')
    fechacon=(dia+'/'+mes+'/'+año)
    fech=datetime.strptime(fechacon, '%d/%m/%Y')
    return fech

# ==================== CONEXIÓN Y TABLAS ====================
# Conexión a la base de datos SQLite
def conexion_bd(ruta='basemibanco.db'):
    try:
        con = sqlite3.connect(ruta)
        print("Conexión exitosa.")
        return con
    except Error as e:
        print("Error de conexión:", e)
        return None


# Cierre de conexión
def cerrar_bd(con):
    if con:
        con.close()
        print("Conexión cerrada.")

# Crear Todas  las tablas si no existen
def crear_tablas(con):
    script = '''
    CREATE TABLE IF NOT EXISTS PRODUCTOS (
        NoIdProducto INTEGER PRIMARY KEY,
        NombreProducto TEXT NOT NULL UNIQUE,
        TipoProducto INTEGER NOT NULL CHECK(TipoProducto IN (1,2)),
        Remuneracion REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS CLIENTES (
        noIdCliente INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        direccion TEXT,
        telefono INTEGER,
        correo TEXT
    );

    CREATE TABLE IF NOT EXISTS PRODUCTOSCONTRATADOS (
        idCuentaCredito INTEGER PRIMARY KEY AUTOINCREMENT,
        idProducto INTEGER NOT NULL,
        idCliente INTEGER NOT NULL,
        capitalInicial REAL NOT NULL,
        plazoMeses INTEGER NOT NULL,
        fechaEntrega TEXT NOT NULL,
        saldoCapital REAL NOT NULL,
        sumatoriaInteresesPagados REAL DEFAULT 0,
        plazoPendiente INTEGER NOT NULL,
        FOREIGN KEY(idProducto) REFERENCES PRODUCTOS(NoIdProducto),
        FOREIGN KEY(idCliente) REFERENCES CLIENTES(noIdCliente)
    );

    CREATE TABLE IF NOT EXISTS TRANSACCIONES (
        idTransaccion INTEGER PRIMARY KEY AUTOINCREMENT,
        idCuentaCredito INTEGER NOT NULL,
        fechaPago TEXT NOT NULL,
        valorPagado REAL NOT NULL,
        FOREIGN KEY(idCuentaCredito) REFERENCES PRODUCTOSCONTRATADOS(idCuentaCredito)
    );
    '''
    con.executescript(script)
    con.commit()
    print("Tablas creadas/verificadas.")

# ==================== CLASES ====================
# Clase para manejar productos del banco
class Producto:
    def __init__(self, con): self.con = con

    def leer(self):
        # Recolecta los datos del producto desde consola
        #id_prod recolescta el ID del producto y garantiza que sea un entero
        id_prod = leer_entero("Código producto: ")
        nombre = leer_no_vacio("Nombre producto: ")
        tipo = None
        #se garantiza que como tipo de producto solo se pueda ingresar 1 o 2
        while tipo not in (1, 2):
            tipo = leer_entero("Tipo (1=Crédito, 2=Ahorros): ")
        #leee_num permite ingresar un número flotante para la tasa de interés
        #y garantiza que sea un número válido
        remuneracion = leee_num('Tasa de Interes (%): ')
        return id_prod, nombre, tipo, remuneracion

    def insertar(self):
        # Inserta un nuevo producto en la tabla
        datos = self.leer()
        try:
            # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
            c = self.con.cursor()
            #ejecutamos la cadena con el metodo execute 

            c.execute(
                "INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?)", datos
            )
            #Garantizamos Persistencia de los datos con commit
            self.con.commit()
            print("Producto agregado.")
        # Capturamos la excepción de integridad para manejar duplicados
        except sqlite3.IntegrityError:
            print("Error: Producto ya existe.")

    def consultar(self):
        # Consulta un producto por ID
        # Se solicita el ID del producto a consultar con la variable idp
        idp = leer_entero("Código producto a consultar: ")
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
        c = self.con.cursor()
        #ejecutamos la cadena con el metodo execute 
        c.execute("SELECT * FROM PRODUCTOS WHERE NoIdProducto=?", (idp,))
        # Se obtiene el resultado de la consulta con fetchone
        #y se almacena en la variable fila
        fila = c.fetchone()
        # Si se encuentra el producto, se imprime su información
        #de lo contrario se indica que no fue encontrado
        if fila:
            tipo = 'Crédito' if fila[2]==1 else 'Ahorros'
            print(f"ID:{fila[0]} Nombre:{fila[1]} Tipo:{tipo} Remun:{fila[3]}%")
        else:
            print("No encontrado.")

    def listar(self):
        # Lista todos los productos
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c 
        # y se ejecuta la consulta para obtener todos los productos
        c = self.con.cursor(); c.execute("SELECT * FROM PRODUCTOS")
        for idp,nm,tp,rem in c.fetchall():
            t = 'Crédito' if tp==1 else 'Ahorros'
            print(f"{idp}: {nm} ({t}) - {rem}%")

# Clase para gestionar los clientes
class Cliente:
    def __init__(self, con): self.con = con

    def leer(self):
        # Solicita información del cliente
        return (
            leer_entero("ID cliente: "),
            leer_texto("Nombre: "),
            leer_texto("Apellido: "),
            leer_no_vacio("Dirección: "),
            leer_entero("Teléfono: "),
            leer_correo("Correo: ")
        )

        # Inserta cliente en la base de datos

    def insertar(self):
        # Recolecta los datos del cliente y se almacena en la variable datos
        datos = self.leer()
        try:
            # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
            c = self.con.cursor()
            #ejecutamos la cadena con el metodo execute
            c.execute("INSERT INTO CLIENTES VALUES (?,?,?,?,?,?)", datos)
            self.con.commit()
            print("Cliente registrado.")
        except sqlite3.IntegrityError:
            print("Error: Cliente ya existe.")

    def actualizar_direccion(self):
        # Permite actualizar la dirección del cliente
        # Se solicita el ID del cliente(idc) y la nueva dirección(nd)
        idc = leer_entero("ID cliente: ")
        nd = leer_no_vacio("Nueva dirección: ")
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
        c = self.con.cursor()
        #se ejecuta el cursor con el metodo execute y se uticiza UPDATE para modificar la dirección
        c.execute("UPDATE CLIENTES SET direccion=? WHERE noIdCliente=?", (nd,idc))
        self.con.commit(); print("Dirección actualizada.")

    def consultar(self):
        # Consulta cliente por ID
        # Se solicita el ID del cliente a consultar con la variable idc
        idc = leer_entero("ID cliente a consultar: ")
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
        c = self.con.cursor(); c.execute("SELECT * FROM CLIENTES WHERE noIdCliente=?",(idc,))
        # Se obtiene el resultado de la consulta con fetchone
        f = c.fetchone()
        # Si se encuentra el cliente, se imprime su información
        #de lo contrario se indica que no fue encontrado
        if f: print(f"{f[0]}: {f[1]} {f[2]} | {f[3]} | Tel:{f[4]} | {f[5]}")
        else: print("No encontrado.")

# Clase para adquirir productos
class ProductoAdquirido:
    #
    def __init__(self, con):
        self.con = con
        # Inicializa las instancias de Cliente y Producto para manejar sus funcionalidades
        self.cli = Cliente(con)
        self.prod = Producto(con)

    def adquirir(self):
        # Contratación de productos (créditos o ahorros)
        print("-- Productos --")
        # Se llama al método listar de la clase Producto para mostrar los productos disponibles
        self.prod.listar()
        # Se solicita el ID del producto a adquirir con la variable idp
        idp = leer_entero("ID producto: ")
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
        c = self.con.cursor()
        #se ejecuta el cursor con el metodo execute y se verifica si el producto existe
        c.execute("SELECT TipoProducto,Remuneracion FROM PRODUCTOS WHERE NoIdProducto=?",(idp,))
        row = c.fetchone()
        # Si el producto no existe, se imprime un mensaje y se retorna
        if not row: print("No existe."); return
        # Si el producto existe, se extraen el tipo y la remuneración
        #y se almacena en las variables tipo y rem
        tipo,rem = row
        #se le pide al usuario el ID del cliente, se guarda en la variable idc
        #  y se verifica si existe
        idc = leer_entero("ID cliente: ")

        c.execute("SELECT 1 FROM CLIENTES WHERE noIdCliente=?",(idc,))
        # Si el cliente no existe, se imprime un mensaje y se retorna
        if not c.fetchone(): print("Cliente no existe."); return
        #Si el producto elejido es de tipo crédito, se solicita el capital inicial y el plazo en meses
        #y se inicializan las variables para saldo(sal) y plazo de pago(pen)
        if tipo==1:
            cap=float(input("Capital inicial: "))
            pl=leer_entero("Plazo meses: ")
            sal=cap; pen=pl
        else:
            # Si el producto es de tipo ahorro, se solicita el capital inicial
            # y se inicializa el saldo con el mismo valor, y plazo pendiente a 0
            cap=float(input("Ahorro inicial (>=100000): "))
            sal=cap; pen=0
        #se le pide al usuario la fecha de entrega del producto
        #y se almacena en la variable fec
        fec=concafecha('ingrese la fecha de entrega de acuerdoa como se le indica')
        # se ejecuta el cursor con el metodo execute y se inserta el producto contratado
        #en la tabla PRODUCTOSCONTRATADOS con los datos recolectados
        c.execute(
            "INSERT INTO PRODUCTOSCONTRATADOS(idProducto,idCliente,capitalInicial,plazoMeses,fechaEntrega,saldoCapital,sumatoriaInteresesPagados,plazoPendiente) VALUES(?,?,?,?,?,?,?,?)",
            (idp,idc,cap,pen,fec,sal,0,pen)
        )
        self.con.commit(); print(f"Cuenta:{c.lastrowid}")

    def consultar(self):
        # Consultar datos del producto adquirido
        # Se solicita el ID de la cuenta a consultar con la variable idc
        idc=leer_entero("Cuenta a consultar: ")
        # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
        #se ejecuta el cursor con el metodo execute y se verifica si la cuenta existe
        c=self.con.cursor(); c.execute("SELECT * FROM PRODUCTOSCONTRATADOS WHERE idCuentaCredito=?",(idc,))
        f=c.fetchone()
        # Si la cuenta no existe, se imprime no existe y se retorna
        print(f if f else "No existe.")

        
    def MenuAdquirirProducto(self):
        # Menú para adquirir productos
        # Se inicializa la variable salirProductosContratados como False para podeer salir del bucle
        salirProductosContratados = False
        while not salirProductosContratados:
            opPrincipal = input('''
                                MENU Aquirir un Producto

                                1. Ya soy cliente
                                2. No soy cliente
                                3. Volver a  menú Productos Adquiridos
                                

                                Seleccione un a opccion>>>:
                ''')
            # Dependiendo de la opción seleccionada, se ejecuta una acción
            # Si el usuario ya es cliente, se llama al método adquirir
            if(opPrincipal == '1'):
                self.adquirir()
            # Si el usuario no es cliente, se llama al método insertar de Cliente
            # y luego se llama al método adquirir para contratar el producto
            elif (opPrincipal == '2'):
                self.cli.insertar()
                self.adquirir()
                #si el usuario dijita tres, sale del menu
            elif (opPrincipal == '3'):
                salirProductosContratados = True
            else:
                print("Opción no válida.")

# Clase para realizar transacciones
class Transacciones:
    def __init__(self, con): self.con = con
# Obtiene el tipo de producto (crédito o ahorro) de una cuenta
    # Se crea un cursor para ejecutar la consulta este cursor lo denotamos como c
    def obtener_tipo(self, cuenta):
        c=self.con.cursor()
        c.execute(
            "SELECT P.TipoProducto FROM PRODUCTOSCONTRATADOS PC JOIN PRODUCTOS P ON PC.idProducto=P.NoIdProducto WHERE PC.idCuentaCredito=?",
            (cuenta,)
        )
        # Se obtiene el tipo de producto, 1 para crédito y 2 para ahorro
        r=c.fetchone(); return r[0] if r else None
    
    # Obtiene los datos de un crédito
    def datos_credito(self, cuenta):
        # Devuelve saldo, plazo pendiente y tasa de interés
        c=self.con.cursor()
        c.execute(
            "SELECT saldoCapital, plazoPendiente, P.Remuneracion FROM PRODUCTOSCONTRATADOS PC JOIN PRODUCTOS P ON PC.idProducto=P.NoIdProducto WHERE PC.idCuentaCredito=?",
            (cuenta,)
        )
        return c.fetchone()

    def datos_ahorro(self, cuenta):
        # Devuelve saldo y tasa de interés
        c=self.con.cursor()
        c.execute(
            "SELECT saldoCapital, P.Remuneracion FROM PRODUCTOSCONTRATADOS PC JOIN PRODUCTOS P ON PC.idProducto=P.NoIdProducto WHERE PC.idCuentaCredito=?",
            (cuenta,)
        )
        return c.fetchone()

    def consultar_cuota(self):
        # Calcula la cuota mensual de un crédito
        # Se solicita el ID de la cuenta de crédito a consultar con la variable idc
        #y se verifica si es de tipo crédito
        idc=leer_entero("Cuenta crédito: ")
        if self.obtener_tipo(idc)!=1: print("No es crédito."); return
        # Se obtienen los datos del crédito con el método datos_credito
        datos=self.datos_credito(idc)
        # Si no hay datos o el plazo pendiente es menor o igual a 0, se imprime un mensaje y se retorna
        if not datos or datos[1]<=0: print("Sin cuota pendiente."); return
        sal,pen,rem=datos
        cap=sal/pen; inte=sal*(rem/100); tot=cap+inte
        print(f'''
                    === CUOTA A PAGAR ===
                    Capital: {cap:.2f}
                    Interés: {inte:.2f}
                    Total: {tot:.2f}
                    Plazo pendiente: {pen} meses
                    ======================''')

    def pagar_cuota(self):
        # Realiza el pago mensual de un crédito
        # Se solicita el ID de la cuenta de crédito a pagar con la variable idc
        idc=leer_entero("Cuenta crédito: ")
        #y se verifica si es de tipo crédito
        # Si no es de tipo crédito, se imprime un Noes Credito y se retorna
        if self.obtener_tipo(idc)!=1: print("No es crédito."); return
        # Se obtienen los datos del crédito con el método datos_credito
        d=self.datos_credito(idc)
        # Si no hay datos o el plazo pendiente es menor o igual a 0, se imprime 
        # credito pagado y se retorna
        if not d or d[1]<=0: print("Crédito pagado."); return
        # Se extraen el saldo, plazo pendiente y tasa de interés de los datos
        #y se almacenan en las variables sal, pen y rem respectivamente
        sal,pen,rem=d
        #se le pide al usuario la fecha de pago con la variable fec
        fec=fecha=concafecha('ingrese la fecha de pago de acuerdoa como se le indica')
        # Se obtiene el mes de la fecha de pago y se verifica si ya hay transacciones
        mes = fec.strftime('%Y-%m')  

        c=self.con.cursor()
        #se ejecuta el cursor con el metodo execute y se verifica si ya se pagó este mes
        c.execute("SELECT COUNT(*) FROM TRANSACCIONES WHERE idCuentaCredito=? AND substr(fechaPago,1,7)=?",(idc,mes))
        # Si ya se pagó este mes, se imprime ya pago este mes y se retorna
         #de lo contrario se calcula la cuota a pagar   
        if c.fetchone()[0]>0: print("Ya pagó este mes."); return
        # Se calcula la cuota a pagar
        # Se calcula el capital a pagar, el interés y se imprime la cuota
        cap=sal/pen; inte=sal*(rem/100)
        print(f"Cuota: Capapital {cap:.2f} Intereses {inte:.2f} Total {cap+inte:.2f}")
        # Se solicita el valor a pagar con la variable val
        val=float(input("Valor a pagar: "))

        nuevo_sal=max(0,sal-(val-inte)); nuevo_pen=max(0,pen-1)
        # Se inserta la transacción en la tabla TRANSACCIONES
        c.execute("INSERT INTO TRANSACCIONES VALUES(NULL,?,?,?)",(idc,fec,val))
        #se optiene el ID de la transacción recién insertada
        #y se almacena en la variable id_transaccion
        id_transaccion = c.lastrowid
        #y se actualiza el saldo y plazo pendiente en PRODUCTOSCONTRATADOS
        c.execute("UPDATE PRODUCTOSCONTRATADOS SET saldoCapital=?,plazoPendiente=?,sumatoriaInteresesPagados=sumatoriaInteresesPagados+? WHERE idCuentaCredito=?",
                  (nuevo_sal,nuevo_pen,inte,idc))
        self.con.commit()
        c.execute("SELECT idCliente FROM PRODUCTOSCONTRATADOS WHERE idCuentaCredito = ?", (idc,)) 
        tup = c.fetchone()
        idclientec = tup[0]
        c.execute("SELECT nombre, apellido FROM CLIENTES WHERE noIdCliente = ?", (idclientec,)) 
        row = c.fetchone()
        name = row[0]
        lastname = row[1]

        print(f'''
    ====== FACTURA DE PAGO CRÉDITO ======
                 ENCABEZADO 
    Factura Número: {id_transaccion}
    Nombre Cliente: {name}
    Apellido Cliente: {lastname}

    Valor pagado: {val:.2f}

    ====== PIE DE LA FACTURA ======
    Saldo restante: {nuevo_sal:.2f}
    Plazo pendiente: {nuevo_pen} meses
    Gracias por su pago.
    =====================================''')

    def consultar_saldo_ahorros(self):
        # Muestra el saldo actual y proyectado de una cuenta de ahorros
        # Se solicita el ID de la cuenta de ahorros a consultar con la variable idc
        idc=leer_entero("Cuenta ahorros: ")
        #y se verifica si es de tipo ahorro
        # Si no es de tipo ahorro, se imprime No es ahorro y se retorna
        if self.obtener_tipo(idc)!=2: print("No es ahorro."); return
        # Se obtienen los datos de la cuenta de ahorros con el método datos_ahorro
        #y se almacenan en la variable d
        d=self.datos_ahorro(idc)
        # Si no hay datos, se imprime No existe y se retorna
        if not d: print("No existe."); return
        # Se extraen el saldo y la tasa de interés de los datos
        sal,rem=d; proj=sal*(1+rem/100)
        # Se imprime el saldo actual, la tasa de interés y el saldo proyectado
        print(f"Saldo:{sal:.2f} Rem:{rem}% Proy:{proj:.2f}")

    def transaccion_ahorros(self):
        # Consignación o retiro de una cuenta de ahorros
        # Se solicita el ID de la cuenta de ahorros a consultar con la variable idc
        idc=leer_entero("Cuenta ahorros: ")
        #y se verifica si es de tipo ahorro
        # Si no es de tipo ahorro, se imprime No es ahorro y se retorna
        if self.obtener_tipo(idc)!=2: print("No es ahorro."); return
        d=self.datos_ahorro(idc)
        if not d: print("No existe."); return
        # Se extraen el saldo actual de la cuenta y se almacena en la variable sal
        sal,_=d; print(f"Saldo actual:{sal:.2f}")
        fec=input("Fecha(YYYY-MM-DD): ").strip()[:10]
        val=float(input("Valor(+/-): "))
        nuevo=sal+val
        c=self.con.cursor()
        c.execute("INSERT INTO TRANSACCIONES VALUES(NULL,?,?,?)",(idc,fec,val))
        id_transaccion = c.lastrowid
        c.execute("UPDATE PRODUCTOSCONTRATADOS SET saldoCapital=? WHERE idCuentaCredito=?",(nuevo,idc))
        self.con.commit()
        c.execute("SELECT idCliente FROM PRODUCTOSCONTRATADOS WHERE idCuentaCredito = ?", (idc,)) 
        tup = c.fetchone()
        idclientec = tup[0]
        c.execute("SELECT nombre, apellido FROM CLIENTES WHERE noIdCliente = ?", (idclientec,)) 
        row = c.fetchone()
        name = row[0]
        lastname = row[1]


        print(f'''
    ====== FACTURA DE PAGO CRÉDITO ======
                 ENCABEZADO 
    Factura Número: {id_transaccion}
    Nombre Cliente: {name}
    Apellido Cliente: {lastname}

    ====== PIE DE LA FACTURA ======
    Nuevo Saldo {nuevo:.2f}
    Gracias por confiar en nosotros.
    =====================================''')

# ======= CLASE ABSTRACTA PARA EL MENÚ =======
# Interfaz para garantizar que clases que hereden implementen un menú
class BaseMenu(ABC):
    @abstractmethod
    def menu(self):
        pass

# ======= CLASE PRINCIPAL =======
# Orquesta todas las funcionalidades del sistema
class AppBanco(BaseMenu):
    def __init__(self, con):
        self._con = con
        self.prod = Producto(con)
        self.cli = Cliente(con)
        self.pad = ProductoAdquirido(con)
        self.trx = Transacciones(con)

    # Getter y Setter de la conexión
    @property
    def conexion(self):
        return self._con

    @conexion.setter
    def conexion(self, nueva_conexion):
        if nueva_conexion:
            self._con = nueva_conexion
        else:
            print("Conexión no válida.")

    # Menú principal
    def menu(self):
        opciones = {
            '1': self.menu_productos,
            '2': self.menu_product_Adqu,
            '3': self.menu_clientes,
            '4': self.menu_transacciones,
            '5': exit
        }
        while True:
            print("\n=== MENU PRINCIPAL ===\n1.Productos\n2.Contratar Producto\n3.Clientes\n4.Transacciones\n5.Salir")
            op = input("Opción: ")
            acciones = opciones.get(op)
            if acciones:
                acciones()
            else:
                print("Inválido.")

    def menu_productos(self):
        while True:
            print("\n-- Productos --\n1.Crear\n2.Consultar\n3.Listar\n4.Volver")
            op = input("Opción: ")
            if op == '1':
                self.prod.insertar()
            elif op == '2':
                self.prod.consultar()
            elif op == '3':
                self.prod.listar()
            elif op == '4':
                break
            else:
                print("Inválida.")
    def menu_product_Adqu(self):
        while True:
            print("\n-- Productos Adquiridos --\n1.Adquirir\n2.Consultar\n3.Volver")
            op = input("Opción: ")
            if op == '1':
                self.pad.MenuAdquirirProducto()
            elif op == '2':
                self.pad.consultar()
            elif op == '3':
                break
            else:
                print("Inválida.")

    def menu_clientes(self):
        while True:
            print("\n-- Clientes --\n1.Crear\n2.Actualizar Dirección\n3.Consultar\n4.Volver")
            op = input("Opción: ")
            if op == '1':
                self.cli.insertar()
                self.pad.adquirir()

            elif op == '2':
                self.cli.actualizar_direccion()
            elif op == '3':
                self.cli.consultar()
            elif op == '4':
                break
            else:
                print("Inválida.")

    def menu_transacciones(self):
        while True:
            print("\n-- Transacciones --\n1.Consultar Cuota\n2.Pagar Cuota\n3.Saldo Ahorros\n4.Transacción Ahorros\n5.Volver")
            op = input("Opción: ")
            if op == '1':
                self.trx.consultar_cuota()
            elif op == '2':
                self.trx.pagar_cuota()
            elif op == '3':
                self.trx.consultar_saldo_ahorros()
            elif op == '4':
                self.trx.transaccion_ahorros()
            elif op == '5':
                break
            else:
                print("Inválida.")

# ==================== EJECUCIÓN PRINCIPAL ====================
# Punto de entrada de la aplicación
def main():
    conexion = conexion_bd()
    if conexion:
        crear_tablas(conexion)
        AppBanco(conexion).menu()
        cerrar_bd(conexion)

if __name__ == "__main__":
    main()
