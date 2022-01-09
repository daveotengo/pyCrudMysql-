import pymysql
from app import app
from db_config import mysql
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask import Flask,request,abort



comment_post_args = reqparse.RequestParser()
comment_post_args.add_argument("name", type=str, help="Name required",required=True)
comment_post_args.add_argument("myUser", type=str, help="myUser required",required=True)
comment_post_args.add_argument("datum", type=str, help="datum  required",required=True)
comment_post_args.add_argument("comments", type=str, help="comments required",required=True)
comment_post_args.add_argument("webpage", type=str, help="webpage required",required=True)
comment_post_args.add_argument("summary", type=str, help="summary required",required=True)



comment_put_args = reqparse.RequestParser()
comment_put_args.add_argument("id", type=str)
comment_put_args.add_argument("name", type=str)
comment_put_args.add_argument("myUser", type=str)
comment_put_args.add_argument("datum", type=str)
comment_put_args.add_argument("comments", type=str)
comment_put_args.add_argument("webpage", type=str)
comment_put_args.add_argument("summary", type=str)


api = Api(app)

#comments = {}

def abort_if_comment_id_doesnt_exist(comment_id):
    if comment_id not in comments:
        abort(404, "Could not find comment...")

def abort_if_comment_id_exist(comment_id):
    if comment_id in comments:
        abort(409, "comment with id: {0} already exists".format(comment_id))

resource_fields = {
    #'id': fields.Integer,
    'name': fields.String,
    'myUser': fields.String,
    'datum': fields.String,
    'comments': fields.String,
    'webpage': fields.String,
    'summary': fields.String
}

resource_fields_update = {
    'id': fields.Integer,
    'name': fields.String,
    'myUser': fields.String,
    'datum': fields.String,
    'comments': fields.String,
    'webpage': fields.String,
    'summary': fields.String
}

def findById(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM comment WHERE id=%s", id)
		row = cursor.fetchone()
		if row:
			return row
		
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

def findByMyUser(myUser):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM comment WHERE myUser=%s", myUser)
		row = cursor.fetchone()
		if row:
			return row

	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

def getComments():
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM comment")
            rows = cursor.fetchall()
            print("printing rows")
            print(rows)
            return rows

        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

def deleteComment(id):
    print("printing id")
    print(id)
    result = findById(id)
    print(result)
    if not result:
        abort(404, "Could not find comment...")
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comment WHERE id=%s", (id,))
        conn.commit()
        return 'Comment deleted successfully!'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    


    
  
     
     

        

class Comment(Resource):

    @marshal_with(resource_fields)
    def post(self):

        args = comment_post_args.parse_args()

        print("printing args")

        print(args)

        #_id = args['id']
        _name = args['name']
        _myUser = args['myUser']
        _datum = args['datum']
        _comments = args['comments']
        _webpage = args['webpage']
        _summary = args['summary']

        result=findByMyUser(_myUser)

        print("printing result")

        print(result)

        if result:
            abort(409, "Comment with _myUser: {0} already exists".format(_myUser))
 
        print("inserting into database")

        sql = "INSERT INTO comment(name, myUser, datum, comments, webpage, summary) VALUES(%s, %s,%s, %s, %s ,%s)"
        data = (_name, _myUser,_datum,_comments,_webpage,_summary)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()

        return args,201

    @marshal_with(resource_fields_update)
    def put(self):
        args = comment_put_args.parse_args()
        print(args)
        _id = args['id']
        _name = args['name']
        _myUser = args['myUser']
        _datum = args['datum']
        _comments = args['comments']
        _webpage = args['webpage']
        _summary = args['summary']

        result=findById(_id)

        if not result:
            abort(404, "Comment with id: {0} does not exists".format(_id))
        try: 
		# validate the received values
            if _id and _name and _myUser and _datum and  _comments and _webpage and _summary and request.method == 'PUT':

                # save edits
                sql = "UPDATE comment SET name=%s, myuser=%s, datum=%s, comments=%s, webpage=%s, summary=%s WHERE id=%s"
                data = (_name, _myUser,_datum,_comments,_webpage,_summary,_id)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()

                return args
            else:
                return 'Error while updating user'

        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()


    def get(self):
        return getComments()
    

 

class CommentById(Resource):

    def delete(self,id):
        result = deleteComment(id)
        print(result)
        return result,204
    
    def get(self,id):
        result = findById(id)
        if not result:
             abort(404, "Could not find comment...")
        return result,200
       
   
  

    













api.add_resource(Comment, "/PyWS/api/comment")

api.add_resource(CommentById, '/PyWS/api/comment/<int:id>')

#api.add_resource(Comment, "/PyWS/api/comment/<int:id>")



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=2200)