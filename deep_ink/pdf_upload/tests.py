import os
import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings

class PDFUploadViewTest(APITestCase):
    def setUp(self):
        self.file_path = os.path.join(settings.BASE_DIR, '../example.pdf')

    @responses.activate
    def test_upload_pdf_success(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}
            responses.add(responses.POST, 'https://api.nft.storage/upload', json={'success': True}, status=200)

            response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('sha256_checksum', response.data)
        self.assertIn('metadata', response.data)
        self.assertIn('upload_response', response.data)

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

