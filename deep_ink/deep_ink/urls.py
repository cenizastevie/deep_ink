from django.urls import include, path

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include('pdf_upload.urls')),
]
