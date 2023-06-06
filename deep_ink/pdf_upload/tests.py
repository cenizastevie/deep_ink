from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import responses

class PDFUploadViewTest(APITestCase):
    def setUp(self):
        self.file_path = 'path/to/your/pdf/file.pdf'

    @responses.activate
    def test_upload_pdf_success(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}
            responses.add(responses.POST, 'https://api.nft.storage/upload', json={'success': True}, status=200)

            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('sha256_checksum', response.data)
        self.assertIn('metadata', response.data)
        self.assertIn('upload_response', response.data)

    def test_upload_pdf_invalid_file(self):
        url = reverse('pdf-upload')
        data = {'pdf_file': 'invalid-file'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_pdf_no_file(self):
        url = reverse('pdf-upload')
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_upload_pdf_unauthorized(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}
            responses.add(responses.POST, 'https://api.nft.storage/upload', json={'error': 'Unauthorized'}, status=401)

            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @responses.activate
    def test_upload_pdf_forbidden(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}
            responses.add(responses.POST, 'https://api.nft.storage/upload', json={'error': 'Forbidden'}, status=403)

            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @responses.activate
    def test_upload_pdf_server_error(self):
        url = reverse('pdf-upload')
        with open(self.file_path, 'rb') as file:
            data = {'pdf_file': file}
            responses.add(responses.POST, 'https://api.nft.storage/upload', json={'error': 'Server error'}, status=500)

            response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
