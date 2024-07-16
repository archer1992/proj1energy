from flask import Flask, render_template, request, jsonify, send_file
import mysql.connector
import pandas as pd
import io

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="",  # your MySQL password
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
    return jsonify(df.to_dict(orient='records'))

@app.route('/import', methods=['POST'])
def import_csv():
    file = request.files['file']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        data = pd.read_csv(file)
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('TRUNCATE TABLE powerplants')

        skipped_rows = []

        for index, row in data.iterrows():
            if row.isnull().any():
                skipped_rows.append(index + 1)  # +1 to account for header row
                continue
            cursor.execute('''
                INSERT INTO powerplants (
                    facility_name, resource_category, technology_type, installed_capacity,
                    dependable_capacity, location, longitude, latitude, region, island, operator, owner, owner_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', tuple(row))

        conn.commit()
        conn.close()

        if skipped_rows:
            return jsonify({"error": f"Rows {skipped_rows} were not imported due to missing values."}), 206

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return "Data imported successfully"

@app.route('/export', methods=['GET'])
def export_csv():
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM powerplants', conn)
    conn.close()

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename='powerplants.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
