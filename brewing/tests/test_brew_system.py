from django.test import TestCase
from ..views import brew_system
from ..process.hardware import brew_server_hardware

# Create your tests here.


class heating_test(TestCase):
    def setUp(self):
        self.brew = brew_system
        self.hardware = brew_server_hardware()

    def test_heating(self):
        """get heating time"""
        print(self.brew.heat(10))
    
    def test_engine(self):
        self.hardware.engine_off()
        self.assertEqual(self.hardware.get_engine_mode(),False)
