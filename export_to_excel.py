import sqlite3
import pandas as pd


db_path = 'instance/site.db'


conn = sqlite3.connect(db_path)


table_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(table_query, conn)


excel_file = 'site_data.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    for table_name in tables['name']:
        
        if table_name.startswith('sqlite_'):
            continue
        
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
        df.to_excel(writer, sheet_name=table_name, index=False)


conn.close()

print(f"Data has been exported to {excel_file}")

