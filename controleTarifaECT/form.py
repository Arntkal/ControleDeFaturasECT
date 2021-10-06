from django import forms

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()
    
class testForm(forms.Form):
    codigoECT = forms.CharField(label='Código de Postagem ',max_length=50)
    peso = forms.CharField(label='Peso do Objeto ',max_length=50)
    