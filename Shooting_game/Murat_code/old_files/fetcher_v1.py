import pandas as pd
import psycopg2
import time

db_name = "tack_test"

# Connect to the PostgreSQL database
def connect_database(db):
    conn = psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        database=db,
        user="postgres",
        password="postgres"
    )
    return conn

def fetch_data_from_view(conn, view_name):
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM force_on_force.{view_name}")

    rows = cursor.fetchall()

    data_list = []
    for row in rows:
        data_list.append(row)

    cursor.close()
    return pd.DataFrame(data_list)

# List of view names you want to fetch data from
view_names = ["export_gunshots", "viz_damage"]

if __name__ == "__main__":
    conn = connect_database(db_name)

    # Create a dictionary to store DataFrames
    data_frames = {}

    # Loop through view names and fetch data from each view
    for view_name in view_names:
        df = fetch_data_from_view(conn, view_name)
        data_frames[view_name] = df

    conn.close()

    # Access the DataFrames using the view names as keys
    export_gunshots_df = data_frames["export_gunshots"]
    viz_damage_df = data_frames["viz_damage"]

    # Now you have two separate Pandas DataFrames: export_gunshots_df and viz_damage_df
    # You can perform further data analysis or operations on these DataFrames as needed

