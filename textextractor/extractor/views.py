from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
import os

def upload_file(request):
    extracted_text = None
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".pdf":
                extracted_text = extract_text_from_pdf(file_path)
            elif ext in [".docx", ".doc"]:
                extracted_text = extract_text_from_docx(file_path)
            elif ext in [".png", ".jpg", ".jpeg"]:
                extracted_text = extract_text_from_image(file_path)
            else:
                extracted_text = "Unsupported file type."
    else:
        form = UploadFileForm()
    
    return render(request, "extractor/upload.html", {
        "form": form,
        "extracted_text": extracted_text,
    })
