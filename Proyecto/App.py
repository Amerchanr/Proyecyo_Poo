import sqlite3
from sqlite3 import Error
from datetime import datetime
from abc import ABC, abstractmethod

# ==================== UTILIDADES ====================
# Funciones auxiliares para validación de entrada
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

# Crear las tablas si no existen
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
        id_prod = leer_entero("Código producto: ")
        nombre = leer_no_vacio("Nombre producto: ")
        tipo = None
        while tipo not in (1, 2):
            tipo = leer_entero("Tipo (1=Crédito, 2=Ahorros): ")
        remuneracion = float(input("Tasa de interés (%): "))
        return id_prod, nombre, tipo, remuneracion

    def insertar(self):
        # Inserta un nuevo producto en la tabla
        datos = self.leer()
        try:
            c = self.con.cursor()
            c.execute(
                "INSERT INTO PRODUCTOS VALUES (?, ?, ?, ?)", datos
            )
            self.con.commit()
            print("Producto agregado.")
        except sqlite3.IntegrityError:
            print("Error: Producto ya existe.")

    def consultar(self):
        # Consulta un producto por ID
        idp = leer_entero("Código producto a consultar: ")
        c = self.con.cursor()
        c.execute("SELECT * FROM PRODUCTOS WHERE NoIdProducto=?", (idp,))
        fila = c.fetchone()
        if fila:
            tipo = 'Crédito' if fila[2]==1 else 'Ahorros'
            print(f"ID:{fila[0]} Nombre:{fila[1]} Tipo:{tipo} Remun:{fila[3]}%")
        else:
            print("No encontrado.")

    def listar(self):
        # Lista todos los productos
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

    def insertar(self):
        # Inserta cliente en la base de datos
        datos = self.leer()
        try:
            c = self.con.cursor()
            c.execute("INSERT INTO CLIENTES VALUES (?,?,?,?,?,?)", datos)
            self.con.commit()
            print("Cliente registrado.")
        except sqlite3.IntegrityError:
            print("Error: Cliente ya existe.")

    def actualizar_direccion(self):
        # Permite actualizar la dirección del cliente
        idc = leer_entero("ID cliente: ")
        nd = leer_no_vacio("Nueva dirección: ")
        c = self.con.cursor()
        c.execute("UPDATE CLIENTES SET direccion=? WHERE noIdCliente=?", (nd,idc))
        self.con.commit(); print("Dirección actualizada.")

    def consultar(self):
        # Consulta cliente por ID
        idc = leer_entero("ID cliente a consultar: ")
        c = self.con.cursor(); c.execute("SELECT * FROM CLIENTES WHERE noIdCliente=?",(idc,))
        f = c.fetchone()
        if f: print(f"{f[0]}: {f[1]} {f[2]} | {f[3]} | Tel:{f[4]} | {f[5]}")
        else: print("No encontrado.")

# Clase para adquirir productos
class ProductoAdquirido:
    def __init__(self, con):
        self.con = con
        self.cli = Cliente(con)
        self.prod = Producto(con)

    def adquirir(self):
        # Contratación de productos (créditos o ahorros)
        print("-- Productos --")
        self.prod.listar()
        idp = leer_entero("ID producto: ")
        c = self.con.cursor()
        c.execute("SELECT TipoProducto,Remuneracion FROM PRODUCTOS WHERE NoIdProducto=?",(idp,))
        row = c.fetchone()
        if not row: print("No existe."); return
        tipo,rem = row
        idc = leer_entero("ID cliente: ")
        c.execute("SELECT 1 FROM CLIENTES WHERE noIdCliente=?",(idc,))
        if not c.fetchone(): print("Cliente no existe."); return
        if tipo==1:
            cap=float(input("Capital inicial: "))
            pl=leer_entero("Plazo meses: ")
            sal=cap; pen=pl
        else:
            cap=float(input("Ahorro inicial (>=100000): "))
            sal=cap; pen=0
        fec=datetime.today().strftime('%Y-%m-%d')
        c.execute(
            "INSERT INTO PRODUCTOSCONTRATADOS(idProducto,idCliente,capitalInicial,plazoMeses,fechaEntrega,saldoCapital,sumatoriaInteresesPagados,plazoPendiente) VALUES(?,?,?,?,?,?,?,?)",
            (idp,idc,cap,pen,fec,sal,0,pen)
        )
        self.con.commit(); print(f"Cuenta:{c.lastrowid}")

    def consultar(self):
        # Consultar datos del producto adquirido
        idc=leer_entero("Cuenta a consultar: ")
        c=self.con.cursor(); c.execute("SELECT * FROM PRODUCTOSCONTRATADOS WHERE idCuentaCredito=?",(idc,))
        f=c.fetchone()
        print(f if f else "No existe.")

