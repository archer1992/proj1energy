from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd
import re

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="powerplants_db"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM powerplants', conn)
    conn.close()
    df['region'] = df['region'].apply(lambda x: f'Region {x}' if re.match(r'^\d+(-[A-Za-z])?$', x) else x)
    return jsonify(df.to_dict(orient='records'))

@app.route('/filters')
def filters():
    conn = get_db_connection()
    df = pd.read_sql('SELECT DISTINCT LOWER(resource_category) AS resource_category, LOWER(owner_type) AS owner_type, LOWER(island) AS island, LOWER(region) AS region FROM powerplants', conn)
    conn.close()
    df['region'] = df['region'].apply(lambda x: f'region {x}' if re.match(r'^\d+(-[A-Za-z])?$', x) else x)
    region_list = df['region'].dropna().unique().tolist()
    region_list.sort(key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'), x))
    filters = {
        "resource_category": sorted(df['resource_category'].dropna().unique().tolist()),
        "owner_type": sorted(df['owner_type'].dropna().unique().tolist()),
        "island": sorted(df['island'].dropna().unique().tolist()),
        "region": region_list
    }
    return jsonify(filters)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
