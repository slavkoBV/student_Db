# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.groups import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Groups views

def group_list(request):
	groups = Group.objects.order_by('title')
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

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)
