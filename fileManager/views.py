from django.shortcuts import render, redirect
from .forms import MediaFileForm
from .models import MediaFile
from django.contrib import messages

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def upload_file(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False)
            # Obtener información adicional
            media_file.user_agent = request.META.get('HTTP_USER_AGENT', '')
            media_file.ip_address = get_client_ip(request)
            media_file.save()  # La detección del tipo de archivo ocurre automáticamente en el modelo

            # Mensaje de éxito
            messages.success(request, 'Archivos subidos con éxito!')
            return redirect('upload_file')  # Redirigir al usuario para evitar reenvío del formulario
        else:
            messages.error(request, 'Hubo un error al subir el archivo. Intenta nuevamente.')
    else:
        form = MediaFileForm()

    return render(request, 'upload.html', {'form': form})


def media_list(request):
    files = MediaFile.objects.all()
    return render(request, 'list.html', {'files': files})