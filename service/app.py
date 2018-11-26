import json
import os

from flask import Flask
from flywheel import Engine
from flywheel.query import EntityNotFoundException

from service.models import Data


db = Engine(namespace=os.environ['DB_NAMESPACE'])
db.connect(
    'local',
    access_key='AK',
    secret_key='SK',
    host='local-db',
    port=8000,
    is_secure=False,
)

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return json.dumps({'status': 'success'})


@app.route('/test/<id_>', methods=['GET'])
def test(id_: int):
    return json.dumps({
        'status': 'success',
        'id': id_,
    })


@app.route('/db/<id_>', methods=['GET'])
def db_endpoint(id_: int):
    try:
        res = db(Data).filter(id=id_).one()

        return json.dumps({
            'status': 'success',
            'id': res.id,
            'val1': res.val1,
            'val2': res.val2,
            'val3': res.val3,
        })
    except EntityNotFoundException:
        return json.dumps({
            'status': 'error',
            'message': f'Item {id_} not found',
        }), 404
