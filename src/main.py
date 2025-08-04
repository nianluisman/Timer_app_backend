from enum import Enum

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import sqlite3 as db

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class _database_todo_interface:

    def load_data_into_db(self, task: str):
        pass
    def get_data_from_fb(self):
        pass

class todo_dataBase_parser(_database_todo_interface):
    class erros(Enum):
        COULD_NOT_ADD_TASK = -1
        TASK_NOT_FOUND = -2
        COUND_NOT_CONNECT = -3
    

    def __init__(self):
        try:
            self.con = db.connect("tutorial.db")
            self.cur = self.con.cursor()
        except(db.DatabaseError) as e:
            raise RuntimeError(f"{self.erros.COUND_NOT_CONNECT} cound to find database {e}")

    def load_data_into_db(self, task: str):
        """
        put a task into the database. 
        """
        try: 
            self.cur.execute("create table if not exists todos(task)")
            self.cur.execute("INSERT INTO todos VALUES (?)", (task,))
            print(("INSERT INTO todos VALUES ('%s')", task))
            self.con.commit()
            
        except(db.ProgrammingError) as e:
            raise RuntimeError(f"({self.erros.COULD_NOT_ADD_TASK}) error insert: {e}")

        # if self.cur.fetchone()[0] == 1:
        # else:
        #     self.cur.execute("INSERT INTO todos VALUES ('{task}') ")

    def get_data_from_fb(self):
        pass
# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):

    def __init__(self):
        self.to_do_database = todo_dataBase_parser()


    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        TODOS[todo_id] = {"task": todo_id}
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        print( args['task'])
        self.to_do_database.load_data_into_db(args['task'])

        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':

    app.run(debug=True)
