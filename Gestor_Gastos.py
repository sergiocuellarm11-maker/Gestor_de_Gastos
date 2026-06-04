from datetime import datetime
import sqlite3 as sql
import csv
import json
def Gestor_Inventario_db():
    conexion = sql.connect("Gestor_Gastos.db")
    cursor = conexion.cursor()
    # Una sola tabla para todo: Ingresos y Gastos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()
print("Bienvenido al Gestor de Gastos")
print("-"*40)
Gestor_Inventario_db()
def agregar_gastos():
    while True:
        try:
            monto= float(input("Ingrese sus ingresos: "))
            if monto < 0:
                print("ERROR: Recuerda que no se valen numero negativos")
            else:
                break
        except ValueError:
            print("ERROR: Recuerda que solo van numeros")
    while True:
        try: 
            gastos = float (input("Ingrese la cantidad de gastos: "))
            if gastos <  0 :
                print("Recuerda que solo valores positivos")
            else:
                break
        except ValueError:
            print("ERROR: Recuerda que solo van numeros")
    
    fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
        conexion = sql.connect("Gestor_Gastos.db")
        cursor = conexion.cursor()
        if monto > 0:
            cursor.execute(
                "INSERT INTO movimientos (fecha, tipo, descripcion, monto) VALUES (?, ?, ?, ?)",
                (fecha, "Ingreso", "Depósito de ingresos", monto),
            )
        if gastos > 0:
            cursor.execute(
                "INSERT INTO movimientos (fecha, tipo, descripcion, monto) VALUES (?, ?, ?, ?)",
                (fecha, "Gasto", "Registro de gastos", gastos),
            )

        conexion.commit()
        total = monto - gastos
        print(f"¡Registros guardados con éxito!")
        print(f"Saldo de esta operación: ${total}")

    except sql.Error as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        conexion.close()
def ver_historial ():
    print("\n---HISTORIAL DE MOVIMIENTOS---")
    try: 
        conexion =  sql.connect("Gestor_Gastos.db")
        cursor = conexion.cursor()
        cursor.execute(
        "SELECT id,fecha, tipo,descripcion, monto FROM movimientos ORDER BY id DESC"
        )
        movimientos = cursor.fetchall()
        if not movimientos:
            print("No hay movimientos registrados aun")
            return
        print(f" {'ID':<5} |{'Fecha':<20} | {'Tipo':<8} | {'Descripcion':<25} | {'Monto':<10}")
        print("-"*70)
        for mov in movimientos:
            print(f" {mov[0]:<5} |{mov[1]:<20} | {mov[2]:<8} | {mov[3]:<25} | {mov[4]:<.2f}")
        cursor.execute(
                "SELECT SUM(monto) FROM movimientos WHERE tipo = 'Ingreso'"
            )
        ingresos_totales = cursor.fetchone()[0] or 0.0

        cursor.execute(
            "SELECT SUM(monto) FROM movimientos WHERE tipo = 'Gasto'"
        )
        gastos_totales = cursor.fetchone()[0] or 0.0

        saldo_total = ingresos_totales - gastos_totales
        print("-" * 70)
        print(f"SALDO TOTAL ACUMULADO: ${saldo_total:.2f}")

    except sql.Error as e:
        print(f"Error al leer la base de datos: {e}")
    finally:
        conexion.close()
