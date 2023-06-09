import hashlib
import PyPDF2
import requests
import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PDFSerializer
from .ripple import mint_nft, get_owned_nfts

class PDFUploadView(APIView):
    def post(self, request):
        serializer = PDFSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']

            # Calculate the SHA256 checksum of the PDF file
            sha256_checksum = self.calculate_sha256_checksum(pdf_file)

            # Retrieve the metadata of the PDF file
            metadata = self.retrieve_pdf_metadata(pdf_file)

            # Upload the JSON object to the specified endpoint
            response = self.upload_pdf_json(sha256_checksum, metadata)

            if not response.ok:
                error_message = response.json().get('error', {}).get('message')
                return {'error': error_message}
                
            cid = response['value']['cid']
            ipfs_url = f"https://nftstorage.link/ipfs/{cid}"

            # Mint the NFT using the generated IPFS URL
            mint_result = mint_nft(ipfs_url)

            return Response({
                'message': 'PDF uploaded successfully.',
                'sha256_checksum': sha256_checksum,
                'metadata': metadata,
            })
        else:
            return Response(serializer.errors, status=400)

    def calculate_sha256_checksum(self, file):
        sha256 = hashlib.sha256()
        for chunk in file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def retrieve_pdf_metadata(self, file):
        try:
            
            pdf = PyPDF2.PdfReader(file)
            return pdf.metadata
        except Exception as e:
            return {}

    def upload_pdf_json(self, sha256_checksum, metadata):
        url = 'https://api.nft.storage/upload'
        nft_storage_token = os.environ.get('NFT_STORAGE_TOKEN')
        headers = {
            'Authorization': f'Bearer {nft_storage_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'file':json.dumps({
                'sha256': sha256_checksum,
                'metadata': metadata
            })
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

class ListNFTsView(APIView):
    def get(self, request):
        marker = request.query_params.get('marker')
        nfts = get_owned_nfts(marker)
        return Response({'nfts': nfts})