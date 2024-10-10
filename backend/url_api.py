from flask import Flask, request, redirect, url_for, jsonify
import psycopg2
import base64
import hashlib

app = Flask(__name__)

conn = psycopg2.connect(database="postgres", user="postgres", password="Yeahright$1123")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS url (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, url VARCHAR(255), \
            shortened_url VARCHAR(64));''')
conn.commit()

cur.close()
conn.close()

@app.route("/url", methods=["POST"])
def create_url():
    data = request.json
    hash_object = hashlib.sha256(data['url'].encode('utf-8'))
    shortened_string = base64.b64encode(hash_object.digest())[:6].decode('utf-8')
    if 'url' not in data:
        return jsonify({ "error": "url is not found in request" }), 404
    
    conn = psycopg2.connect(database="postgres", user="postgres", password="Yeahright$1123")
    cur = conn.cursor()

    cur.execute('''INSERT INTO url (url,shortened_url) \
                 VALUES (%s,%s)''',(data['url'], shortened_string))
    
    conn.commit()
    
    cur.close()
    conn.close()

    return jsonify({ "url": data['url'], "shorten_url": shortened_string })

@app.route("/url", methods=["GET"])
def get_urls():
    conn = psycopg2.connect(database="postgres", user="postgres", password="Yeahright$1123")
    cur = conn.cursor()

    cur.execute('''SELECT * from url''')

    data = cur.fetchall()

    conn.close()
    cur.close()

    return jsonify({ "data": data }), 200 

  

if __name__=="__main__":
    app.run(debug=True)