# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from datetime import datetime
from PIL import Image


from ..models.students import Student
from ..models.groups import Group

# Students views
# List of Students ###############################################################
def student_list(request):
	students = Student.objects.all().order_by('last_name') # default ordering by last_name
	# try to order student list
	order_by = request.GET.get('order_by', '')
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

# Add new Student #################################################################
def students_add(request):
	groups = Group.objects.all().order_by('title')
	# if form was posted
	if request.method =="POST":
		# if form add_button was clicked
		if request.POST.get('add_button') is not None:
			# Validate input data
			errors = {}

			data = {'middle_name':request.POST.get('middle_name'),
					'notes':request.POST.get('notes')}

			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (Напр. 1980-12-30)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер квитка є обов'язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу для студента"
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = groups[0]

			photo = request.FILES.get('photo')
			if photo:
				# validation of photo
				try:
					image = Image.open(photo)
					if image.format not in ('JPG', 'PNG', 'JPEG'):
						errors['photo'] = u"Формат файла некоректний, має бути jpg або png"
					elif image.size > 2*1024*1024:
						errors['photo'] = u"Розмір файлу більше 2 Мб"
					else:
						data['photo'] = photo
				except Exception:
					errors['photo'] = u"Це не файл зображення"
					
			# save student
			if not errors:
				student = Student(**data)
				student.save()
				#redirect user to students list
				messages.success(request, u'Студент %s успішно доданий' % student.last_name)
				return HttpResponseRedirect(reverse('home') )
			else:
				# render form with errors and previous user input
				return render(request, 'students/students_add.html',
					{'groups':groups, 'errors':errors})
		
		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			messages.warning(request, u'Додавання студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
	else:
		# initial form render
		return render(request, 'students/students_add.html', {'groups':groups})


def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)


def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)