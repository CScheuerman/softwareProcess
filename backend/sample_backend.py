from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_userjob = request.args.get('job')
      if search_username and search_userjob:
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username and user['job'] == search_userjob:
               subdict['users_list'].append(user)
         return subdict
      elif search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd = addId(userToAdd)
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd)
      resp.status_code = 201 
      return resp
   
def addId(user):
   user['id'] = ''.join(random.choice(string.ascii_lowercase) for _ in range(3)) +  ''.join(random.choice(string.digits) for _ in range(3))
   return user

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   userToRemove = find_user(id)
   if(userToRemove == {}):
      resp = jsonify(success=False)
      resp.status_code = 404 #optionally, you can always set a response code. 
      # 200 is the default code for a normal respo
      return resp
   if request.method == 'DELETE':
      users['users_list'].remove(userToRemove)
      resp = jsonify(success=True)
      resp.status_code = 204 #optionally, you can always set a response code. 
      # 200 is the default code for a normal respo
      return resp
   return jsonify(success=False)
   
def find_user(id):
   if id :
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users