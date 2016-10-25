# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.exams import Exam
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Groups views

def exams_list(request):
	exams = Exam.objects.all()

	# try to order student list
	order_by = request.GET.get('order_by', 'subject')
	if order_by in ('subject', 'dataAndTime'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()
		
	# paginate of groups list
	paginator = Paginator(exams, 3)
	page = request.GET.get('page')
	try:
		exams = paginator.page(page)
	except PageNotAnInteger:
		exams = paginator.page(1)
	except EmptyPage:
		exmas = paginator.page(paginator.num_pages)

	return render(request, 'students/exams_list.html', {'exams':exams})
