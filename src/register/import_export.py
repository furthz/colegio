from django.shortcuts import render
import csv
from import_export import resources
from django.http import HttpResponse
from tablib import Dataset
from profiles.models import Profile

class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Profile


def exportJSON(request):
    person_resource = AlumnoResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="alumnos.json"'
    return response

def exportCSV(request):
    person_resource = AlumnoResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'
    return response


"""
def simple_upload(request):
    if request.method == 'POST':
        person_resource = AlumnoResource()
        #new_persons = request.FILES['myfile']

        #dataset = Dataset().load(open(request.FILES['myfile']).read())
        #dataset = Dataset().load(open(request.FILES['myfile']).write().read())
        dataset = Dataset().load(csv.DictReader(request.FILES['myfile']))


        #imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import.html')
"""

"""
def simple_upload(request):
    if request.method == 'POST':
        person_resource = AlumnoResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'import.html')
"""

def simple_upload(request):
    if request.method == 'POST':
        person_resource = AlumnoResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(imported_data, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(imported_data, dry_run=False)  # Actually import now

    return render(request, 'import.html')

