import io
import sqlite3 as sql
import csv
import json
from flask import Flask, render_template, request, redirect, url_for, flash, Response

app = Flask(__name__)
app.secret_key = "mi_calve_secreta_para_alertas_y_seguridad"
DATABASE = "inventario.db"

def Gestor_Inventario_db():
    conexion = sql.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL NOT NULL,
            gasto REAL NOT NULL,
            descripcion TEXT NOT NULL,
            total REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

Gestor_Inventario_db()

@app.route('/')
def index():
    conexion = sql.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM movimientos ORDER BY id ASC")
    movimientos = cursor.fetchall()
    cursor.execute("SELECT SUM(total) FROM movimientos")
    resultado_total = cursor.fetchone()[0]
    gran_total = resultado_total if resultado_total is not None else 0.0
    
    conexion.close()
    return render_template('inventario.html', movimientos=movimientos, gran_total=gran_total)

@app.route('/agregar', methods=['POST'])
def agregar_gastos():
    monto = float(request.form.get('monto'))
    gasto = float(request.form.get('gasto'))
    descripcion = request.form.get('descripcion').strip().upper()
    total = monto - gasto
    
    conexion = sql.connect(DATABASE)
    cursor = conexion.cursor()
    try:    
        cursor.execute("INSERT INTO movimientos(monto, gasto, descripcion, total) VALUES (?,?,?,?)", (monto, gasto, descripcion, total))
        conexion.commit()
        flash(f"Movimiento agregado correctamente al sistema")
    except sql.IntegrityError:
        flash(f"ERROR: El movimiento no pudo ser registrado", "success")
    finally:
        conexion.close()
    return redirect(url_for('index'))
@app.route('/actualizar', methods=['POST'])
def actualizar():
    id_actualizar = int(request.form.get('id'))
    nuevo_monto = float(request.form.get('precio'))
    nuevo_gasto = int(request.form.get('cantidad'))
    nueva_descripcion = request.form.get('nombre').strip().upper()
    nuevo_total = nuevo_monto * nuevo_gasto
    conexion=sql.connect(DATABASE)
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM movimientos WHERE id = ?", (id_actualizar,))
    if cursor.fetchone() is None:
        flash(f"⚠️ Error: El movimiento '{id_actualizar}' no existe en el sistema actual.", "danger")
    else:
        cursor.execute("UPDATE movimientos SET monto = ?, gasto = ?, descripcion = ?, total = ? WHERE id = ?",(nuevo_monto, nuevo_gasto,nueva_descripcion, nuevo_total, id_actualizar))
        conexion.commit()
        flash(f"🔄 ¡Movimiento '{id_actualizar}' actualizado correctamente!", "success")
        
    conexion.close()
    return redirect(url_for('index'))
@app.route('/eliminar/<int:id>')     
def eliminar():
    conexion = sql.connect(DATABASE)
    cursor= conexion.cursor()
    cursor.execute("DELETE FROM movimientos WHERE id =?", (id,))
    conexion.commit()
    conexion.close()
    flash("Movimiento eliminado correctamente del sistema.", "success")
    return redirect(url_for('index'))
@app.route('/reporte/txt')
def archivo_txt():
    conexion = sql.connect(DATABASE)
    cursor= conexion.cursor()
    cursor.execute("SELECT *FROM movimientos")
    movimientos = cursor.fetchall()
    conexion.close()
    output = io.StringIO()
    output.write("="*74+"\n")
    output.write("|                            GESTOR DE GASTOS                            |\n")
    output.write("="*74+"\n")
    output.write(f"{'ID':<3} | {'FECHA':<19} | {'TIPO':>10} | {'DESCRIPCIÓN':>21} | {'MONTO':>8}\n")
    output.write("-"*55 + "\n")
    for item in movimientos:
        output.write(f"{item[0]:<3} | {item[1]:>15} | {item[2]:>10} |  {item[3]:>20} | {item[4]:>8} \n")
    res =Response(output.getvalue(), mimetype="text/plain")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_gestor_gastos.txt"
    return res
@app.route('/reporte/csv')
def archivo_csv():
    conexion = sql.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conexion.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "FECHA", "TIPO", "DESCRIPCION", "MONTO","TOTAL"])
    for item in movimientos:
            writer.writerow([item[0],item[1],item[2],item[3],item[4] 
            ])
    res =Response(output.getvalue(), mimetype="text/csv")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_gestor_gastos.csv"
    return res
@app.route('/reporte/json')
def archivo_json():
    conexion = sql.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM movimientos")
    movimientos = cursor.fetchall()
    conexion.close()
    
    datos_json = []
    for item in movimientos:
        linea = {
            "ID": item[0],
            "MONTO": item[1],
            "GASTO": item[2],
            "DESCRIPCION": item[3],
            "TOTAL": item[4]
        }
        datos_json.append(linea)
    json_data = json.dumps(datos_json, indent=4, ensure_ascii=False)
    res = Response(json_data, mimetype="application/json")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_inventario.json"
    return res
    
if __name__ == '__main__':
    app.run(debug=True)