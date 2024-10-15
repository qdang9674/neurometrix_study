import pandas as pd
import psycopg2
import time


db_name = "tack_test"
# Connect to the PostgreSQL database
def connect_database(db):
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database=db_name,
        user="postgres",
        password="postgres"
    )
    return conn

def fetch_data_for_topic(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT utc, data, headers FROM tack.message WHERE topic = 'unreal.client'"
        #unreal.actor.damage
    )

    rows = cursor.fetchall()

    data_list = []
    for row in rows:
        utc, data, headers = row
        data_dict = {'UTC': utc, 'Host': None}

        if headers and isinstance(headers, dict):
            data_dict['Host'] = headers.get('host', None)

        if data:
            for key, value in data.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        data_dict[f"{key}_{sub_key}"] = sub_value
                else:
                    data_dict[key] = value
        else:
            for key in data_dict.keys():
                if key != 'UTC' and key != 'Host':
                    data_dict[key] = None
        data_list.append(data_dict)

    cursor.close()
    return pd.DataFrame(data_list)



conn = connect_database(db_name)
data_frame = fetch_data_for_topic(conn)


mapping = data_frame.groupby('id')['PlayerName'].agg(lambda x: x.unique().tolist())



mapped_values = df_hit_copy[column].map(mapping1).str[0]
