# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Groups views

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
