import json
import os
import requests
import tempfile
from django.conf import settings

class JsonRpcClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def call_method(self, method, params=None):
        headers = {'Content-Type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or [],
            'id': 1,
        }

        # Создание временных файлов для сертификата и ключа
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(settings.CLIENT_CERT.encode())
            cert_file.flush()
            cert_file_name = cert_file.name

        with tempfile.NamedTemporaryFile(delete=False) as key_file:
            key_file.write(settings.CLIENT_KEY.encode())
            key_file.flush()
            key_file_name = key_file.name

        try:
            response = requests.post(
                self.endpoint,
                data=json.dumps(payload),
                headers=headers,
                cert=(cert_file_name, key_file_name)
            )

            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        finally:
            # Удаление временных файлов
            os.remove(cert_file_name)
            os.remove(key_file_name)

client = JsonRpcClient('https://slb.medv.ru/api/v2/')
