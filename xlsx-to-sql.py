import pandas as pd
from sqlalchemy import create_engine, text
import phpserialize
from datetime import datetime
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# START EDITABLE CONTENT
host = "127.0.0.1"
port = 3306
user = "root"
password = "root"
database = "application"
table_name = "post_data"
serialized_columns = ['aliases', 'keywords', 'tasks', 'preferences', 'requirements', 'offers']
# END EDITABLE CONTENT

xlsx_file_path = table_name + '.xlsx'

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

dataframe = pd.read_excel(xlsx_file_path)

def string_to_php_serialized(value):
    """
    Convert a comma-separated string to a PHP serialized array.
    """
    if pd.isnull(value) or value == '':
        return phpserialize.dumps([], charset='utf-8')
    else:
        items = [item.strip() for item in value.split(',')]
        return phpserialize.dumps(items, charset='utf-8')

def convert_to_datetime(value):
    """
    Convert a date string to datetime format.
    """
    if isinstance(value, (str, pd.Timestamp)):
        if pd.isnull(value) or value == '':
            return datetime.now()
        else:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
    return value 

for col in serialized_columns:
    if col in dataframe.columns:
        dataframe[col] = dataframe[col].apply(string_to_php_serialized)

# Dátumok konvertálása
dataframe['timestamp'] = dataframe['timestamp'].apply(lambda x: datetime.now() if pd.isnull(x) else x)

with engine.begin() as connection: 
    for index, row in dataframe.iterrows():
        try:
            values = {col: row[col] for col in dataframe.columns if col != 'id'}
            id_value = row['id']
            set_clause = ', '.join([f"{col} = :{col}" for col in values.keys()])
            update_query = text(f"UPDATE {table_name} SET {set_clause} WHERE id = :id")

            values['id'] = id_value
            
            connection.execute(update_query, values)
        except Exception as e:
            print(f"ERROR: {e}")
            break

print("DONE")
