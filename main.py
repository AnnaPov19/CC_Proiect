from flask import Flask, request, jsonify
from google.cloud import firestore
import datetime

app = Flask(__name__)
client = datastore.Client(datastore="bilete")

@app.route('/ticket/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    key = client.key('Bilet', ticket_id)
    entity = client.get(key)

    if not entity:
        return jsonify({'message': 'Biletul nu există'}), 404

    ticket_date = datetime.datetime.strptime(entity['data'], '%d.%m.%Y').date()
    current_date = datetime.date.today()

    if ticket_date < current_date:
        return jsonify({'valid': False, 'message': 'Bilet expirat'})
    else:
        return jsonify({'valid': True, 'bilet': dict(entity)})

@app.route('/ticket', methods=['POST'])
def create_ticket():
    data = request.get_json()
    required = ['data', 'destinație', 'nume_client', 'ora', 'plecare']
    if not all(k in data for k in required):
        return jsonify({'message': 'Date incomplete'}), 400

    new_id = f"bilet-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    key = client.key('Bilet', new_id)
    entity = datastore.Entity(key=key)
    entity.update({**data, 'id': new_id})
    client.put(entity)

    return jsonify({'message': 'Bilet creat', 'id': new_id}), 201

if __name__ == '__main__':
    app.run()
