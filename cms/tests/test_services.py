from unittest import TestCase, mock
from unittest.mock import Mock, patch

from cms.services import address_to_point


class AddressToPointTest(TestCase):
    def setUp(self):
        self.address = 'Rio de Janeiro'

    @patch('cms.services.geocoder')
    def test_use_openstreetmap(self, geocoder):
        address_to_point(self.address)
        self.assertEqual(1, len(geocoder.method_calls))
        geocoder.osm.assert_called_once_with(self.address)

    @patch('cms.services.geocoder')
    def test_get_point(self, geocoder):
        latlng = [-22.9110137, -43.2093727]
        lat, lng = latlng
        geocoder.osm.return_value = Mock(latlng=latlng)
        self.assertEqual((lat, lng), address_to_point(self.address))

    @patch('cms.services.geocoder')
    def test_invalid_address(self, geocoder):
        address = 'Nowhere'
        error_msg = 'invalid address: "Nowhere"'
        geocoder.osm.return_value = Mock(ok=False)
        self.assertRaisesRegex(ValueError, error_msg, address_to_point, address)
