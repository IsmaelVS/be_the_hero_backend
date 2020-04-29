from json import dumps, loads

from django.test import Client, TestCase

from ..models import Incidents
from ..models import ONGs


class TestsONGs(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        data_ong = dumps({
            "name": "ONG",
            "email": "hihi@ong.com",
            "whatsapp": "1111111111",
            "city": "Capão Redondo",
            "uf": "SP"
        })

        self.client.post('/ongs/',
                         content_type="application/json", data=data_ong)

    def test_created_ong(self):

        data = dumps({
            "name": "ONG2",
            "email": "hihi@ong.com",
            "whatsapp": "1111111111",
            "city": "Capão Redondo",
            "uf": "SP"
        })

        response = self.client.post(
            '/ongs/', content_type="application/json", data=data)

        ongs = ONGs.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['id'], 2)
        self.assertEqual(ongs, 2)

    def test_data_with_incomplete(self):

        data = dumps({
            "name": "ONG3",
            "email": "hihi@ong.com",
            "city": "Capão Redondo",
            "uf": "SP"
        })

        response = self.client.post(
            '/ongs/', content_type="application/json", data=data)

        ongs = ONGs.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Fail'], 'Data is missing.')
        self.assertEqual(ongs, 1)
