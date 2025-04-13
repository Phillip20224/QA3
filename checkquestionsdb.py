import sqlite3

def show_table_contents(table_name, db_file="questionsdb.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()



def drop_table(table_name, db_file="questionsdb.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Drop the table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
    # Example usage:
    drop_table("Math101")

    conn.commit()
    conn.close()

show_table_contents("DS3620")