from django.contrib.auth.models import User
from .models import StProfile
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from django.utils.translation import ugettext as _


class editProfileForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

	def __init__(self, *args, **kwargs):
		super(editProfileForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_action = reverse('profile_edit', kwargs = {'pk': kwargs['instance'].id})
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'

		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-3 control-label'
		self.helper.field_class = 'col-sm-6 input-form'

		self.helper.add_input(Submit('add_button', _(u'Save'), css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"))

class editProfileView(SuccessMessageMixin, UpdateView):
	model = User
	template_name = 'registration/profile_edit.html'
	form_class = editProfileForm
		
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(editProfileView, self).dispatch(*args, **kwargs)

	def get_success_url(self):
		return reverse('profile')

	def get_success_message(self, cleaned_data):
		return _(u"User %(calc_last_name)s is saved successfully!") % dict(cleaned_data, calc_last_name=self.object.last_name,)
				 
	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.warning(request, _(u'Edit of User <%s> cancel!') % request.POST['last_name'])
			return HttpResponseRedirect(reverse('profile'))
		else:
			return super(editProfileView, self).post(request, *args, **kwargs)