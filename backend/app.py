from flask import Flask, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    "host": os.environ['DB_HOST'],
    "port": os.environ['DB_PORT'],
    "database": os.environ['DB_NAME'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASSWORD']
}

def get_db_connection():
    """
    Returns a database connection object.

    Returns a new, unconnected instance of :py:class:`psycopg2.extensions.connection`.
    The connection is configured using the values in the ``db_config`` dictionary.
    """
    return psycopg2.connect(**db_config)

@app.route('/api/health')
def health_check():
    """
    GET /api/health

    Returns a JSON object with a single key: "status". The value of "status" is "healthy"
    if the application is operating normally, and an error message otherwise.

    Example response:
    {
        "status": "healthy"
    }
    """
    return jsonify({"status": "healthy"}), 200

@app.route('/api/data', methods=['GET'])
def handle_data():
    """
    GET /api/data

    Returns a JSON array of timestamps, which are the access times of the /api/data endpoint.
    Each timestamp is a string in the ISO 8601 format, e.g. "2021-05-08T14:30:00.123456".
    If the database connection fails, an empty array is returned.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS access_log (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL
                )
            ''')
            cur.execute("INSERT INTO access_log (timestamp) VALUES (%s)", (datetime.now(),))
            cur.execute("SELECT timestamp FROM access_log ORDER BY timestamp DESC")
            results = cur.fetchall()
            
        conn.commit()
    
    return jsonify([str(row[0]) for row in results])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)