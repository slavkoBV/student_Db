# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.groups import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.forms import ModelForm, ValidationError
from django.views.generic import UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.students import Student
from ..models.groups import Group


# List of Groups ######################################################

def group_list(request):
	groups = Group.objects.all().order_by('title')
	# try to order groups list
	order_by = request.GET.get('order_by', '')
	if order_by == 'title':
		groups = groups.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			groups = groups.reverse()
		
	# paginate of groups list
	paginator = Paginator(groups, 3)
	page = request.GET.get('page')
	try:
		groups = paginator.page(page)
	except PageNotAnInteger:
		groups = paginator.page(1)
	except EmptyPage:
		groups = paginator.page(paginator.num_pages)

	return render(request, 'students/groups_list.html', {'groups':groups})

# Group Edit View ###########################################################
class GroupUpdateForm(ModelForm):
	class Meta:
		model = Group
		fields = ['title', 'leader', 'notes']

	def __init__(self, *args, **kwargs):
		super(GroupUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		self.helper.form_action = reverse('groups_edit', kwargs = {'pk': kwargs['instance'].id})
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

	def clean_leader(self):
		students = Student.objects.filter(student_group=self.instance)
		if len(students) > 0 and self.cleaned_data['leader'] not in students:
			raise ValidationError(u'Студент не належить до цієї групи', code='invalid')
		return self.cleaned_data['leader']

class GroupUpdateView(SuccessMessageMixin, UpdateView):
	model = Group
	template_name = 'students/groups_edit.html'
	form_class = GroupUpdateForm
	success_message = u"Група %(calc_title)s успішно збережена"

	def get_success_url(self):
		return reverse('groups')

	def get_success_message(self, cleaned_data):
		return self.success_message % dict(cleaned_data, calc_title=self.object.title,)

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.warning(request, u'Редагування групи %s скасовано!' % request.POST['title'])
			return HttpResponseRedirect(reverse('groups'))
		else:
			return super(GroupUpdateView, self).post(request, *args, **kwargs)


# Group Delete Form #########################################################
def groups_delete(request, pk):
	
	del_group = Group.objects.get(id=pk)
	studentsOfDelGroup = Student.objects.filter(student_group=del_group)

	if request.method == 'POST':
		if request.POST.get('delete_button') is not None:
			if len(studentsOfDelGroup) == 0:
				del_group.delete()
				messages.success(request, u'Групу %s успішно видалено' % del_group.title)
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, u'Групу %s неможливо видалити, бо у групі є студенти' % del_group.title)
				return HttpResponseRedirect(reverse('groups'))
		else:
			messages.warning(request, u'Видалення групи %s відмінено' % del_group.title)
			return HttpResponseRedirect(reverse('groups'))
	else:
		return render(request, 'students/groups_confirm_delete.html', {'del_group':del_group})