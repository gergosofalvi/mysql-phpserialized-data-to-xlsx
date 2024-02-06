import pandas as pd
from sqlalchemy import create_engine
import phpserialize

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

query = f"SELECT * FROM {table_name}"
dataframe = pd.read_sql(query, engine)

def serialize_to_string(value):
    if isinstance(value, (list, dict)):
        if isinstance(value, list):
            return ', '.join(map(str, value))
        elif isinstance(value, dict):
            return ', '.join(map(str, value.values()))
    return value

def safely_deserialize_php(data):
    try:
        deserialized_data = phpserialize.loads(data.encode(), decode_strings=True) if data is not None else None
        return serialize_to_string(deserialized_data)
    except:
        return None

for col in serialized_columns:
    if col in dataframe.columns:
        dataframe[col] = dataframe[col].apply(safely_deserialize_php)

dataframe.to_excel(xlsx_file_path, index=False)

print(f"DONE - Export: {xlsx_file_path}")