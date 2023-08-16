from flask import Flask, render_template, request, make_response
from flask_wtf.csrf import CSRFProtect
import requests

app = Flask(__name__, template_folder='.', static_folder='./static')
csrf = CSRFProtect()
csrf.init_app(app)

db_url = 'https://db-sokola.duckdns.org'


def execute_query(query):
    url = f'{db_url}/db/query?associative&q={query}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None


def write_query(query_list):
    url = f'{db_url}/db/execute'
    
    response = requests.post(url, json=query_list)
    r = response.json()
    
    if response.status_code == 200 and 'rows_affected' in r['results'][0]:
        return r
    else:
        return None


@app.route('/', methods=['GET'])
def web():
    results = execute_query("SELECT * FROM sokola")
    rows = results['results'][0]['rows']
    name_pairs = []

    for i in range(0, len(rows), 2):
        if i + 1 < len(rows):
            pair = (rows[i]['NAME'], rows[i + 1]['NAME'])
        else:
            pair = (rows[i]['NAME'], "")
        name_pairs.append(pair)

    print(name_pairs)
    
    return render_template('index.html', sokola_names=name_pairs)


@app.route('/admin', methods=['GET'])
def admin():
    results = execute_query("SELECT * FROM sokola")
    names = []
    if results:
        names = [(item['ID'], item['NAME']) for item in results['results'][0]['rows']]

    return render_template('admin.html', message="", sokola_names=names)


@app.route('/add', methods=['POST'])
def add():
    name = request.form['sokola-name']
    
    query = f"INSERT INTO sokola (NAME) VALUES ('{name}')"
    write_query([query])

    results = execute_query("SELECT * FROM sokola")
    names = []
    if results:
        names = [(item['ID'], item['NAME']) for item in results['results'][0]['rows']]
    
    return render_template('admin.html', message="Tafiditra", sokola_names=names)


@app.route('/delete', methods=['POST'])
def delete():
    ID = request.args['id']
    
    query = f"DELETE FROM sokola WHERE ID={ID}"
    r = write_query([query])
    if r == None:
        return make_response({'code': 400}, 400)
    
    return make_response({'code': 200}, 200)


@app.route('/update', methods=['POST'])
def update():
    ID = request.args['id']
    new_name = request.args['name']
    
    query = f"UPDATE sokola SET NAME='{new_name}' WHERE ID={ID}"
    r = write_query([query])
    if r == None:
        return make_response({'code': 400}, 400)
    
    return make_response({'code': 200}, 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)