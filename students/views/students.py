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
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions, AppendedText

from ..models.students import Student
from ..models.groups import Group

from ..util import paginate, get_current_group

# List of Students ###############################################################
def student_list(request):
	current_group = get_current_group(request)

	if current_group:
		students = Student.objects.filter(student_group=current_group)
	else:
		students = Student.objects.all().order_by('last_name') # default ordering by last_name
	
	# try to order student list
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):

		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
		
	# paginate of students list
	context = paginate(students, 5, request, {'students':students}, var_name='students')

	return render(request, 'students/students_list.html', context)

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
				errors['first_name'] = _(u"First Name is required")
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = _(u"Last Name is required")
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = _(u"Birthday is required")
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = _(u"Input correct date format(Ex. 1980-12-30)")
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = _(u"Ticket number is required")
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = _(u"Choose group for student")
			else:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = _(u"Choose correct group")
				else:
					data['student_group'] = groups[0]

			photo = request.FILES.get('photo')
			if photo:
				# validation of photo
				try:
					image = Image.open(photo)
					if image.format not in ('JPG', 'PNG', 'JPEG'):
						errors['photo'] = _(u"File format incorrect, must be jpg or png")
					elif photo.size > 2*1024*1024:
						errors['photo'] = _(u"File size greater than 2 Mb")
					else:
						data['photo'] = photo
				except Exception:
					errors['photo'] = _(u"It's not an image file")
					
			# save student
			if not errors:
				student = Student(**data)
				student.save()
				#redirect user to students list
				messages.success(request, _(u'Student %s is added successfully') % student.last_name)
				return HttpResponseRedirect(reverse('home') )
			else:
				# render form with errors and previous user input
				return render(request, 'students/students_add.html',
					{'groups':groups, 'errors':errors})
		
		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			messages.warning(request, _(u'Adding of student is canceled!'))
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
		self.helper.label_class = 'col-sm-3 control-label'
		self.helper.field_class = 'col-sm-6 input-form'

		# add calendar icon to birthday input field
		self.helper.layout[3] = AppendedText("birthday", '<span class="glyphicon glyphicon-calendar"></span>', active=True)

		# add buttons
		self.helper.add_input(Submit('add_button', _(u'Save'), css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"))

	def clean_student_group(self):
	
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(_(u'Student is a leader of another group'), code='invalid')
		return self.cleaned_data['student_group']

class StudentUpdateView(SuccessMessageMixin, UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm
	#success_message = _(u"Student %(calc_last_name)s is saved successfully!")
	
	def get_success_url(self):
		return reverse('home')

	def get_success_message(self, cleaned_data):
		return _(u"Student %(calc_last_name)s is saved successfully!") % dict(cleaned_data, calc_last_name=self.object.last_name,)
				 
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.warning(request, _(u'Edit of student <%s> cancel!') % request.POST['last_name'])
			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

# Student Delete View ########################################################################
def students_delete(request, pk):

	del_student = Student.objects.get(id=pk)

	if request.method == 'POST':
		if request.POST.get('delete_button') is not None:
			del_student.delete()
			messages.success(request, _(u'Student %s is deleted successfully') % del_student.last_name)
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.warning(request, _(u'Delete of student %s is canceled') % del_student.last_name)
			return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'students/students_confirm_delete.html', {'del_student':del_student})	