from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method =='GET':
        msgs = Message.query.order_by(Message.created_at).all()
        new_array=[msg.to_dict() for msg in msgs]
        return jsonify(new_array), 200

    elif request.method == 'POST':
        new_msg= Message(
            id= request.json.get('id'),
            body= request.json.get('body'),
            username= request.json.get('username'),
            created_at= request.json.get('created_at'),
            updated_at= request.json.get('updated_at'),
        )
        db.session.add(new_msg)
        db.session.commit()
        response= make_response(new_msg.to_dict(), 200)
        return response

@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):

    if request.method== 'PATCH':
        msg= Message.query.filter_by(id=id).first()
        msg.body= request.json.get('body')
        return make_response(msg.to_dict(), 200)

    elif request.method=='DELETE':
        msg= Message.query.filter_by(id=id).first()
        db.session.delete(msg)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