# Clase para realizar transacciones
class Transacciones:
    def __init__(self, con): self.con = con

    def obtener_tipo(self, cuenta):
        # Determina si la cuenta es de crédito o ahorros
        c=self.con.cursor()
        c.execute(
            "SELECT P.TipoProducto FROM PRODUCTOSCONTRATADOS PC JOIN PRODUCTOS P ON PC.idProducto=P.NoIdProducto WHERE PC.idCuentaCredito=?",
            (cuenta,)
        )
        r=c.fetchone(); return r[0] if r else None

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
        idc=leer_entero("Cuenta crédito: ")
        if self.obtener_tipo(idc)!=1: print("No es crédito."); return
        datos=self.datos_credito(idc)
        if not datos or datos[1]<=0: print("Sin cuota pendiente."); return
        sal,pen,rem=datos
        cap=sal/pen; inte=sal*(rem/100); tot=cap+inte
        print(f"Capital:{cap:.2f} Interés:{inte:.2f} Total:{tot:.2f} Pendiente:{pen} meses")

    def pagar_cuota(self):
        # Realiza el pago mensual de un crédito
        idc=leer_entero("Cuenta crédito: ")
        if self.obtener_tipo(idc)!=1: print("No es crédito."); return
        d=self.datos_credito(idc)
        if not d or d[1]<=0: print("Crédito pagado."); return
        sal,pen,rem=d
        fec=input("Fecha pago(YYYY-MM-DD): ").strip()[:10]
        mes=fec[:7]
        c=self.con.cursor()
        c.execute("SELECT COUNT(*) FROM TRANSACCIONES WHERE idCuentaCredito=? AND substr(fechaPago,1,7)=?",(idc,mes))
        if c.fetchone()[0]>0: print("Ya pagó este mes."); return
        cap=sal/pen; inte=sal*(rem/100)
        print(f"Cuota: Cap {cap:.2f} Int {inte:.2f} Tot {cap+inte:.2f}")
        val=float(input("Valor a pagar: "))
        nuevo_sal=max(0,sal-(val-inte)); nuevo_pen=max(0,pen-1)
        c.execute("INSERT INTO TRANSACCIONES VALUES(NULL,?,?,?)",(idc,fec,val))
        c.execute("UPDATE PRODUCTOSCONTRATADOS SET saldoCapital=?,plazoPendiente=?,sumatoriaInteresesPagados=sumatoriaInteresesPagados+? WHERE idCuentaCredito=?",
                  (nuevo_sal,nuevo_pen,inte,idc))
        self.con.commit()
        print(f"Pagó {val:.2f}. Saldo {nuevo_sal:.2f}. Meses restantes {nuevo_pen}.")

    def consultar_saldo_ahorros(self):
        # Muestra el saldo actual y proyectado de una cuenta de ahorros
        idc=leer_entero("Cuenta ahorros: ")
        if self.obtener_tipo(idc)!=2: print("No es ahorro."); return
        d=self.datos_ahorro(idc)
        if not d: print("No existe."); return
        sal,rem=d; proj=sal*(1+rem/100)
        print(f"Saldo:{sal:.2f} Rem:{rem}% Proy:{proj:.2f}")

    def transaccion_ahorros(self):
        # Consignación o retiro de una cuenta de ahorros
        idc=leer_entero("Cuenta ahorros: ")
        if self.obtener_tipo(idc)!=2: print("No es ahorro."); return
        d=self.datos_ahorro(idc)
        if not d: print("No existe."); return
        sal,_=d; print(f"Saldo actual:{sal:.2f}")
        fec=input("Fecha(YYYY-MM-DD): ").strip()[:10]
        val=float(input("Valor(+/-): "))
        nuevo=sal+val
        c=self.con.cursor()
        c.execute("INSERT INTO TRANSACCIONES VALUES(NULL,?,?,?)",(idc,fec,val))
        c.execute("UPDATE PRODUCTOSCONTRATADOS SET saldoCapital=? WHERE idCuentaCredito=?",(nuevo,idc))
        self.con.commit(); print(f"Nuevo saldo:{nuevo:.2f}")

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
            '2': self.pad.adquirir,
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

    def menu_clientes(self):
        while True:
            print("\n-- Clientes --\n1.Crear\n2.Actualizar Dirección\n3.Consultar\n4.Volver")
            op = input("Opción: ")
            if op == '1':
                self.cli.insertar()
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
