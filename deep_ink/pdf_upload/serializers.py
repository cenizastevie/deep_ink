from rest_framework import serializers

class PDFSerializer(serializers.Serializer):
    pdf_file = serializers.FileField()
