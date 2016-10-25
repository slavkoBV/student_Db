# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.students import Student
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Students views

def student_list(request):
	students = Student.objects.all()

	# try to order student list
	order_by = request.GET.get('order_by', 'last_name') # default ordering by last_name
	if order_by in ('last_name', 'first_name', 'ticket'):

		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
		
	# paginate of students list
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
		students = paginator.page(paginator.num_pages)

	return render(request, 'students/students_list.html', {'students':students})

def students_add(request):
		return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
