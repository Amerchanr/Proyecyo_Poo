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
    print('conexion cerrada')



def crearTablaTransacciones(con):
    #creamos el objeto para recorrer la base de datos
    cursorObj=con.cursor()
    #ejecutamos la cadena con el metodo execute del objeto cursorObj
    cursorObj.execute('''
        CREATE TABLE IF NOT EXISTS Transacciones(
            idTransaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            idCuentaCredito INTEGER,
            fechaPago TEXT,
            valorPagado REAL,
            FOREIGN KEY(idCuentaCredito) REFERENCES ProductosContratados(idCuentaCredito)
        )
    ''')
    #aseguramos la persistencia con un commit
    con.commit()

def menuTransacciones(con):
    salirTransacciones = False
    while not salirTransacciones:
        opPrincipal = input('''
                            MENU Transaciones 

                            1. Consultar couta a pagar 
                            2. Pagar cuota
                            3. Consultar saldo proyectado
                            4. Consignar o retirar
                            5. Salir
                            Seleccione un a opccion>>>: 

                            ''')
        if(opPrincipal == '1'):
            consultarCuota(con)
        elif (opPrincipal == '2'):
            pagarCuota(con)
        elif (opPrincipal == '3'):
            consultarSaldoAhorros(con)
        elif (opPrincipal == '4'):
            transaccionAhorros(con)
        elif (opPrincipal == '5'):
            salirTransacciones = True
        else:
            print("Opción no válida.")



def consultarCuota(con):
    idCuenta = input("Número de cuenta de crédito: ")
    tipo = obtenerTipoProducto_deCuenta(con, idCuenta)
    if tipo is None:
        print(" Cuenta/Crédito no encontrado.")
        return
    elif tipo != 1:
        print(" Esta opción solo es válida para productos de crédito.")
        return

    datos = obtenerDatosCredito(con, idCuenta)
    if datos:
        saldo, plazoPendiente, interes = datos
        if plazoPendiente <= 0:
            print(" El crédito ya fue pagado totalmente.")
            return
        cuotaCapital = saldo / plazoPendiente
        cuotaInteres = saldo * (interes / 100)
        cuotaTotal = cuotaCapital + cuotaInteres
        print(f"\n=== CUOTA A PAGAR ===")
        print(f"Capital: {cuotaCapital:.2f}")
        print(f"Interés: {cuotaInteres:.2f}")
        print(f"Total a pagar: {cuotaTotal:.2f}")
        print(f"Plazo pendiente: {plazoPendiente} meses")
        print("=====================")
    else:
        print(" No se encontró la cuenta de crédito.")




def obtenerTipoProducto_deCuenta(con, idCuentaCredito):
    cursor = con.cursor()
    cursor.execute('''SELECT P.tipoProducto
                      FROM ProductosContratados PC
                      JOIN Productos P ON PC.idProducto = P.noIdProducto
                      WHERE PC.idCuentaCredito = ?''', (idCuentaCredito,))
    row = cursor.fetchone()
    return int(row[0]) if row else None

def obtenerDatosCredito(con, idCuentaCredito):
    cursor = con.cursor()
    cursor.execute('''SELECT PC.saldoCapital, PC.plazoPendiente, P.remuneracion
                      FROM ProductosContratados PC
                      JOIN Productos P ON PC.idProducto = P.noIdProducto
                      WHERE PC.idCuentaCredito = ?''', (idCuentaCredito,))
    return cursor.fetchone()

def pagarCuota(con):
    idCuenta = input("Número de cuenta de crédito: ")
    tipo = obtenerTipoProducto_deCuenta(con, idCuenta)
    if tipo is None:
        print(" Cuenta/Crédito no encontrado.")
        return
    elif tipo != 1:
        print(" Esta opción solo es válida para productos de crédito.")
        return

    cursor = con.cursor()
    fechaPago = input("Fecha de pago (DD/MM/AAAA): ")

    # Verificar si ya hay pago en el mes actual
    mes_actual = fechaPago[:7]  # 'YYYY-MM'
    cursor.execute('''
        SELECT COUNT(*) FROM Transacciones 
        WHERE idCuentaCredito=? AND strftime('%Y-%m', fechaPago)=?
    ''', (idCuenta, mes_actual))
    pagos_en_mes = cursor.fetchone()[0]

    if pagos_en_mes > 0:
        print(" Este crédito ya está al día este mes. No es necesario pagar de nuevo.")
        return

    datos = obtenerDatosCredito(con, idCuenta)
    if datos:
        saldo, plazoPendiente, interes = datos
        if plazoPendiente <= 0:
            print(" El crédito ya fue pagado totalmente.")
            return
        cuotaCapital = saldo / plazoPendiente
        cuotaInteres = saldo * (interes / 100)
        cuotaTotal = cuotaCapital + cuotaInteres
        print(f"Cuota a pagar este mes: Capital: {cuotaCapital:.2f}, Interés: {cuotaInteres:.2f}, Total: {cuotaTotal:.2f}")
        try:
            valor = float(input("Valor pagado: "))
        except ValueError:
            print(" Error: Debe ingresar un valor numérico.")
            return

        # Registrar transacción
        cursor.execute('''INSERT INTO Transacciones (idCuentaCredito, fechaPago, valorPagado)
                          VALUES (?, ?, ?)''', (idCuenta, fechaPago, valor))

        # Actualizar saldo, plazo, intereses
        saldoNuevo = max(0, saldo - (valor - cuotaInteres))
        plazoNuevo = max(0, plazoPendiente - 1)
        interesesAnt = cursor.execute("SELECT sumatoriaInteresesPagados FROM ProductosContratados WHERE idCuentaCredito = ?", (idCuenta,)).fetchone()[0] or 0
        interesesTotal = interesesAnt + cuotaInteres
        cursor.execute('''UPDATE ProductosContratados
                          SET saldoCapital=?, plazoPendiente=?, sumatoriaInteresesPagados=?
                          WHERE idCuentaCredito=?''',
                       (saldoNuevo, plazoNuevo, interesesTotal, idCuenta))
        con.commit()
        imprimirFacturaCredito(idCuenta, valor, cuotaCapital, cuotaInteres, saldoNuevo, plazoNuevo)
    else:
        print(" No se encontró la cuenta de crédito.")

