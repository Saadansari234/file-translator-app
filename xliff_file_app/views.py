from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .utils.script4 import translate_file, save_xliff_file
import os
from django.http import FileResponse, HttpResponseNotFound
from .utils.language import languages
# Create your views here.


source_data = []
translated_data = []

def index(request):
    global source_data, translated_data
    if request.method == "POST" and request.FILES.get("xliff_file"):
        xliff_file = request.FILES["xliff_file"]
        selected_language = request.POST.get("target_language")  # Get selected language

       
        file_path = default_storage.save(f"temp/{xliff_file.name}", xliff_file)

        print(file_path)
        request.session["file_path"] = file_path
        source_data, translated_data = translate_file(file_path, selected_language)
            # Store translated data in session

        context = {
                "paired_data": list(zip(source_data, translated_data)),  # Pair source & translated text
                "languages": languages
            }
        return render(request, "index.html", context)
    else:
       options = {"languages": languages}
       return render(request, "index.html", options )
    




@csrf_exempt  # Remove this in production and use proper CSRF handling
def update_translations(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        source_data = data.get("source_data", [])
        translated_data = data.get("translated_data", [])
        print("Received Source Data:", source_data)
        print("Received Translated Data:", translated_data)

        file_path = request.session.get("file_path", "")
        print("File path:", file_path)

        save_xliff_file(file_path, translated_data)  
        os.remove(file_path)

        return JsonResponse({"message": "Success", "status": "ok"})
        
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data", "status": "error"}, status=400)
    


def download_edited_File(request):
   if request.method == "GET":
      translated_file_path = "media/translated.xlf"
      file_path = request.session.get("file_path", "")
      if os.path.exists(translated_file_path):  
             response = FileResponse(
             open(translated_file_path, "rb"), 
             as_attachment=True, 
             filename="translated.xlf"
             )
             response['Content-Type'] = 'application/x-xliff+xml'  # Ensure correct MIME type
             return response
      else:   
              return HttpResponseNotFound("File not found.")
      

             
def download_File(request):
   if request.method == "GET":
      file_path = request.session.get("file_path", "") 
      save_xliff_file(file_path, translated_data)  
      os.remove(file_path)

      translated_file_path = "media/translated.xlf"
      

      if os.path.exists(translated_file_path):  
             response = FileResponse(
             open(translated_file_path, "rb"), 
             as_attachment=True, 
             filename="translated.xlf"
             )
             response['Content-Type'] = 'application/x-xliff+xml'  # Ensure correct MIME type
             return response
      else:   
              return HttpResponseNotFound("File not found.")    
