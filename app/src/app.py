import json
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

""" Init flask and prometheus client"""
app = Flask(__name__)
metrics = PrometheusMetrics(app)

users = {
  'John': 100,
  'Sam': 200,
  'Cem': 300,
}

@app.route('/tocos')
def get_allUsers():
  """Returns all users with Tocos variable"""
  tocos = []
  for user, toco in users.items():
    tocos.append({'user': user, 'tocos': toco})
  response = json.dumps(tocos)
  return response


@app.route("/tocos/<user>")
def get_user(user: str):
  """Returns specific user with Tocos variable"""
  if user in users.keys():
    response = json.dumps({'user': user, 'tocos': users.get(user)})
    return response

if __name__ == '__main__':
  app.run(debug=False)
