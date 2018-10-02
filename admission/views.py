from django.shortcuts import render, reverse
from django.conf import settings
import weasyprint
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from .models import AppointmentRequest
from .forms import AppointmentRequestForm
from django.core.mail import EmailMessage
from io import BytesIO
# Create your views here.


def home(request):
    context = {'request': request}
    return render(request, 'home.html', context)


def appointment_request_pdf(request, appointment_request_id, appointment_request_slug):
    appointment_request = AppointmentRequest.objects.get(
        id=appointment_request_id)
    html = render_to_string(
        'pdf.html', {'appointment_request': appointment_request})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\"appoinment_request_{}.pdf"'.format(
        appointment_request.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT + '/main.css')])
    return response


def appointment_request_success(request, appointment_request_id, appointment_request_slug):
    context = {'request': request}
    appointment_request_instance = AppointmentRequest.objects.get(
        id=appointment_request_id)
    context['appointment_request_instance'] = appointment_request_instance
    return render(request, 'appointment_request_success.html', context)


def cancel_appointment_request(request, appointment_request_id):
    appointment_request_instance = AppointmentRequest.objects.get(
        id=appointment_request_id)
    appointment_request_instance.delete()
    return HttpResponseRedirect(reverse('admission:home'))


def appointment_request(request):
    context = {'request': request}
    if request.method == 'GET':
        appointment_request_form = AppointmentRequestForm()
    elif request.method == 'POST':
        appointment_request_form = AppointmentRequestForm(data=request.POST)
        if appointment_request_form.is_valid():
            new_appointment = appointment_request_form.save(commit=False)
            new_appointment.save()
            # send to the provided email
            subject = 'Appointment Request - request no. {} ref. code {}'.format(
                new_appointment.id, new_appointment.slug)
            message = 'Please, see the attached the PDF for your recent Appointment Request.'
            email = EmailMessage(subject, message, 'admin@myshop.com', [new_appointment.email])
            # generate PDF
            html = render_to_string('pdf.html', {'appointment_request': new_appointment})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/main.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
            # attach PDF file
            email.attach('appointment_request_{}.pdf'.format(new_appointment.id), out.getvalue(), 'application/pdf')
            # send e-mail
            email.send()
            return HttpResponseRedirect(
                reverse('admission:appointment_request_success',
                        args=[new_appointment.id, new_appointment.slug])
            )
    context['appointment_request_form'] = appointment_request_form
    return render(request, 'appointment_request_form.html', context)
