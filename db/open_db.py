import sqlite3

def create_table():
    conn = sqlite3.connect('./db/database.db')
    if conn:
        print("Succesfully connected to database.")
    else:
        print("Error connecting to database.")
    cursor = conn.cursor()

    # Tabela Objects
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            width REAL NULL,
            height REAL NULL,
            shape TEXT,
            user_preferences TEXT,
            file_path TEXT
        )
    ''')

    # Tabela ToolParameters
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ToolParameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_type TEXT,
            cutting_speed INTEGER,
            move_speed INTEGER,
            cutting_depth INTEGER,
            stop_time INTEGER,
            power INTEGER,
            units TEXT,
            heading TEXT,
            footer TEXT
        )
    ''')

    # Tabela ConfigParameters
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NestConfig (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_name TEXT,
            space REAL,
            alignment TEXT,
            starting_point TEXT,
            rotations INTEGER,
            accuracy REAL,
            explore_holes INTEGER,
            parallel INTEGER,
            tool_id INTEGER,
            FOREIGN KEY (tool_id) REFERENCES ToolParameters(id)
        ) 
    ''')

    # Tabela GcodeHistory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GcodeHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_date DATETIME,
            file_path TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()

# def insert_sample_data():
#     try:
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()

#         cursor.execute('''
#             INSERT INTO Objects (name, width, height, shape, user_preferences, file_path)
#             VALUES ('Samples', 10.0, 5.0, 'var', 'preferences', './objects/objects1.dxf')
#         ''')

#         conn.commit()
#         print("Succesfully added data.")
#         conn.close()
#     except sqlite3.Error as e:
#         print(f"Blad przy dodawaniu przykladowych danych: {e}")
#     finally:
#         if conn:
#             conn.close()