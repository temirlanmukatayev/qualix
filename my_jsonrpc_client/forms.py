from django import forms


class JsonRpcForm(forms.Form):
    method = forms.CharField(label='Method', max_length=100)
    params = forms.CharField(label='Params', widget=forms.Textarea, required=False)
