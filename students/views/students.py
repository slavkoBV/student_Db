# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from datetime import datetime
from PIL import Image

from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.students import Student
from ..models.groups import Group

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
					elif photo.size > 2*1024*1024:
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

# Student Edit View ##########################################################################
class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'middle_name', 'birthday', 
			'photo', 'ticket', 'student_group', 'notes']

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('students_edit', kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# add buttons
		self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))

	def clean_student_group(self):
	
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи', code='invalid')
		return self.cleaned_data['student_group']

class StudentUpdateView(SuccessMessageMixin, UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm
	success_message = u"Студент %(calc_last_name)s успішно збережений"

	def get_success_url(self):
		return reverse('home')

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, calc_last_name=self.object.last_name,)

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.warning(request, u'Редагування студента <%s> скасовано!' % request.POST['last_name'])
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

# Student Delete View ########################################################################
def students_delete(request, pk):

	del_student = Student.objects.get(id=pk)

	if request.method == 'POST':
		if request.POST.get('delete_button') is not None:
			del_student.delete()
			messages.success(request, u'Студента %s успішно видалено' % del_student.last_name)
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.warning(request, u'Видалення студента %s відмінено' % del_student.last_name)
			return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'students/students_confirm_delete.html', {'del_student':del_student})	