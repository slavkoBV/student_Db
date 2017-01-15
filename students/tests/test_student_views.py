from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from students.models.students import Student
from students.models.groups import Group


class TestStudentList(TestCase):

	def setUp(self):
		group1, created = Group.objects.get_or_create(
								title='Test-1')
		group2, created = Group.objects.get_or_create(
								title='Test-2')
		Student.objects.get_or_create(
			first_name="John",
			last_name="Petrucci",
			birthday=datetime.today(),
			ticket=12345,
			student_group=group1)
		Student.objects.get_or_create(
			first_name="Steve",
			last_name="Vai",
			birthday=datetime.today(),
			ticket=100500,
			student_group=group2)
		Student.objects.get_or_create(
			first_name="James",
			last_name="LaBree",
			birthday=datetime.today(),
			ticket=22345,
			student_group=group1)
		Student.objects.get_or_create(
			first_name="John",
			last_name="Muyung",
			birthday=datetime.today(),
			ticket=32345,
			student_group=group1)

		self.client = Client()
		self.url = reverse('home')

	def test_students_list(self):
		# make request to the server to get homepage
		response = self.client.get(self.url)

		# have we received OK status from the server?
		self.assertEqual(response.status_code, 200)

		# do we have student name on a page?
		self.assertIn('John', response.content)

		# do we have link to student edit form?
		#self.assertIn(reverse("students_edit", kwargs={'pk': Student.objects.all()[0].id}), response.content)

		# ensure we got 3 students, pagination limit is 3
		self.assertEqual(len(response.context['students']), 3)

	def test_current_group(self):
		group = Group.objects.filter(title='Test-2')[0]
		self.client.cookies['current_group'] = group.id

		response = self.client.get(self.url)

		self.assertEqual(len(response.context['students']), 1)

	def test_order_by(self):
		response = self.client.get(self.url, {'order_by': 'last_name'})

		students = response.context['students']
		self.assertEqual(students[0].last_name, 'LaBree')
		self.assertEqual(students[1].last_name, 'Muyung')
		self.assertEqual(students[2].last_name, 'Petrucci')	
