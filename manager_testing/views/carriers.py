from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View

from manager_testing.forms.carriers import CarrierForm
from manager_testing.models import AccessPoint, Carrier


class CarriersListView(View):

    def get(self, request):
        template = loader.get_template('carriers.html')
        list_carrier = Carrier.objects.all()
        return HttpResponse(template.render({'list_carrier': list_carrier}, request))


class CarrierNewView(View):
    template_name = 'form-carrier.html'

    def get(self, request):
        form = CarrierForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CarrierForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('carriers'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class CarrierEditView(View):
    template_name = 'form-carrier.html'

    def get(self, request, pk):
        carrier = get_object_or_404(Carrier, pk=pk)
        form = CarrierForm(instance=carrier)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        carrier = get_object_or_404(Carrier, pk=pk)
        form = CarrierForm(data=request.POST, instance=carrier)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('carriers'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

