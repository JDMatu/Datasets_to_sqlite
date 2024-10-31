
import sqlite3

# Conectar a la base de datos
db_name = "F1.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Desactivar las restricciones de claves foráneas temporalmente
cursor.execute("PRAGMA foreign_keys=off;")

# Diccionario de tablas con claves primarias y foráneas
table_definitions = {
    "circuits": {
        "primary_key": "circuitId",
        "columns": ["circuitId INTEGER", "circuitRef TEXT", "name TEXT", "location TEXT", "country TEXT", "lat REAL", "lng REAL", "alt INTEGER", "url TEXT"],
        "foreign_keys": {}  # No tiene claves foráneas
    },
    "constructor_results": {
        "primary_key": "constructorResultsId",
        "columns": ["constructorResultsId INTEGER", "raceId INTEGER", "constructorId INTEGER", "points REAL", "status TEXT"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "constructorId": "constructors(constructorId)"
        }
    },
    "constructor_standings": {
        "primary_key": "constructorStandingsId",
        "columns": ["constructorStandingsId INTEGER", "raceId INTEGER", "constructorId INTEGER", "points REAL", "position INTEGER", "positionText TEXT", "wins INTEGER"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "constructorId": "constructors(constructorId)"
        }
    },
    "constructors": {
        "primary_key": "constructorId",
        "columns": ["constructorId INTEGER", "constructorRef TEXT", "name TEXT", "national TEXT", "url TEXT"],
        "foreign_keys": {}  # No tiene claves foráneas
    },
    "driver_standings": {
        "primary_key": "driverStandingsId",
        "columns": ["driverStandingsId INTEGER", "raceId INTEGER", "driverId INTEGER", "points REAL", "position INTEGER", "positionText TEXT", "wins INTEGER"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "driverId": "drivers(driverId)"
        }
    },
    "drivers": {
        "primary_key": "driverId",
        "columns": ["driverId INTEGER", "driverRef TEXT", "number TEXT", "code TEXT", "forename TEXT", "surname TEXT", "dob TEXT", "nationality TEXT", "url TEXT"],
        "foreign_keys": {}  # No tiene claves foráneas
    },
    "lap_times": {
        "columns": ["raceId INTEGER", "driverId INTEGER", "lap INTEGER", "position INTEGER", "time TEXT", "milliseconds INTEGER"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "driverId": "drivers(driverId)"
        }
    },
    "pit_stops": {
        "columns": ["raceId INTEGER", "driverId INTEGER", "stop INTEGER", "lap INTEGER", "time TEXT", "duration TEXT", "milliseconds INTEGER"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "driverId": "drivers(driverId)"
        }
    },
    "qualifying": {
        "primary_key": "qualifyId",
        "columns": ["qualifyId INTEGER", "raceId INTEGER", "driverId INTEGER", "constructorId INTEGER", "number INTEGER", "position INTEGER", "q1 TEXT", "q2 TEXT", "q3 TEXT"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "driverId": "drivers(driverId)",
            "constructorId": "constructors(constructorId)"
        }
    },
    "races": {
        "primary_key": "raceId",
        "columns": ["raceId INTEGER", "year INTEGER", "round INTEGER", "circuitId INTEGER", "name TEXT", "date TEXT", "time TEXT", "url TEXT", "fp1_date TEXT", "fp1_time TEXT", "fp2_date TEXT", "fp2_time TEXT", "fp3_date TEXT", "fp3_time TEXT", "quali_date TEXT", "quali_time TEXT", "sprint_date TEXT", "sprint_time TEXT"],
        "foreign_keys": {
            "circuitId": "circuits(circuitId)"
        }
    },
    "results": {
        "primary_key": "resultId",
        "columns": ["resultId INTEGER", "raceId INTEGER", "driverId INTEGER", "constructorId INTEGER", "number TEXT", "grid INTEGER", "position TEXT", "positionText TEXT", "positionOrder INTEGER", "points REAL", "laps INTEGER", "time TEXT", "milliseconds TEXT", "fastestLap TEXT", "rank TEXT", "fastestLapTime TEXT", "fastestLapSpeed TEXT", "statusId INTEGER"],
        "foreign_keys": {
            "raceId": "races(raceId)",
            "driverId": "drivers(driverId)",
            "constructorId": "constructors(constructorId)",
            "statusId": "status(statusId)"
        }
    },
    "seasons": {
        "primary_key": "year",
        "columns": ["year INTEGER", "url TEXT"],
        "foreign_keys": {}  # No tiene claves foráneas
    },
    "status": {
        "primary_key": "statusId",
        "columns": ["statusId INTEGER", "status TEXT"],
        "foreign_keys": {}  # No tiene claves foráneas
    },
           
}
# Iterar sobre cada tabla y agregar clave primaria y foráneas
for table, details in table_definitions.items():
    primary_key = details.get("primary_key")
    columns = ", ".join(details["columns"])
    foreign_keys = ", ".join(
        [f"FOREIGN KEY ({col}) REFERENCES {ref}" for col, ref in details["foreign_keys"].items()]
    )

    # Crear la tabla temporal, eliminando si ya existe
    cursor.execute(f"DROP TABLE IF EXISTS {table}_temp;")
    cursor.execute(f"CREATE TABLE {table}_temp AS SELECT * FROM {table};")

    # Crear la nueva tabla con clave primaria (si existe) y foráneas
    create_table_sql = f"""
    CREATE TABLE new_{table} (
        {columns}
        {f', PRIMARY KEY ({primary_key})' if primary_key else ""}
        {f', {foreign_keys}' if foreign_keys else ""}
    );
    """
    # Limpiar cualquier línea vacía adicional que se genere por omisiones
    create_table_sql = create_table_sql.replace(", ,", ",").replace(", )", ")").replace(",  ", " ")
    print(create_table_sql)
    cursor.execute(create_table_sql)

    # Copiar los datos a la nueva tabla
    cursor.execute(f"INSERT INTO new_{table} SELECT * FROM {table}_temp;")

    # Renombrar las tablas
    cursor.execute(f"DROP TABLE {table};")
    cursor.execute(f"ALTER TABLE new_{table} RENAME TO {table};")

    # Eliminar la tabla temporal
    cursor.execute(f"DROP TABLE {table}_temp;")

# Activar restricciones de claves foráneas
cursor.execute("PRAGMA foreign_keys=on;")

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()
print("Claves primarias y foráneas agregadas exitosamente.")