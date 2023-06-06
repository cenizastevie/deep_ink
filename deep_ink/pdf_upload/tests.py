import os
import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from unittest.mock import patch

class PDFUploadViewTest(APITestCase):
    def setUp(self):
        self.file_path = os.path.join(settings.BASE_DIR, '../example.pdf')

    def test_upload_pdf(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}

            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('sha256_checksum', response.data)
        self.assertIn('metadata', response.data)

    def test_upload_pdf_expired_api_key(self):
        response_data = {'ok': False, 'error': {'code': 'ERROR_DIDT_EXPIRED', 'message': 'API Key has expired.'}}
        self.client.post('url-to-pdf-upload', data={}, format='multipart')

        # Check that the response has the expected error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'API Key has expired.'})

    def test_upload_pdf_invalid_file(self):
        url = reverse('pdf-upload')
        data = {'pdf_file': 'invalid-file'}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_pdf_no_file(self):
        url = reverse('pdf-upload')
        data = {}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class ListNFTsViewTest(APITestCase):
#     def test_list_nfts_with_marker(self):
#         # Assuming you have some initial nfts
#         initial_nfts = [
#             {'NFTokenID': 'nft1'},
#             {'NFTokenID': 'nft2'},
#             {'NFTokenID': 'nft3'},
#             {'NFTokenID': 'nft4'},
#             {'NFTokenID': 'nft5'},
#         ]

#         # Mock the get_owned_nfts function to return the initial nfts
#         with patch('pdf_upload.views.get_owned_nfts') as mock_get_owned_nfts:
#             mock_get_owned_nfts.return_value = initial_nfts

#             # Make a GET request to the ListNFTsView with a marker
#             url = reverse('list-nfts') + '?marker=nft3'
            
#             response = self.client.get(url)

#             # Assert the response status code
#             self.assertEqual(response.status_code, 200)

#             # Assert the response data contains the expected nfts
#             self.assertEqual(response.data['nfts'], initial_nfts[3:])

#             # Assert the get_owned_nfts function was called with the correct marker
#             mock_get_owned_nfts.assert_called_with(marker='nft3')
