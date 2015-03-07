#! python
"""
# This file demonstrates writing tests using the unittest module. These will pass
# when you run "manage.py test".
# 
# Replace this with more appropriate tests for your application.
"""
from django.test.runner.DiscoverRunner import DiscoverRunner
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

from temperature.models import Temperature
from temperature.views import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class TemperatureTests(TestCase):
    """Temperature model tests."""

    def test_str(self):

        termperature = Temperature(ReadingDateTime='2015-02-07 22:15:01', 
		TempC='22.20*C', TempF ='71.96*f', Humidity='50.80%' ) 

        #self.assertEquals( str(contact), 'John Smith',)

class TemperatureListViewTests(TestCase):
    """Temperature list view tests."""

    def test_temperature_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(list(response.context['object_list']), [])

        Temperature.objects.create(ReadingDateTime='2015-02-07 22:15:01',
             TempC='22.20*C', TempF ='71.96*f', Humidity='50.80%' ) 
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_temperature_in_the_context(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = ListTemperatureView.as_view()(request)

        self.assertEquals(list(response.context_data['object_list']), [])
       
        Temperature.objects.create(ReadingDateTime='2015-02-07 22:15:01', 
             TempC='22.20*C', TempF ='71.96*f', Humidity='50.80%' )

        response = ListTemperatureView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)

class TemperatureListIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(TemperatureListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TemperatureListIntegrationTests, cls).tearDownClass()

    def test_temperature_listed(self):

        # create a test temperature
        Temperature.objects.create(ReadingDateTime='2015-02-07 22:15:01', TempC='22.20*C', TempF ='71.96*f', Humidity='50.80%' ) 

        # make sure it's listed as <first> <last> on the list
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.temperature')[0].text,
            'foo bar'
        )

    def test_add_temperature_linked(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_element_by_link_text('add temperature')
        )

    def test_add_temperature(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add temperature').click()

        #Temperature.objects.create(ReadingDateTime='2015-02-07 22:15:01', 
        #	TempC='22.20*C', TempF ='71.96*f', Humidity='50.80%' ) 
        self.selenium.find_element_by_id('id_ReadingDateTime').send_keys('2015-02-07 22:15:01')
        self.selenium.find_element_by_id('id_TempC').send_keys('22.20*C')
        self.selenium.find_element_by_id('id_TempF').send_keys('71.96*f')
        self.selenium.find_element_by_id('id_Humidity').send_keys('50.80%')

        self.selenium.find_element_by_id("save_temperature").click()
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.temperature')[-1].text,
            'test temperature'
        )
