from django.shortcuts import render, HttpResponseRedirect
from .models import ListTest, AddPdfFileModel
from . import forms

# Create your views here.
def home(request):
	return render(request, "home.html")
def testlist(request):
	test = ListTest()
	test.labels = ["python","django"]
	test.labels.append("cityking")
	test.save()

	obs = ListTest.objects.all()
	for ob in obs:
		print(ob.labels)
	return HttpResponseRedirect("/")
	
	
def addfile(request):
	if request.method == "POST":
		form = forms.AddPdfForm(request.POST, request.FILES)
		#import pdb
		#pdb.set_trace()
		if not form.is_valid():
			print(form.errors)
			return HttpResponseRedirect("/")
		name = form.cleaned_data['name']
		file = form.cleaned_data['file']
		add_pdf_model = AddPdfFileModel(name=name, file=file)
		add_pdf_model.save()
	return render(request, "add.html", {'form':forms.AddPdfForm()})
