from django.urls import path
from .views import index
# from .views import translate_xliff_view
from .views import update_translations
from .views import download_edited_File
from .views import download_File

urlpatterns = [
    path('', index, name='index'),
     path("update-translations/", update_translations, name="update-translations"),
     path("download-edited-translations/", download_edited_File, name="download-edited-translations"),
     path("download-translations/", download_File, name="download-translations"),
]