import pandas as pd
import sqlite3
import os

# Configura el nombre de la base de datos y la carpeta de CSV
db_name = "F1.db"
csv_folder = "F1_Datasets/"  # Cambia esto por la ruta donde están tus CSV

# Conectar a SQLite (crea el archivo si no existe)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Iterar sobre cada archivo CSV en la carpeta
for file_name in os.listdir(csv_folder):
    if file_name.endswith(".csv"):
        table_name = file_name.replace(".csv", "")
        file_path = os.path.join(csv_folder, file_name)

        # Cargar el CSV en un DataFrame
        df = pd.read_csv(file_path)

        # Escribir el DataFrame en una tabla SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Tabla '{table_name}' creada en la base de datos.")

# Cerrar la conexión
conn.close()
print(f"Base de datos '{db_name}' creada con éxito.")