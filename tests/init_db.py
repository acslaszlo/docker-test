from datetime import datetime

from flywheel import Engine, Field, Model


class Data(Model):
    id = Field(data_type=str, hash_key=True)
    val1 = Field(data_type=str)
    val2 = Field(data_type=int)
    val3 = Field(data_type=str)


def write_data(namepsace: str, val3_base: str) -> None:
    db = Engine(namespace=namepsace)
    db.connect(
        'local',
        access_key='AK',
        secret_key='SK',
        host='localhost',
        port=8000,
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


write_data(namepsace='Test', val3_base='test')
write_data(namepsace='Prod', val3_base='prod')
