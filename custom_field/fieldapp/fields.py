# encoding: utf-8
from django.db import models
import ast

class ListField(models.TextField):

	description = "just a listfield"

	def __init__(self, *args, **kwargs):
		super(ListField, self).__init__(*args, **kwargs)
		
	#转换数据库中的数据到python变量
	def from_db_value(self, value, expression, conn, context):
		print("from_db_value")
		if not value:
			value=[]
		if isinstance(value, list):
			return value
		print("value type", type(value))
		#把数据还原成它能转换的数据类型
		return ast.literal_eval(value)

	#将python变量处理后保存到数据库
	def get_prep_value(self, value):
		print("get_prep_value")
		if not value:
			return value
		print("value type",type(value))
		return str(value)

from django.forms import ValidationError
class ContextTypeRestrictedFileField(models.FileField):
	def __init__(self, context_type=None, max_upload_size=None, **kwargs):
		self.context_type = context_type
		self.max_upload_size = max_upload_size
		super(ContextTypeRestrictedFileField, self).__init__(**kwargs)
	def clean(self, *args, **kwargs):
		data = super(ContextTypeRestrictedFileField, self).clean(*args, **kwargs)
		#import pdb
		#pdb.set_trace()
		file = data.file
		try:
			type = file.content_type
			if type != self.context_type:
				raise ValidationError("context_type error")
			if file.size > self.max_upload_size:
				raise ValidationError("exceed max uploadsize")
		except AttributeError:
			print("error")
			pass
		return data

