from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views import generic
from django.contrib import messages

import csv
import pandas as pd
import json # use to convert pandas dataframe into json object which we can use in html
import pathlib
from google_drive_downloader import GoogleDriveDownloader as gdd
from itertools import islice

from response import forms # Import forms module from response app


# adding new functions here -- Eduardo v v v v
# View: As the name implies, it represents what you see while on your 
# browser for a web application or In the UI for a desktop application.

def home(request):

    if not pathlib.Path('static/archive/').exists():
        data_exists = False
        if request.GET.get('Download') == 'Download':
            gdd.download_file_from_google_drive(file_id='13kkIW87tneP6wLQuEMd1PTPYJ4h7orq3',
                                        dest_path='static/data.zip',
                                        unzip=True)
            data_exists = True
            return render(request,'response/home.html', {'data_exists': data_exists})

    else:
        data_exists = True

    return render(request,'response/home.html', {'data_exists': data_exists})
