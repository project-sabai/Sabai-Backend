from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from clinicmodels.models import Patient
from django.views.decorators.csrf import csrf_exempt

from visit.forms import VisitForm


@csrf_exempt
def create_new_visit(request):
    try:
        patient_id = request.POST['patient_id']

        # Patient exists, go on to create a new visit
        patient = Patient.objects.get(pk=patient_id)

        visit_form = VisitForm(request.POST)
        if visit_form.is_valid():
            visit = visit_form.save()
            response = serializers.serialize("json", [visit, ])
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse(visit_form.errors, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
