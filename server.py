from flask import Flask, render_template, jsonify
import json
from crime import SeattlePDApi

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/api/raw')
@app.route('/api/raw/<int:limit>')
def api_raw(limit=20):
    path = r'C:\dev\jim\seattle_crime\exports\raw_json_20181102.json'
    with open(path, 'r') as _f:
        data = json.load(_f)
        _f.close()
    
    if limit:
        data = data[:limit]
    return jsonify(data)

@app.route('/api/bydate')
def crime_by_date():
    s = SeattlePDApi()
    data = s.get_crimes_by_date()
    return jsonify(data)