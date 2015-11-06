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
from sqlalchemy import desc

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
  # if len(all_press) == 0:
  #   return []
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

def fetch_by_pressType(pressType, offset=0):
  all_press = Press.query.filter_by(pressType=pressType).order_by(desc(Press.pressTime)).limit(20).offset(offset)
  presses = model_to_dict(all_press)
  return presses

#######
### routes
######
@app.route('/press/fetch_new', methods=['get'])
def fetch_new_press():
  offset = request.args.get('offset') or 0
  target_time = request.args.get('target_time')
  press_type = request.args.get('press_type')
  query_list = [Press.pressTime > target_time]
  if pressType:
    query_list.append(Press.pressType == pressType)
  all_press = Press.query.filter(*query_list).order_by(desc(Press.pressTime)).limit(20).offset(offset).all()
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/fetch_old', methods=['get'])
def fetch_all():
  offset = request.args.get('offset') or 0
  target_time = request.args.get('target_time')
  query_list = [Press.pressTime > target_time]
  if pressType:
    query_list.append(Press.pressType == pressType)
  all_press = Press.query.filter(*query_list).order_by(desc(Press.pressTime)).limit(20).offset(offset).all()
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/top', methods=['get'])
def fetch_top():
  offset = request.args.get('offset') or 0
  all_press = Press.query.filter_by(pressIsTop=1).order_by(desc(Press.pressTime)).limit(20).offset(offset)
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/teaching', methods=['get'])
def teaching():
  offset = request.args.get('offset') or 0
  presses = fetch_by_pressType("教务", offset)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/research', methods=['get'])
def research():
  offset = request.args.get('offset') or 0
  presses = fetch_by_pressType("学术", offset)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/administratation', methods=['get'])
def administratation():
  offset = request.args.get('offset') or 0
  presses = fetch_by_pressType("行政", offset)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/student', methods=['get'])
def student():
  offset = request.args.get('offset') or 0
  presses = fetch_by_pressType("学工", offset)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/school', methods=['get'])
def school():
  offset = request.args.get('offset') or 0
  presses = fetch_by_pressType("校园", offset)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/press/search', methods=['get'])
def search():
  type = request.args.get('type')
  key = request.args.get('key')
  dept = request.args.get('dept')
  offset = request.args.get('offset') or 0
  query_list = []
  if type:
    query_list.append(Press.pressType == type)
  if dept:
    query_list.append(Press.pressDept == dept)
  if key:
    sql_key = "%" + key + "%"
    query_list.append(Press.pressTitle.like(sql_key))
  all_press = Press.query.filter(*query_list).order_by(desc(Press.pressTime)).limit(20).offset(offset).all()
  presses = model_to_dict(all_press)
  data = dict({"success": "success", "data": presses})
  return json.dumps(data, cls=DatetimeEncoder)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)