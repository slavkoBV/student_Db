# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Students view

def student_list(request):
	students = (
		{'id': 1,
		'first_name' : u'Іван',
		'last_name' : u'Сидоренко',
		'ticket' : 21,
		'image' : 'img/me.jpeg'
		},
		)
	return render(request, 'students/students_list.html', {'students':students})

def students_add(request):
		return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

# Groups view

def group_list(request):
	groups = (
		{'id': 1,
		'title' : u'ІВТ-97',
		'leader' : u'Сидоренко Іван',
		
		},
		)
	return render(request, 'students/groups_list.html', {'groups':groups})

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)