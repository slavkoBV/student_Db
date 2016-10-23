from django.conf.urls import include, url
from django.contrib import admin
from students.views import students, groups
from .settings import DEBUG, MEDIA_ROOT
from django.views.static import serve

 
urlpatterns = [
    # Students url patterns:
    url(r'^$', students.student_list, name='home'),
  	url(r'^students/add/$', students.students_add, name='students_add'),
   	url(r'^students/(?P<sid>\d+)/edit/$', students.students_edit, name='students_edit'),
  	url(r'^students/(?P<sid>\d+)/delete/$', students.students_delete, name='students_delete'),

    # Groups url patterns:
    url(r'^groups$', groups.group_list, name='groups'),
	url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
  	url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),    

    url(r'^admin/', include(admin.site.urls)),
]

if DEBUG:
	urlpatterns += [
		url(r'media/(?P<path>.*)$', serve,
	 	{'document_root': MEDIA_ROOT})
	]
