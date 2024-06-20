import json
import ssl
import http.client
import tempfile
import os
from urllib.parse import urlparse
from django.conf import settings

class JsonRpcClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def call_method(self, method, params=None):
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or [],
            'id': 1,
        }
        data = json.dumps(payload)

        # Создание временных файлов для сертификата и ключа
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as cert_file:
            cert_file.write(settings.CLIENT_CERT)
            cert_file.flush()
            cert_file_name = cert_file.name

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as key_file:
            key_file.write(settings.CLIENT_KEY)
            key_file.flush()
            key_file_name = key_file.name

        try:
            # Настройка SSL контекста для клиента с отключенной проверкой сертификатов
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.load_cert_chain(certfile=cert_file_name, keyfile=key_file_name)

            # Разбор URL для извлечения хоста и пути
            url = urlparse(self.endpoint)
            conn = http.client.HTTPSConnection(url.hostname, url.port, context=context)
            headers = {'Content-Type': 'application/json'}

            conn.request("POST", url.path, body=data, headers=headers)
            response = conn.getresponse()
            response_data = response.read().decode()

            if response.status == 200:
                return json.loads(response_data)
            else:
                raise Exception(f"HTTP {response.status}: {response.reason}")
        finally:
            conn.close()
            # Удаление временных файлов
            os.remove(cert_file_name)
            os.remove(key_file_name)

client = JsonRpcClient('https://slb.medv.ru/api/v2/')
