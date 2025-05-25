from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

app = Flask(__name__)
api = Api(app)

# Initialize Firestore
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'cloud-computing-454218',
})
db = firestore.client()

class Ticket(Resource):
    def get(self, ticket_id):
        """Verifică validitatea unui bilet"""
        doc_ref = db.collection('bilete').document(ticket_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return {'message': 'Biletul nu există'}, 404
            
        ticket_data = doc.to_dict()
        ticket_date = datetime.datetime.strptime(ticket_data['data'], '%d.%m.%Y').date()
        current_date = datetime.date.today()
        
        if ticket_date < current_date:
            return {'valid': False, 'message': 'Bilet expirat'}, 200
        else:
            return {'valid': True, 'bilet': ticket_data}, 200

    def post(self):
        """Creează un nou bilet"""
        data = request.get_json()
        
        required_fields = ['data', 'destinație', 'nume_client', 'ora']
        if not all(field in data for field in required_fields):
            return {'message': 'Date incomplete'}, 400
        
        # Generează ID unic
        new_id = f"bilet-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        data['id'] = new_id
        
        # Salvează în Firestore
        db.collection('bilete').document(new_id).set(data)
        
        return {'message': 'Bilet creat', 'id': new_id}, 201

api.add_resource(Ticket, '/ticket', '/ticket/<string:ticket_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)