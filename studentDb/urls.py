# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from students.views import students, groups, exams, contact_admin
from students.views.students import StudentUpdateView
from students.views.groups import GroupUpdateView
from students.views.exams import ExamUpdateView
from students.views.journal import JournalView
from .settings import DEBUG, MEDIA_ROOT
from django.views.static import serve


js_info_dict = {
  'packages': ('students',),
}
 
urlpatterns = [

    # User Related urs:
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page':'home'},
          name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
          name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
    
    # Students url patterns:
    url(r'^$', students.student_list, name='home'),
  	url(r'^students/add/$', students.students_add, name='students_add'),
   	url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
  	url(r'^students/(?P<pk>\d+)/delete/$', students.students_delete, name='students_delete'),

    # Groups url patterns:
    url(r'^groups$', groups.group_list, name='groups'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
  	url(r'^groups/(?P<pk>\d+)/delete/$', groups.groups_delete, name='groups_delete'),

  	# Exams url patterns:
  	url(r'^exams$', exams.exams_list, name='exams'),
    url(r'^exams/add/$', exams.exams_add, name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$', ExamUpdateView.as_view(), name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$', exams.exams_delete, name='exams_delete'),

    # Journal url patterns:
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),

    # Contact Admin url:
    url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),
]

if DEBUG:
	urlpatterns += [
		url(r'media/(?P<path>.*)$', serve,
	 	{'document_root': MEDIA_ROOT})
	]
