import os
import uuid
import time
import requests
from io import BytesIO

from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import ApplicationForm

LOGIN_URL = "https://recruitment.fisdev.com/api/login/"
TEST_APPLICATION_URL = "https://recruitment.fisdev.com/api/v0/recruiting-entities/"
FINAL_APPLICATOIN_URL = "https://recruitment.fisdev.com/api/v1/recruiting-entities/"
CV_UPLOAD_API = "https://recruitment.fisdev.com/api/file-object/"


def login(credentials):
    user_token = requests.post(LOGIN_URL, data=credentials).json()['token']
    return user_token


def upload_file(file, file_token_id, token):
    file_path = f'uploaded_files/'
    file_name = file.name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    default_storage.save(f'{file_path}/{file}', ContentFile(file.read()))
    files = {"files": open(os.path.join(file_path, str(file_name)), 'rb')}
    cv_upload_response = requests.put(f'{CV_UPLOAD_API}{file_token_id}/', files=files,
                                              headers={'Authorization': f'TOKEN {token}'})
    print(f'cv upload response is : {cv_upload_response.json()}')
    messages.success(request, "Successful Submission")
    return redirect('core:home')
    

def index(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            token = login({"username": "moinul.hossain.in2019@gmail.com", "password": "u5QiNmi20"})
            request_payload = form.cleaned_data
            applying_in = form.cleaned_data['applying_in']
            # Internally generated
            tsync_id = "90fee1b1-33d6-466a-ae52-69b5b3565a20"
            cv = request.FILES['cv_file']
            request_payload.update(
                {"tsync_id": tsync_id,
                 "applying_in": dict(form.fields['applying_in'].choices)[applying_in],
                 "cv_file": {"tsync_id": tsync_id},
                 "on_spot_update_time": int(time.time()),
                 "on_spot_creation_time": int(time.time())}
            )
            response = requests.post(FINAL_APPLICATOIN_URL, json=request_payload,
                                     headers={'Authorization': f'TOKEN {token}'})
            if 'cv_file' in response.json():
                file_token_id = response.json()['cv_file']['id']
                upload_file(cv, file_token_id, token)
            else:
                messages.warning(request, f"{response.json()['message']}")
                return redirect('core:home')
    else:
        # If form to be generated with tsync_id
        # u_id = uuid.uuid4()
        # form = ApplicationForm({"tsync_id": u_id})
        form = ApplicationForm()
    return render(request, 'index.html', {"form": form})
