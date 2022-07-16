from django.test import TestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from linkcutter.views import jump_to_target, cutter
from linkcutter.models import Links


class TestUrls(SimpleTestCase):

    def test_cutter(self):
        url = reverse('linkcutter:cutter')
        self.assertEquals(resolve(url).func, cutter)


class SimpleTest(TestCase):

    def test_index(self):
        """  The index page loads properly  """
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_link_not_existed_in_db(self):
        response = self.client.get('/somelink123', follow=True)
        text = response.content
        self.assertTrue(text.find(b"Such link doesn't exist"))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('linkcutter:link_list'))
        self.assertRedirects(response, '/login/?next=/link_list/')
