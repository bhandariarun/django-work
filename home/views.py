
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import UploadForm
from .models import Image
from django.http import HttpResponse
import shutil
import os
import zipfile

class UploadView(View):
    def get(self, request):
        form = UploadForm()
        return render(request, 'image_upload/upload.html', {'form': form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            files = request.FILES.getlist('files')

            # Set configurable file save path (change as needed)
            # save_path = '/static/images/'

            # Iterate over the uploaded files
            for file in files:
                # Perform file type validation
                if file.content_type.split('/')[0] != 'image':
                    return render(request, 'image_upload/upload.html', {'form': form, 'error': 'Only image files are allowed.'})

                # Perform file size validation (change the size limit as needed)
                if file.size > 5 * 1024 * 1024:  # 5 MB
                    return render(request, 'image_upload/upload.html', {'form': form, 'error': 'File size exceeds the limit.'})

                # Save the file with a .jpg extension
                # with open(save_path + file.name + '.jpg') as destination:
                #     for chunk in file.chunks():
                #         destination.write(chunk)

                # Create Image object and save it to the database
                image = Image(title=title, file=file)
                image.save()

            # Display uploaded images
            images = Image.objects.all()
            return render(request, 'image_upload/gallery.html', {'title': title, 'images': images})
        else:
            return render(request, 'image_upload/upload.html', {'form': form})

class ImageView(View):
    def get(self, request, image_id):
        image = Image.objects.get(id=image_id)
        return render(request, 'image_upload/image_detail.html', {'image': image})

    def post(self, request, image_id):
        image = Image.objects.get(id=image_id)
        image.delete()
        # Delete the related file from the server
        if os.path.exists(image.file.path):
            os.remove(image.file.path)
        return redirect('gallery')

class DownloadView(View):
    def get(self, request):
        # Create a temporary directory to store the files
        temp_dir = '/path/to/temp/dir/'
        os.makedirs(temp_dir, exist_ok=True)

        # Get all the images
        images = Image.objects.all()

        # Copy the image files to the temporary directory
        for image in images:
            shutil.copy2(image.file.path, temp_dir)

        # Create a ZIP archive of the files
        shutil.make_archive(temp_dir, 'zip', temp_dir)

        # Serve the ZIP file for download
        response = HttpResponse(content_type='application/zip')
        zip_file = open(temp_dir + '.zip', 'rb')
        response['Content-Disposition'] = 'attachment; filename="images.zip"'
        response.write(zip_file.read())
        zip_file.close()

        # Delete the temporary directory and ZIP file
        shutil.rmtree(temp_dir)

        return response
    



def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    # Add any additional logic you need for the view
    return render(request, 'image_detail.html', {'image': image})

        
        