def eliminar():
    while True:
        try:
            numero_id = int(input("Ingrese el numero de id a eliminar"))
            if numero_id <= 0:
                print("El ID debe ser mayor a cero(0)")
            else:
                break
        except ValueError:
            print("Recuerda que solo se pueden ingresar numeros positivos")
    conexion = None
    try:
        conexion = sql.connect("Gestor_Gastos.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM movimientos WHERE id = ?",(numero_id,))
        conexion.commit()
        if cursor.rowcount > 0:
            print("Movimiento eliminado correctamente")
        else:
            print("El movimiento no existe")   
    except sql.Error as e:
        print(f"Error al eliminar en la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()
def actualizar():
    while True:
        try:
            numero_de_id = int(input("Ingrese el numero de ID a actualizar"))
            if numero_de_id <= 0:
                print("Recuerda que el id es mayor a cero (0)")
            else:
                break
        except ValueError:
            print("Recuerda que solo se pueden ingresar numeros positivos")
    conexion = sql.connect("Gestor_Gastos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM movimientos WHERE id = ?", (numero_de_id,))
    if cursor.fetchone() is None:
        print(f"No se encontró ningún movimiento con el ID {numero_de_id}.")
        conexion.close()
        return
    print("Nuevos Datos")
    print("\n--- Ingrese los nuevos datos ---")
    nuevo_concepto = input("Nuevo concepto/descripción: ")

    while True:
        try:
            nuevo_monto = float(input("Nuevo monto: "))
            break
        except ValueError:
            print("Por favor, ingrese un monto numérico válido.")
    sentencia_sql = (
        "UPDATE movimientos SET descripcion = ?, monto = ? WHERE id = ?"
    )
    datos = (nuevo_concepto, nuevo_monto, numero_de_id)

    try:
        cursor.execute(sentencia_sql, datos)
        conexion.commit()  # Guarda los cambios permanentemente
        print(
            f"¡Movimiento con ID {numero_de_id} actualizado correctamente!"
        )
    except sql.Error as e:
        print(f"Hubo un error al actualizar: {e}")
    finally:
            conexion.close() 
def archivo_txt():
    
        ahora = datetime.now()
        fecha = ahora.strftime("%d/%m/%Y %H:%M:%S")
        conexion = sql.connect("Gestor_Gastos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, fecha, tipo, descripcion, monto FROM movimientos")
        items = cursor.fetchall()
        with open("Gestor_Gastos.txt","w" ,encoding="utf-8" )as archivo:
            archivo.write("="*74+"\n")
            archivo.write("|                            GESTOR DE GASTOS                            |\n")
            archivo.write("="*74+"\n")
            archivo.write(f"{'ID':<3} | {'FECHA':<19} | {'TIPO':>10} | {'DESCRIPCIÓN':>21} | {'MONTO':>8}\n")
            for item in items:
                linea = (f"{item[0]:<3} | {item[1]:>15} | {item[2]:>10} |  {item[3]:>20} | {item[4]:>8} \n")
                archivo.write(linea)
            archivo.write(f"Reporte generado el {fecha}\n")
        conexion.close()
def archivo_csv():
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y %H:%M:%S")
    conexion = sql.connect("Gestor_Gastos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, fecha, tipo, descripcion, monto FROM movimientos")
    items = cursor.fetchall()
    conexion.close()
    with open ("Gestor_Gastos.csv", "w", newline="", encoding="utf-8") as archivo:
        escribir = csv.writer(archivo)
        escribir.writerow(["ID", "FECHA", "TIPO", "DESCRIPCION", "MONTO"])
        for item in items:
            escribir.writerow([
                item[0],
                item[1],
                item[2],
                item[3],
                item[4]
                
            ])
        escribir.writerow([])
        escribir.writerow([f"FECHA REPORTE","","","", fecha])
    print("Archivo guardado correctamente")
def archivo_json():
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y %H:%M:%S")
    
    conexion = sql.connect("Gestor_Gastos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, fecha, tipo, descripcion, monto FROM movimientos")
    items = cursor.fetchall()
    conexion.close()
    datos_json = [ ]
    for item in items:
        linea={
            "ID": item[0],
            "FECHA": item[1],
            "TIPO": item[2],
            "DESCRIPCION": item[3],
            "MONTO": item[4]
        }
        datos_json.append(linea)
    reporte = {
        "Fecha_reporte": fecha,
        "Total_Registros": len(datos_json),
        "Movimientos": datos_json
    }
    with open ("Gestor_Gastos.json", "w", encoding="utf-8")as archivo:
        json.dump(reporte,archivo,indent=4, ensure_ascii=False)
    print("Archivo json creado correctamente")


def salir():
    print("Hasta luego")
def menu():
    Gestor_Inventario_db()
    while True:
        print("\n============================")
        print("      GESTOR DE GASTOS         ")
        print("\n============================")
        print("1-Agregar Movimientos(Gastos/Ingresos)")
        print("2-Ver Historial  y Saldo Total")
        print("3-Eliminar movimiento")
        print("4-Actualizar")
        print("5-Generar Reporte TXT")
        print("6-Generar Reporte CSV")
        print("7-Generar Reporte JSON")
        print("8-Salir")
        print("\n============================")
        op = input("Ingrese una opcion: ").strip()
        if op == "1":
            agregar_gastos()
        elif op =="2":
            ver_historial()
        elif op =="3":
            eliminar()
        elif op == "4":
            actualizar()
        elif op =="5":
            archivo_txt()
        elif op =="6":
            archivo_csv()
        elif op =="7":
            archivo_json()
        elif op == "8":
            salir()
            break
        else:
            print("ERROR: Opcion no es valida, Intente de nuevo")
menu()