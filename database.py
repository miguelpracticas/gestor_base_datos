import sqlite3 as sql
import pandas as pd
from tkinter import messagebox
from datetime import datetime

conn = sql.connect("base_de_datos.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Residentes(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT UNIQUE,
        edad INTEGER,
        fecha_inscripcion TEXT
    )
""")

def anadir_residente_db(nombre_completo, edad, fecha_inscripcion):
    try:
        cursor.execute("INSERT INTO Residentes VALUES (null, ?, ?, ?)", (nombre_completo, edad, fecha_inscripcion,))
        conn.commit()
    except sql.IntegrityError:
        messagebox.showerror(title="Residente ya encontrado", message=f"El residente {nombre_completo} ya está en la base de datos")

def busqueda_residente_db(query):
    cursor.execute("SELECT nombre_completo FROM Residentes WHERE nombre_completo LIKE ?", (f'%{query}%',))
    resultados = cursor.fetchall()
    return resultados

def obtener_residentes():
    cursor.execute("SELECT nombre_completo FROM Residentes")
    resultados = cursor.fetchall()
    return resultados

def eliminar_residente(nombre_completo):
    cursor.execute("DELETE FROM Residentes WHERE nombre_completo = ?", (nombre_completo,))
    conn.commit()

def obtener_datos(nombre_completo):
    cursor.execute("SELECT * FROM Residentes WHERE nombre_completo = ?", (nombre_completo,))
    datos = cursor.fetchall()
    return datos[0]

def actualizar_datos_db(nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior):
    cursor.execute("UPDATE Residentes SET nombre_completo = ?, edad = ?, fecha_inscripcion = ? WHERE nombre_completo = ?", (nombre_completo_nuevo, edad_nueva, fecha_nueva, nombre_completo_anterior))
    conn.commit()

def importar_excel_db(ruta_archivo):
    # Leer el archivo Excel y almacenar los datos en un DataFrame
    df = pd.read_excel(ruta_archivo, names=["Nombre", "Edad", "Fecha"])

    # Iterar sobre las filas del DataFrame y ejecutar las consultas INSERT
    for fila in df.itertuples(index=False):
        try:
            fecha_valor = fila[2]
            if isinstance(fecha_valor, str):
                fecha_inscripcion = fecha_valor  # Si es una cadena, mantenerla tal cual
            else:
                fecha_inscripcion = fecha_valor.strftime("%d/%m/%Y")  # Convertir a formato deseado
            cursor.execute('INSERT INTO Residentes VALUES (null, ?, ?, ?)', (fila[0], fila[1], fecha_inscripcion,))
        except sql.IntegrityError:
            continue

    conn.commit()

def exportar_excel_db(ruta_archivo):
    # Leer el archivo de Excel existente y almacenar los datos en un DataFrame
    try:
        df_existente = pd.read_excel(ruta_archivo)
    except FileNotFoundError:
        df_existente = pd.DataFrame(columns=['Nombre', 'Edad', 'Fecha de Inscripción'])
    
    cursor.execute("SELECT nombre_completo, edad, fecha_inscripcion FROM Residentes")
    resultados = cursor.fetchall()
    
    # Crear un DataFrame con los nuevos resultados de la consulta
    df_nuevos = pd.DataFrame(resultados, columns=['Nombre', 'Edad', 'Fecha de Inscripción'])
    
    # Comparar los nuevos datos con los datos existentes
    df_final = pd.concat([df_existente, df_nuevos]).drop_duplicates(keep='last')
    
    # Exportar el DataFrame actualizado a un archivo de Excel
    df_final.to_excel(ruta_archivo, index=False)

def borrar_todo_db():
    cursor.execute("DELETE FROM Residentes;")
    conn.commit

def cerrar_db():
    conn.close()   

