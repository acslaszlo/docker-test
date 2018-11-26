from datetime import datetime, timedelta
import sys
import time
from threading import Thread

import requests

TIMEOUT = timedelta(seconds=10)
failed = set()


def check_service(started: datetime, url: str) -> None:
    while True:
        if datetime.utcnow() - started > TIMEOUT:
            failed.add(url)
            break

        try:
            r = requests.get(url=url, timeout=1)

            if r.status_code // 100 == 2:
                print(f'{url} is OK')

                break
            else:
                print(f'{url} failed with {r.status_code}')
                time.sleep(1)
        except Exception as e:
            print(f'{url} failed with {e}')
            time.sleep(1)


urls = list(sorted(sys.argv[1:]))
started = datetime.utcnow()

print(f'Checking the following services: {urls}')
threads = [Thread(target=check_service, kwargs={'started': started, 'url': url}) for url in urls]

for t in threads:
    t.start()

for t in threads:
    t.join()

if len(failed):
    raise TimeoutError(f'The following services failed to respond in time: {list(sorted(failed))}')

print('All services are OK')
