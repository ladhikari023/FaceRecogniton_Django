from django.shortcuts import render
from app.forms import FaceRecognitionForm
from app.machinelearning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition
import os
# Create your views here.
def index(request):
    form =  FaceRecognitionForm()

    if request.method == 'POST':
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)

            # extract from DATABASES
            primary_key =  save.pk
            imgobj = FaceRecognition.objects.get(pk=primary_key)
            fileroot = str(imgobj.image)
            filepath = os.path.join(settings.MEDIA_ROOT,fileroot)
            results = pipeline_model(filepath)

            return render(request,'index.html',{'form':form,'upload':True,'results':results})


    return render(request,'index.html',{'form':form,'upload':False})
