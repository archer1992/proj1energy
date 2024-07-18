from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd
import re

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="srv1412.hstgr.io",
        user="u540656491_powerplants_db",  # your MySQL username
        password="0kMEX3Zv;",  # your MySQL password
        database="u540656491_test"
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
    df = df[(df['resource_category'] != '') & (df['owner_type'] != '') & (df['island'] != '') & (df['region'] != '')]
    df['region'] = df['region'].apply(lambda x: f'Region {x}' if re.match(r'^\d+(-[A-Za-z])?$', x) else x)
    df['region'] = df['region'].str.upper()
    df['facility_name'] = df['facility_name'].str.upper()
    df['resource_category'] = df['resource_category'].str.upper()
    df['technology_type'] = df['technology_type'].str.upper()
    df['island'] = df['island'].str.upper()
    df['owner_type'] = df['owner_type'].str.upper()
    df['dependable_capacity'] = df['dependable_capacity'].apply(lambda x: round(float(x), 2))
    return jsonify(df.to_dict(orient='records'))

@app.route('/filters')
def filters():
    conn = get_db_connection()
    df = pd.read_sql('SELECT DISTINCT LOWER(resource_category) AS resource_category, LOWER(owner_type) AS owner_type, LOWER(island) AS island, LOWER(region) AS region FROM powerplants', conn)
    conn.close()
    df = df[(df['resource_category'] != '') & (df['owner_type'] != '') & (df['island'] != '') & (df['region'] != '')]
    df['region'] = df['region'].apply(lambda x: f'region {x}' if re.match(r'^\d+(-[A-Za-z])?$', x) else x)
    df['region'] = df['region'].str.upper()
    filters = {
        "resource_category": sorted(df['resource_category'].dropna().unique().tolist()),
        "owner_type": sorted(df['owner_type'].dropna().unique().tolist()),
        "island": sorted(df['island'].dropna().unique().tolist()),
        "region": sorted(df['region'].dropna().unique().tolist(), key=lambda x: (int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'), x))
    }
    return jsonify(filters)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')