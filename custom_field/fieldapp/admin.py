# coding: utf-8

import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')  

from django.contrib import admin
from .models import Poem
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#子类化UserAdmin
class MyUserAdmin(UserAdmin):
	#修改要显示的字段
	list_display = ('email','first_name','last_name', 'is_staff')
	#修改过滤器
	list_filter = ('is_staff', 'last_name')

	search_fields = ('last_name',)

#先取消对User的注册再用MyUserAdmin对其重新注册
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

#class PoemModelAdmin(admin.ModelAdmin):
#	class Meta:
#		model = Poem
#	#定义要显示的字段
#	list_display = ['title', 'author']
#	#定义要显示为链接的字段
#	list_display_links = ['author']
#	#定义搜索框 可以搜索的字段
#	search_fields = ['title', 'author']
#	#定义可编辑的字段
#	list_editable = ['title']
#	#定义可作为过滤器的字段
#	list_filter = ['author']
#
#	#定义显示模板
#	change_form_template = 'change_form.html'
#admin.site.register(Poem, PoemModelAdmin)

from django import forms
from .models import Poem
from .forms import SetTypeForm
from django.shortcuts import render
#自定义widget
class SubInputText(forms.TextInput):
	class Media:
		css = {
			'all':('input.css',)	
		}

class PoemForm(forms.ModelForm):
	class Meta:
		model = Poem
		fields = ['author', 'title', 'type']
		widgets = {
			#设置author的显示方式为文本域
			'author':forms.Textarea(attrs = {'cols':20, 'rows':1}),	
			#设置title为自定义widget SubInputText 
			'title':SubInputText(),
			#设置为单选按钮
			'type':forms.RadioSelect,
		}
		

class PoemModelAdmin(admin.ModelAdmin):
	
	#自定义action
	def print_poem(self, request, queryset):
		for qs in queryset:
			print(qs)
	
	def set_type(self, request, queryset):
		if request.POST.get('post'):
			form = SetTypeForm(request.POST)
			if form.is_valid():
				type = form.cleaned_data['type']
				for qs in queryset:
					qs.type = type 
					qs.save()
				#设置action执行成功的消息提示
				self.message_user(request, "%d poems were changed type %d" % (len(queryset),type))

		else:
			return render(request, 'set_type.html', {'form':SetTypeForm(initial={'_selected_action':request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}),
				'objects':queryset})
			
	#删除不需要的全局action
	def get_actions(self, request):
		actions = super(PoemModelAdmin, self).get_actions(request)
		if 'hello' in actions:
			del actions['hello']
		return actions

	#设置set_type action的显示名称
	set_type.short_description = "set_type_action"

	form = PoemForm
	actions = [print_poem,set_type]
	#禁用所有action
	#actions = None
admin.site.register(Poem, PoemModelAdmin)

#添加全局action
def sayHello(modelname, request, queryset):
	print('hello')
admin.site.add_action(sayHello, 'hello')
#全局禁止action
admin.site.disable_action('delete_selected')
