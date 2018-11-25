import pytest
import requests


SERVERS = [
    {'url': 'http://localhost:5000', 'mode': 'test'},
    {'url': 'http://localhost:5001', 'mode': 'prod'},
]


class TestOne:
    @pytest.mark.parametrize('server', SERVERS)
    def test_test(self, server):
        r = requests.get(
            url=f'{server["url"]}/test/12',
        )

        assert r.status_code == 200
        assert r.json() == {
            'status': 'success',
            'id': '12',
        }

    @pytest.mark.parametrize('server', SERVERS)
    def test_db_found(self, server):
        r = requests.get(
            url=f'{server["url"]}/db/53',
        )

        assert r.status_code == 200
        assert r.json() == {
            'status': 'success',
            'id': '53',
            'val1': '53',
            'val2': 53,
            'val3': f'{server["mode"]}-53'
        }

    @pytest.mark.parametrize('server', SERVERS)
    def test_not_found(self, server):
        r = requests.get(
            url=f'{server["url"]}/db/100',
        )

        assert r.status_code == 404
        assert r.json() == {
            'status': 'error',
            'message': 'Item 100 not found',
        }
