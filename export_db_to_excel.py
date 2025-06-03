import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = 'bot_database.db'
EXPORT_FILE = f"db_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

def export_db_to_excel(db_path, export_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]

    # Create a Pandas Excel writer
    with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
        for table in tables:
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                df.to_excel(writer, sheet_name=table[:31], index=False)  # Excel sheet name max length is 31
                print(f"Exported table: {table}")
            except Exception as e:
                print(f"Failed to export {table}: {e}")
    
    conn.close()
    print(f"\n✅ Export complete! File saved as: {export_path}")

if __name__ == '__main__':
    export_db_to_excel(DB_NAME, EXPORT_FILE)
