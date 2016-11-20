# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.forms import ModelForm, ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions, AppendedText

from ..models.exams import Exam
from ..models.groups import Group

from ..util import paginate, get_current_group

# Exam List View ################################################
def exams_list(request):
	current_group = get_current_group(request)

	if current_group:
		exams = Exam.objects.filter(exam_group=current_group)
	else:
		exams = Exam.objects.all()

	# try to order exams list
	order_by = request.GET.get('order_by', 'subject')
	if order_by in ('subject', 'dataAndTime'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
		
	# paginate of exams list
	context = paginate(exams, 3, request, {'exams':exams}, var_name='exams')


	return render(request, 'students/exams_list.html', context)
#Exam Add Form #########################################################################################
def exams_add(request):
	groups = Group.objects.all().order_by('title')

	# if form was posted
	if request.method =="POST":
		# if form add_button was clicked
		if request.POST.get('add_button') is not None:
			# Validate input data
			errors = {}

			data = {}

			subject = request.POST.get('subject', '').strip()
			if not subject:
				errors['subject'] = u"Предмет є обов'язковим"
			else:
				data['subject'] = subject

			dataAndTime = request.POST.get('dataAndTime', '').strip()
			if not dataAndTime:
				errors['dataAndTime'] = u"Дата та час іспиту є обов'язковими"
			else:
				try:
					datetime.strptime(dataAndTime, '%Y-%m-%d %H:%M')
				except Exception:
					errors['dataAndTime'] = u"Введіть коректний формат дати (Напр. 2016-11-01 14:00)"
				else:
					data['dataAndTime'] = dataAndTime

			teacher = request.POST.get('teacher', '').strip()
			if not teacher:
				errors['teacher'] = u"Прізвище та ініціали викладача обов'язкові"
			else:
				data['teacher'] = teacher

			exam_group = request.POST.get('exam_group', '').strip()
			if not exam_group:
				errors['exam_group'] = u"Оберіть групу для іспиту"
			else:
				groups = Group.objects.filter(pk=exam_group)
				if len(groups) != 1:
					errors['exam_group'] = u"Оберіть коректну групу"
				else:
					data['exam_group'] = groups[0]

			# save exam
			if not errors:
				exam = Exam(**data)
				exam.save()
				#redirect user to students list
				messages.success(request, u'Іспит з предмету "%s" для групи %s успішно доданий' %
					 (exam.subject, exam.exam_group.title))
				return HttpResponseRedirect(reverse('exams') )
			else:
				# render form with errors and previous user input
				return render(request, 'students/exams_add.html',
					{'groups':groups, 'errors':errors})
		
		elif request.POST.get('cancel_button') is not None:
			# redirect to exams page on cancel button
			messages.warning(request, u'Додавання іспиту скасовано!')
			return HttpResponseRedirect(reverse('exams'))
	else:
		# initial form render
		return render(request, 'students/exams_add.html', {'groups':groups})
# Exams Edit View #########################################################################

class ExamUpdateForm(ModelForm):
	class Meta:
		model = Exam
		fields = ['subject', 'dataAndTime', 'teacher', 'exam_group']

	def __init__(self, *args, **kwargs):
		super(ExamUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('exams_edit', kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-3 control-label'
		self.helper.field_class = 'col-sm-6 input-form'

		# add calendar icon to birthday input field
		self.helper.layout[1] = AppendedText("dataAndTime", '<span class="glyphicon glyphicon-calendar"></span>', active=True)
		# add buttons
		self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))

class ExamUpdateView(SuccessMessageMixin, UpdateView):
	model = Exam
	template_name = 'students/exams_edit.html'
	form_class = ExamUpdateForm
	success_message = u"Іспит з '%(calc_last_name)s' успішно збережений"

	def get_success_url(self):
		return reverse('exams')

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, calc_last_name=self.object.subject,)

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.warning(request, u'Редагування іспиту з "%s" скасовано!' % request.POST['subject'])
			return HttpResponseRedirect(reverse('exams'))
		else:
			return super(ExamUpdateView, self).post(request, *args, **kwargs)

# Exams Delete View ########################################################################
def exams_delete(request, pk):

	del_exam = Exam.objects.get(id=pk)

	if request.method == 'POST':
		if request.POST.get('delete_button') is not None:
			del_exam.delete()
			messages.success(request, u'Іспит з "%s" успішно видалено' % del_exam.subject)
			return HttpResponseRedirect(reverse('exams'))
		else:
			messages.warning(request, u'Видалення іспиту з "%s" відмінено' % del_exam.subject)
			return HttpResponseRedirect(reverse('exams'))
	else:
		return render(request, 'students/exams_confirm_delete.html', {'del_exam':del_exam})