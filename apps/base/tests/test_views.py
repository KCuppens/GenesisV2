from django.test import TestCase
import unittest
from apps.base import views
from django.urls import reverse


class ViewsTest(TestCase):
	
	def test_views_getURLpicker(self):
		url = reverse('getURLPicker')
		resp = self.client.get(url)

		# not action
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(resp.template)
		print(resp)

	# def test_demo(self):
	# 	self.assertEqual(1, 1)

# if __name__ == '__main__':
# 	unittest.main()