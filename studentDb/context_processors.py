def student_proc(request):
	return {'PORTAL_URL': request.scheme + '://' + request.get_host()}