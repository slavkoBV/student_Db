# -*- coding: utf-8 -*-

from django.contrib import admin
from .models.groups import Group
from .models.students import Student
from .models.exams import Exam
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

class StudentFormAdmin(ModelForm):

	def clean_student_group(self):
		"""Check if student is leader of any group.

		If yes, then ensure it's the same as selected group."""

		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
		return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('first_name', 'last_name', 'middle_name')
			}),
		(None, {
			'fields': ('birthday', 'photo')
			}),
		(None, {
			'fields': ('student_group', 'notes')
			}))

	list_display = ('last_name', 'first_name', 'birthday', 'student_group')
	ordering = ['last_name']
	list_display_links = ['last_name', 'first_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'student_group__title']
	form = StudentFormAdmin

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})

class GroupFormAdmin(ModelForm):
	
	def clean_leader(self):
		students = Student.objects.filter(student_group=self.instance)
		if len(students) > 0 and self.cleaned_data['leader'] not in students:
			raise ValidationError(u'Студент не належить до цієї групи', code='invalid')
		return self.cleaned_data['leader']


class GroupAdmin(admin.ModelAdmin):
	fields = ('title', 'leader', 'notes')

	list_display = ('title', 'leader')
	ordering = ['title']
	list_display_links = ['title']
	list_per_page = 10
	search_fields = ['title']
	list_filter = ['leader']
	form = GroupFormAdmin	

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)