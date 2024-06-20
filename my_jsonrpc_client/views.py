import json
from django.http import HttpResponse
from django.views.generic import FormView
from django.shortcuts import render

from .forms import JsonRpcForm
from .my_jsonrpc_v1 import client


class JsonRpcView(FormView):
    template_name = 'my_jsonrpc_client/jsonrpc_form.html'
    form_class = JsonRpcForm
    success_url = '/'

    def form_valid(self, form):
        method = form.cleaned_data['method']
        params = form.cleaned_data['params']

        if params:
            params = json.loads(params)
        
        try:
            result = client.call_method(method, params)
        except Exception as e:
            result = {'error': str(e)}
        
        return render(
            self.request,
            self.template_name,
            {'form': form, 'result': result}
        )
