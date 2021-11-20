
from flask import Flask, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from os import environ

app = Flask(__name__)
api = Api(app)

# set the SQLALCHEMY_DATABASE_URI key
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL") or "sqlite:///Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)


class TemperaturModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatur = db.Column(db.Float(), index=True, unique=False)


temp_put_args = reqparse.RequestParser()
temp_put_args.add_argument(
    "id", type=int, help="ID of the Temperature youre looking for", required=False)
temp_put_args.add_argument(
    "temperatur", type=float, help="Weight value is required", required=True)

temp_updt_args = reqparse.RequestParser()
temp_updt_args.add_argument(
    "id", type=int, help="ID of the Temperature youre looking for", required=True)
temp_updt_args.add_argument(
    "temperatur", type=float, help="Weight value is required", required=True)

temp_del_args = reqparse.RequestParser()
temp_del_args.add_argument(
    "id", type=int, help="ID of the Temperature youre looking for", required=False)


resource_fields = {
    'id': fields.Integer,
    'temperatur': fields.Float
}


@app.route('/')
@app.route('/index')
def greeting():
    return "This is a test REST Api, which handles temperatur recordings"


class Temperatur(Resource):
    @marshal_with(resource_fields)
    def get(self):
        try:
            result = TemperaturModel.query.all()
            return result
        except:
            return("Api Aktion hat nicht funktioniert")

    @marshal_with(resource_fields)
    def put(self):
        try:
            args = temp_put_args.parse_args()
            temp_value = TemperaturModel(temperatur=args['temperatur'])
            db.session.add(temp_value)
            db.session.commit()
            return f"Eintrag mit dem Wert {args['temperatur']} wurde angelegt"
        except:
            return("Api Aktion hat nicht funktioniert")
            


    @marshal_with(resource_fields)
    def patch(self):
        try:
            args = temp_updt_args.parse_args()
            # print(type(args['id']))
            result = TemperaturModel.query.filter_by(id=args['id']).first()
            print(result)
            if result == None:
                abort(404, message="Temperatur id does not exist")
            elif args['temperatur']:
                result.temperatur = args['temperatur']

            db.session.commit()
            return result
        except:
            return("Api Aktion hat nicht funktioniert")


    def delete(self):
        try:
            args = temp_del_args.parse_args()
            wert = args["id"]
            wertPlus1 = wert + 1    
            print(wertPlus1)    
        
            result = TemperaturModel.query.filter_by(id=wert).first()
            print(result)
            db.session.delete(result)
            db.session.commit()
            return f"Eintrag mit ID = {args['id']} wurde gelöscht"
            
        except:
            try:
                result = TemperaturModel.query.all()[-1]
                db.session.delete(result)
                db.session.commit()            
                print(result)
                return f"Eintrag mit ID = {result.id} wurde gelöscht"
            except:
                return("Api Aktion hat nicht funktioniert")


api.add_resource(Temperatur,
                 "/temperatur",)


if __name__ == '__main__':
    app.run(debug=True)
