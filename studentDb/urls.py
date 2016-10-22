from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Students patterns:
    url(r'^$', 'students.views.student_list', name='home'),
  	url(r'^students/add/$', 'students.views.students_add', name='students_add'),
   	url(r'^students/(?P<sid>\d+)/edit/$', 'students.views.students_edit', name='students_edit'),
  	url(r'^students/(?P<sid>\d+)/delete/$', 'students.views.students_delete', name='students_delete'),

    # Groups patterns:
    url(r'^groups$', 'students.views.group_list', name='groups'),
	url(r'^groups/(?P<gid>\d+)/edit/$', 'students.views.groups_edit', name='groups_edit'),
  	url(r'^groups/(?P<gid>\d+)/delete/$', 'students.views.groups_delete', name='groups_delete'),    

    url(r'^admin/', include(admin.site.urls)),
]
