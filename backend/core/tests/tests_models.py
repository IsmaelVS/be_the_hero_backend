from django.test import TestCase

from ..models import Incidents
from ..models import ONGs


class OngsTestCase(TestCase):

    def setUp(self):
        ONGs.objects.create(
            name="ONG - Da vida",
            email="hihi@ong.com",
            whatsapp="1111111111",
            city="Capão Redondo",
            uf="SP"
        )

    def test_ongs_retorn_str(self):
        ong = ONGs.objects.get(id=1)
        self.assertEquals(ong.__str__(), 'ONG - Da vida')


class IncidentsTestCase(TestCase):

    def setUp(self):
        ONGs.objects.create(
            name="ONG",
            email="hihi@ong.com",
            whatsapp="1111111111",
            city="Capão Redondo",
            uf="SP"
        )

        ong = ONGs.objects.get(id=1)

        Incidents.objects.create(
            title="Caso - teste",
            description="hihihihihihihihihihihihihihihihihihihi",
            value="1100",
            ong=ong,
        )

    def test_incident_retorn_str(self):
        incident = Incidents.objects.get(title='Caso - teste')

        self.assertEquals(incident.__str__(), 'Caso - teste')
