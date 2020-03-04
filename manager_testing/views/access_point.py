from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View

from manager_testing.forms.access_point import AccessPointForm
from manager_testing.models import AccessPoint


class AccessPointListView(View):

    def get(self, request):
        template = loader.get_template('accesspoints.html')
        list_access_point = AccessPoint.objects.all()
        return HttpResponse(template.render({'list_access_point': list_access_point}, request))


class AccessPointNewView(View):
    template_name = 'form-access_point.html'

    def get(self, request):
        form = AccessPointForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AccessPointForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('access_points'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class AccessPointEditView(View):
    template_name = 'form-access_point.html'

    def get(self, request, pk):
        access_point = get_object_or_404(AccessPoint, pk=pk)
        form = AccessPointForm(instance=access_point)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        access_point = get_object_or_404(AccessPoint, pk=pk)
        form = AccessPointForm(data=request.POST, instance=access_point)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('access_points'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)