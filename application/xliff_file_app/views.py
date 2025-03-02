from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .utils.script4 import translate_file, save_xliff_file
import os
from django.http import FileResponse, HttpResponseNotFound
# Create your views here.




def index(request):
    return render(request, "index.html")




def translate_xliff_view(request):
    source_data = []
    translated_data = []

    if request.method == "POST" and request.FILES.get("xliff_file"):
        xliff_file = request.FILES["xliff_file"]

        # Save the uploaded file temporarily
        file_path = default_storage.save(f"temp/{xliff_file.name}", xliff_file)
        print(file_path)
        request.session["file_path"] = file_path
        source_data, translated_data = translate_file(file_path)

        return render(request, "index.html", {
            "source_data": source_data,
            "translated_data": translated_data,
        })

    return render(request, "index.html")




@csrf_exempt  # Use only for testing; better to handle CSRF properly in production
def update_translations(request):
    if request.method == "POST":
        try:
            # xliff_file = request.FILES["xliff_file"]
            data = json.loads(request.body)
            source_data = data.get("source_data", [])
            translated_data = data.get("translated_data", [])

            print("Received Source Data:", source_data)
            print("Received Translated Data:", translated_data)
            file_path = request.session.get("file_path", "")
            print("file pathhhhhhhhhhhhhhhhhhhhhhhhhhhh",file_path)

            
            save_xliff_file(file_path, translated_data)  

              
                            
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data", "status": "error"}, status=400)

    return JsonResponse({"message": "Only POST requests are allowed"}, status=405)



def download_File(request):
   if request.method == "GET":
      translated_file_path = "media/translated.xlf"

      if os.path.exists(translated_file_path):  
             response = FileResponse(
             open(translated_file_path, "rb"), 
             as_attachment=True, 
             filename="translated.xlf"
             )
             response['Content-Type'] = 'application/x-xliff+xml'  # Ensure correct MIME type
             print("responssssssssssssssssseeeeeeeeeeee", response)
             return response
      else:   
              return HttpResponseNotFound("File not found.")        
      