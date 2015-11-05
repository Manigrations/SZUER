# -*- coding: utf-8 -*-
# generate by acgt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######
###  model
#######

from flask import Flask, request
import json
from datetime import datetime, date
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pressDB'
db = SQLAlchemy(app)

class Press(db.Model):
  pressID = db.Column(db.String(6), primary_key=True)
  pressTitle = db.Column(db.String(80))
  pressURL = db.Column(db.String(100))
  pressDate = db.Column(db.String(100))
  pressTime = db.Column(db.DateTime)
  pressType = db.Column(db.String(10))
  pressDept = db.Column(db.String(20))
  pressIsTop = db.Column(db.SmallInteger)
  pressHasFile = db.Column(db.SmallInteger)

#######
### json date encode method
######
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
#######
### commom method
######
def model_to_dict(all_press):
  if len(all_press) == 0:
    return []
  presses = []
  for p in all_press:
    presses.append({
      "pressID": p.pressID,
      "pressTitle": p.pressTitle,
      "pressURL" : p.pressURL,
      "pressDate": p.pressDate,
      "pressTime": p.pressTime,
      "pressType" : p.pressType,
      "pressDept" : p.pressDept,
      "pressIsTop" : p.pressIsTop,
      "pressHasFile" : p.pressHasFile
    })
  return presses

#######
### routes
######
@app.route('/press/fetch_new_press', methods=['get'])
def fetch_new_press():
  data = dict({"success": "success"})
  return jsonify(data)

@app.route('/press/fetch_all', methods=['get'])
def fetch_all():
  all_press = Press.query.all()
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/top', methods=['get'])
def fetch_top():
  all_press = Press.query.filter_by(pressIsTop=1)
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/teaching', methods=['get'])
def teaching():
  all_press = Press.query.filter_by(pressType="教务")
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/research', methods=['get'])
def researchch():
  all_press = Press.query.filter_by(pressType="学术")
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/administratation', methods=['get'])
def administratation():
  all_press = Press.query.filter_by(pressType="行政")
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/student', methods=['get'])
def student():
  all_press = Press.query.filter_by(pressType="学工")
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/school', methods=['get'])
def school():
  all_press = Press.query.filter_by(pressType="校园")
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/search', methods=['get'])
def search():
  type = request.args.get('type')
  key = request.args.get('key')
  dept = request.args.get('dept')
  query_list = []
  if type:
    query_list.append(Press.pressType == type)
  if dept:
    query_list.append(Press.pressDept == dept)
  if key:
    sql_key = "%" + key + "%"
    query_list.append(Press.pressTitle.like(sql_key))
  all_press = Press.query.filter(*query_list).all()
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)