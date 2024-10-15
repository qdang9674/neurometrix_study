import argparse
import os
import pandas as pd
import psycopg2
import time

def fetch_topics(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT topic from tack.message")
    topics = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return topics

def fetch_data_for_topic(conn, topic):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT utc, data, headers FROM tack.message WHERE topic = %s",
        (topic,)
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

if __name__ == '__main__':
    database_numbers = ["tack_test"]

    for db_name in database_numbers:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            database=db_name,
            user="postgres",
            password="postgres"
        )

        folder_name = f"{db_name}_Data"  # Change the folder naming as desired
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        t1 = time.time()

        topics = fetch_topics(conn)

        data_sections = {}

        for topic in topics:
            try:
                print("Processing topic:", topic, 'fetch start.', time.time())
                df = fetch_data_for_topic(conn, topic)
                print("Processing topic:", topic, 'fetch end.', time.time())
                data_sections[topic] = df

                csv_file = f"{folder_name}/{topic}.csv"
                df.to_csv(csv_file, index=False)
                print(f"Data sections for topic '{topic}' saved as '{csv_file}' successfully.")
            except Exception as e:
                print(f"error happened while processing the topic")
                continue
        conn.close()

        t2 = time.time()
        runtime = int(t2 - t1)
        print("Runtime:", runtime, "seconds")
