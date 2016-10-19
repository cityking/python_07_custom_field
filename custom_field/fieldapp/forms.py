from django import forms
from .models import AddPdfFileModel  

class AddPdfForm(forms.ModelForm):
	class Meta:
		model = AddPdfFileModel
		fields = ['name', 'file']

