from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View

from manager_testing.forms.services import ServiceForm
from manager_testing.models import Service


class ServiceListView(View):

    def get(self, request):
        template = loader.get_template('services.html')
        list_service = Service.objects.all()
        return HttpResponse(template.render({'list_service': list_service}, request))


class ServiceNewView(View):
    template_name = 'form-service.html'

    def get(self, request):
        form = ServiceForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ServiceForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('services'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class ServiceEditView(View):
    template_name = 'form-service.html'

    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(instance=service)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(data=request.POST, instance=service)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('services'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)