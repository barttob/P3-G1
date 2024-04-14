import sqlite3

DB_FILE_PATH = './db/database.db'

def connect_to_database():
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        print("Successfully connected to database.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def close_database_connection(conn):
    if conn:
        conn.close()
        print("Database connection closed.")

def insert_tool_parameter(tool_type, cutting_speed, move_speed, cutting_depth, stop_time, power, units, heading, footer):
    conn = connect_to_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ToolParameters (tool_type, cutting_speed, move_speed, cutting_depth, stop_time, power, units, heading, footer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tool_type, cutting_speed, move_speed, cutting_depth, stop_time, power, units, heading, footer))
        conn.commit()
        print("Tool parameter inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting tool parameter: {e}")
    finally:
        close_database_connection(conn)

def insert_nest_config(config_name, space, alignment, starting_point, rotations, accuracy, explore_holes, parallel, tool_id):
    conn = connect_to_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO NestConfig (config_name, space, alignment, starting_point, rotations, accuracy, explore_holes, parallel, tool_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (config_name, space, alignment, starting_point, rotations, accuracy, explore_holes, parallel, tool_id))
        conn.commit()
        print("Nest configuration inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting nest configuration: {e}")
    finally:
        close_database_connection(conn)

def select_all_tool_parameters():
    conn = connect_to_database()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ToolParameters')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error selecting tool parameters: {e}")
        return []
    finally:
        close_database_connection(conn)

def select_all_nest_configs():
    conn = connect_to_database()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM NestConfig')
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error selecting nest configurations: {e}")
        return []
    finally:
        close_database_connection(conn)
