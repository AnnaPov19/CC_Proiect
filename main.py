from flask import Flask, request, jsonify
from google.cloud import firestore
import datetime

app = Flask(__name__)
client = firestore.Client(database="bilete")

@app.route('/ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    doc_ref = client.collection("bilete").document(ticket_id)
    entity = doc_ref.get()

    if not entity.exists:
        return jsonify({'message': 'Biletul nu există'}), 404

    ticket_data = entity.to_dict()
    ticket_date = datetime.datetime.strptime(ticket_data['data'], '%d.%m.%Y').date()
    current_date = datetime.date.today()

    if ticket_date < current_date:
        return jsonify({'valid': False, 'message': 'Bilet expirat'})
    else:
        return jsonify({'valid': True, 'bilet': ticket_data})

@app.route('/ticket', methods=['POST'])
def create_ticket():
    data = request.get_json()
    required = ['data', 'destinație', 'nume_client', 'ora', 'plecare']
    
    if not all(k in data for k in required):
        return jsonify({'message': 'Date incomplete'}), 400

    new_id = f"bilet-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    doc_ref = client.collection("bilete").document(new_id)
    doc_ref.set({**data, 'id': new_id})

    return jsonify({'message': 'Bilet creat', 'id': new_id}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
