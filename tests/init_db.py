import argparse
from datetime import datetime

from flywheel import Engine

from service.models import Data


parser = argparse.ArgumentParser()
parser.add_argument('--db-port', type=int, help='The port for local DynamoDB')


def write_data(namepsace: str, val3_base: str, port: int) -> None:
    db = Engine(namespace=namepsace)
    db.connect(
        'local',
        access_key='AK',
        secret_key='SK',
        host='localhost',
        port=port,
        is_secure=False,
    )

    db.register(Data)
    db.create_schema()

    started = datetime.utcnow()
    db.save(items=[
        Data(id=str(i), val1=str(i), val2=i, val3=f'{val3_base}-{i}') for i in range(100)
    ])
    elapsed = datetime.utcnow() - started
    print(f'{namepsace} elapsed time: {elapsed}')


args = parser.parse_args()

if args.db_port is None:
    raise ValueError('--db-port has not been set')

write_data(namepsace='Test', val3_base='test', port=args.db_port)
write_data(namepsace='Prod', val3_base='prod', port=args.db_port)
