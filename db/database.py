import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    if conn:
        print("Succesfully connected to database.")
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
            parameter_name TEXT,
            parameter_value REAL
        )
    ''')

    # Tabela GcodeHistory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GcodeHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_date DATETIME,
            generated_code TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_sample_data():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Objects (name, width, height, shape, user_preferences, file_path)
            VALUES ('Samples', 10.0, 5.0, 'var', 'preferences', './objects/objects1.dxf')
        ''')

        conn.commit()
        print("Succesfully added data.")
        conn.close()
    except sqlite3.Error as e:
        print(f"Blad przy dodawaniu przykladowych danych: {e}")
    finally:
        if conn:
            conn.close()