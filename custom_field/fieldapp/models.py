from __future__ import unicode_literals

from django.db import models
from .fields import ListField, ContextTypeRestrictedFileField
# Create your models here.

class ListTest(models.Model):
	labels = ListField()

	def __str__(self):
		return "%s " % self.labels
		
class AddPdfFileModel(models.Model):
	name = models.CharField(max_length=200)
	file = ContextTypeRestrictedFileField(context_type='application/pdf',max_upload_size=2000, upload_to='pdf')
	def __str__(self):
		return self.name
