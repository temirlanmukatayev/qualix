from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import JsonRpcView


class JsonRpcViewTests(SimpleTestCase):

    def setUp(self):
        url = reverse('jsonrpc_form')
        self.response = self.client.get(url)

    def test_jsonrpcview_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_jsonrpcview_template(self):
        self.assertTemplateUsed(self.response, 'my_jsonrpc_client/jsonrpc_form.html')

    def test_jsonrpcview_contains_correct_html(self):
        self.assertContains(self.response, 'JsonRpcClient')
    
    def test_jsonrpcview_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'Этого здеть быть не должно!')
    