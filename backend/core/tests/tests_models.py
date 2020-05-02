"""Tests to models."""
from django.test import TestCase

from ..models import Incidents, ONGs


class TestONGsCase(TestCase):
    """Class to tests in model ONGs."""

    def setUp(self):
        """Prepare environment for tests."""
        ONGs.objects.create(
            name="ONG - Da vida",
            email="hihi@ong.com",
            whatsapp="1111111111",
            city="Capão Redondo",
            uf="SP"
        )

    def test_ongs_return_str(self):
        """Validate return str models."""
        ong = ONGs.objects.get(id=1)
        self.assertEquals(ong.__str__(), 'ONG - Da vida')


class TestIncidentsCase(TestCase):
    """Class to tests in model Incidents."""

    def setUp(self):
        """Prepare environment for tests."""
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
        """Validate return str models."""
        incident = Incidents.objects.get(title='Caso - teste')

        self.assertEquals(incident.__str__(), 'Caso - teste')
