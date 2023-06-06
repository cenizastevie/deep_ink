from django.urls import path
from . import views

urlpatterns = [
    path('api/upload-pdf/', views.PDFUploadView.as_view(), name='pdf-upload'),
    path('api/nfts/', views.ListNFTsView.as_view(), name='list-nfts'),
]
