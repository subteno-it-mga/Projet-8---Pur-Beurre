from django.urls import reverse

def test_create(self):
    response = self.client.get(reverse('create', args=[self.userName]))
    self.assertEqual(response.status_code, 200)