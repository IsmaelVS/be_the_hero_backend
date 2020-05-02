"""Tests for views.py endpoints."""
from json import dumps, loads

from django.test import Client, TestCase

from ..models import Incidents, ONGs


class TestsONGs(TestCase):
    """ONG testing class."""

    def setUp(self) -> None:
        """Prepare environment for tests."""
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

    def test_created_ong(self) -> None:
        """Test creating new ONG."""
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

    def test_data_with_incomplete(self) -> None:
        """New ONG with data incomplete."""
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

    def test_list_ongs(self) -> None:
        """List all ONGs."""
        response = self.client.get('/ongs/')

        ongs = ONGs.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id')
        self.assertContains(response, 'name')
        self.assertContains(response, 'whatsapp')
        self.assertContains(response, 'city')
        self.assertContains(response, 'uf')
        self.assertEqual(response_data[0]['email'], 'hihi@ong.com')
        self.assertEqual(ongs, len(response_data))


class TestsIncidents(TestCase):
    """Incident testing class."""

    def setUp(self) -> None:
        """Prepare environment for tests."""
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

        ong = ONGs.objects.get(id=1)

        data_inc = dumps({
            "title": "Caso - teste",
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": ong.id,
        })

        header = {'HTTP_Authorization': ong.id}

        self.client.post('/incidents/',
                         content_type="application/json",
                         data=data_inc, **header
                         )

    def test_created_incident(self) -> None:
        """Test creating new incident."""
        ong = ONGs.objects.get(id=1)

        data = dumps({
            "title": "Caso - teste",
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": ong.id,
        })

        header = {'HTTP_Authorization': '1'}

        response = self.client.post('/incidents/',
                                    content_type="application/json",
                                    data=data, **header
                                    )

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['id'], 2)
        self.assertEqual(incidents, 2)

    def test_data_with_incomplete(self) -> None:
        """New incident with data incomplete."""
        ong = ONGs.objects.get(id=1)

        data = dumps({
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": ong.id,
        })

        header = {'HTTP_Authorization': '1'}

        response = self.client.post('/incidents/',
                                    content_type="application/json",
                                    data=data, **header
                                    )

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Fail'], 'Data is missing.')
        self.assertEqual(incidents, 1)

    def test_without_header(self) -> None:
        """New incident without header."""
        ong = ONGs.objects.get(id=1)

        data = dumps({
            "title": "Caso - teste2",
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": ong.id,
        })

        response = self.client.post('/incidents/',
                                    content_type="application/json",
                                    data=data
                                    )

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Fail'], 'Data is missing.')
        self.assertEqual(incidents, 1)

    def testing_with_ong_invalid(self) -> None:
        """New incident with wrong header."""
        data = dumps({
            "title": "Caso - teste3",
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": 500,
        })

        header = {'HTTP_Authorization': '500'}

        response = self.client.post('/incidents/',
                                    content_type="application/json",
                                    data=data, **header
                                    )

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Error'], 'Ong invalid.')
        self.assertEqual(incidents, 1)

    def test_list_incidents(self) -> None:
        """List all Incidents."""
        response = self.client.get('/incidents/')

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id')
        self.assertContains(response, 'title')
        self.assertContains(response, 'value')
        self.assertEqual(response_data[0]['description'],
                         'hihihihihihihihihihihihihihi')
        self.assertEqual(incidents, len(response_data))

    def test_list_incidents_with_pagination(self) -> None:
        """List Incidents with paginate."""
        response = self.client.get('/incidents/?page=1')

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id')
        self.assertContains(response, 'title')
        self.assertContains(response, 'value')
        self.assertEqual(response_data[0]['description'],
                         'hihihihihihihihihihihihihihi')
        self.assertEqual(incidents, len(response_data))

    def test_list_incidents_with_invalid_pagination(self) -> None:
        """List Incidents with invalid pagination."""
        response = self.client.get('/incidents/?page=175')

        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Error'], 'Invalid pagination.')


class TestsDeleteIncidentView(TestCase):
    """Delete incident testing class."""

    def setUp(self) -> None:
        """Prepare environment for tests."""
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

        ong = ONGs.objects.get(id=1)

        data_inc = dumps({
            "title": "Caso - teste",
            "description": "hihihihihihihihihihihihihihi",
            "value": "1100",
            "ong": ong.id,
        })

        header = {'HTTP_Authorization': ong.id}

        self.client.post('/incidents/',
                         content_type="application/json",
                         data=data_inc, **header
                         )

    def test_delete_incident(self) -> None:
        """Delete Incident."""
        header = {'HTTP_Authorization': 1}
        response = self.client.delete('/incidents/1/', **header)

        incidents = Incidents.objects.count()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(incidents, 0)

    def test_delete_incident_with_invalid_ong(self) -> None:
        """Delete Incident with invalid header."""
        header = {'HTTP_Authorization': 2}
        response = self.client.delete('/incidents/1/', **header)

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['Error'], 'Operation not permitted.')
        self.assertEqual(incidents, 1)

    def test_delete_incident_with_invalid_incident(self) -> None:
        """Delete Incident with invalid params."""
        header = {'HTTP_Authorization': 1}
        response = self.client.delete('/incidents/2/', **header)

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['Error'], 'Incident invalid.')
        self.assertEqual(incidents, 1)

    def test_delete_incident_without_header(self) -> None:
        """Delete Incident without header."""
        response = self.client.delete('/incidents/1/')

        incidents = Incidents.objects.count()
        response_data = loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data['Error'], 'Operation not permitted.')
        self.assertEqual(incidents, 1)
