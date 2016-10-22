# coding: utf-8
from django import forms
from .models import AddPdfFileModel  

class AddPdfForm(forms.ModelForm):
	class Meta:
		model = AddPdfFileModel
		fields = ['name', 'file']

class SetTypeForm(forms.Form):
	type = forms.IntegerField()
	#必需要有
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
		