def consultarSaldoAhorros(con):
    idCuenta = input("Número de cuenta de ahorros: ")
    tipo = obtenerTipoProducto_deCuenta(con, idCuenta)
    if tipo is None:
        print(" Cuenta no encontrada.")
        return
    elif tipo != 2:
        print(" Esta opción solo es válida para productos de ahorros.")
        return

    datos = obtenerDatosAhorro(con, idCuenta)
    if datos:
        saldo, interes = datos
        saldoFinal = saldo * (1 + interes / 100)
        print(f"\n=== SALDO DE AHORROS ===")
        print(f"Saldo actual: {saldo:.2f}")
        print(f"Interés mensual: {interes}%")
        print(f"Saldo proyectado al final del mes: {saldoFinal:.2f}")
        print("=======================")
    else:
        print(" No se encontró la cuenta de ahorros.")


def transaccionAhorros(con):
    idCuenta = input("Número de cuenta de ahorros: ")
    tipo = obtenerTipoProducto_deCuenta(con, idCuenta)
    if tipo is None:
        print(" Cuenta no encontrada.")
        return
    elif tipo != 2:
        print(" Esta opción solo es válida para productos de ahorros.")
        return

    cursor = con.cursor()
    fechaPago = input("Fecha de transacción (DD/MM/AAAA): ")

    datos = obtenerDatosAhorro(con, idCuenta)
    if datos:
        saldo, interes = datos
        print(f"Saldo actual: {saldo:.2f}")
        try:
            valor = float(input("Valor a consignar (+) o retirar (-): "))
        except ValueError:
            print(" Error: Debe ingresar un valor numérico.")
            return

        saldoNuevo = saldo + valor
        cursor.execute('''INSERT INTO Transacciones (idCuentaCredito, fechaPago, valorPagado)
                          VALUES (?, ?, ?)''', (idCuenta, fechaPago, valor))
        cursor.execute('''UPDATE ProductosContratados
                          SET saldoCapital=?
                          WHERE idCuentaCredito=?''', (saldoNuevo, idCuenta))
        con.commit()
        imprimirFacturaAhorro(idCuenta, valor, saldoNuevo)
    else:
        print(" No se encontró la cuenta de ahorro.")

def imprimirFacturaCredito(factura_id, idCuenta, valor, cuotaCapital, cuotaInteres, saldoNuevo, plazoNuevo):
    print("\n====== FACTURA DE TRANSACCIÓN CRÉDITO ======")
    print(f"Número de factura: {factura_id}")
    print(f"Número de cuenta de crédito: {idCuenta}")
    print(f"Valor abonado: {valor}")
    print(f"Cuota capital: {cuotaCapital:.2f}")
    print(f"Cuota interés: {cuotaInteres:.2f}")
    print(f"Saldo restante: {saldoNuevo:.2f}")
    print(f"Plazo pendiente: {plazoNuevo}")
    print("Gracias por su pago.")
    print("============================================")

def imprimirFacturaAhorro(factura_id, idCuenta, valor, saldoNuevo):
    print("\n====== FACTURA DE TRANSACCIÓN AHORRO ======")
    print(f"Número de factura: {factura_id}")
    print(f"Número de cuenta de ahorros: {idCuenta}")
    print(f"Valor consignado/retirado: {valor}")
    print(f"Saldo nuevo: {saldoNuevo:.2f}")
    print("Gracias por su transacción.")
    print("==========================================")

def obtenerDatosAhorro(con, idCuentaCredito):
    cursor = con.cursor()
    cursor.execute('''SELECT PC.saldoCapital, P.remuneracion
                      FROM ProductosContratados PC
                      JOIN Productos P ON PC.idProducto = P.noIdProducto
                      WHERE PC.idCuentaCredito = ?''', (idCuentaCredito,))
    return cursor.fetchone()