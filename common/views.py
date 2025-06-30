from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .forms import UploadForm

# Create your views here.
def intro(request):
    return render(request,'common/intro.html' )

@login_required(login_url='common:login')
def userpage(request):
    context={'user':request.user}
    return render(request,'common/userpage.html',context)

@login_required(login_url='common:login')
def file_list(request):
    if request.user.is_superuser:
        files = UploadedFile.objects.all().order_by('-uploaded_at')  
    else:
        files = UploadedFile.objects.filter(owner=request.user).order_by('-uploaded_at')  
    context = {
        'user': request.user,
        'files': files,
    }
    return render(request, 'common/file_list.html', context)



@login_required(login_url='common:login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.owner = request.user
            uploaded_file.save()
            return redirect('common:file_list')
    else:
        form = UploadForm()
        context={'form':form}
    return render(request, 'common/upload.html', context)

@login_required(login_url='common:login')
def download_file(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        if uploaded_file.owner != request.user and not uploaded_file.owner.is_superuser and not request.user.is_superuser:
            raise Http404("E:Something went wrong. Please contact the site owner.")
        return FileResponse(uploaded_file.file.open('rb'),as_attachment=True)
    except UploadedFile.DoesNotExist:
        raise Http404("E:Something went wrong. Please contact the site owner.")
    
@login_required(login_url='common:login')
def delete_file(request, file_id):
        uploaded_file = UploadedFile.objects.get(id=file_id)
        if uploaded_file.owner != request.user and not request.user.is_superuser:
            raise Http404("E:Something went wrong. Please contact the site owner.")
        uploaded_file.file.delete()
        uploaded_file.delete()
        return redirect('common:file_list')

    

