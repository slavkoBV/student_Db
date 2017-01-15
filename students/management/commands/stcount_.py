from django.core.management.base import BaseCommand

from students.models.students import Student

class Command(BaseCommand):
	args = '<model_name model_name ...>'
	help = "Prints to console number of student related objects in database."

	def handle(self, *args, **options):
		if 'student' in args:
			self.stdout.write('Number of students in database: %d' % Student.objects.count())