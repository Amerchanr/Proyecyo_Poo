def crearTablas(con):
    cursor = con.cursor()
    # Tabla de productos
    cursor.execute('''CREATE TABLE IF NOT EXISTS PRODUCTOS (NoIdProducto integer ,
                                        NombreProducto txt NOT NULL,
                                        TipoProducto integer NOT NULL,
                                        Remuneracion integer NOT NULL,
                                        PRIMARY KEY(NoIdProducto,NombreProducto)) ''')
    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes(
                                                noIdCliente INTEGER PRIMARY KEY,
                                                nombre TEXT NOT NULL,
                                                apellido TEXT NOT NULL,
                                                direccion TEXT,
                                                telefono TEXT,
                                                correo TEXT) ''')
    # Tabla de productos contratados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductosContratados(
                                                idCuentaCredito INTEGER PRIMARY KEY AUTOINCREMENT,
                                                idProducto INTEGER,
                                                idCliente INTEGER,
                                                capitalInicial REAL,
                                                plazoMeses INTEGER,
                                                fechaEntrega TEXT,
                                                saldoCapital REAL,
                                                sumatoriaInteresesPagados REAL DEFAULT 0,
                                                plazoPendiente INTEGER,
                                                FOREIGN KEY(idProducto) REFERENCES Productos(noIdProducto),
                                                FOREIGN KEY(idCliente) REFERENCES Clientes(noIdCliente))  ''')
    # Tabla de transacciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transacciones(
            idTransaccion INTEGER PRIMARY KEY AUTOINCREMENT,
            idCuentaCredito INTEGER,
            fechaPago TEXT,
            valorPagado REAL,
            FOREIGN KEY(idCuentaCredito) REFERENCES ProductosContratados(idCuentaCredito)
        )
    ''')
    con.commit()