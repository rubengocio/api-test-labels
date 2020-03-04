from django.template import loader
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from manager_testing.forms.test import TestForm
from manager_testing.models import Test
from manager_testing.tasks import run_tests


class TestListView(View):

    def get(self, request):
        template = loader.get_template('pruebas.html')
        list_tests = Test.objects.all()
        return HttpResponse(template.render({'list_tests': list_tests}, request))


class TestRunView(View):
    def get(self, request, pk):
        test = get_object_or_404(Test, pk=pk)
        #run_tests.delay(test.id)
        run_tests(test.id)
        return HttpResponseRedirect(reverse('tests'))


class TestNewView(View):
    template_name = 'form-test.html'

    def get(self, request):
        form = TestForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = TestForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tests'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class TestEditView(View):
    template_name = 'form-test.html'

    def get(self, request, pk):
        test = get_object_or_404(Test, pk=pk)
        form = TestForm(instance=test)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        test = get_object_or_404(Test, pk=pk)
        form = TestForm(data=request.POST, instance=test)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('tests'))

        context = {
            'form': form
        }
        return render(request, self.template_name, context)