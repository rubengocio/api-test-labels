from django.template import loader
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from manager_testing.forms.test_plan import TestPlanForm
from manager_testing.models import TestPlan


class TestPlanListView(View):

    def get(self, request):
        template = loader.get_template('test-plans.html')
        list_tests = TestPlan.objects.all()
        return HttpResponse(template.render({'list_tests': list_tests}, request))


class TestPlanDetailView(View):
    template_name = 'form-test-plan.html'

    def get(self, request, pk):
        test_plan = get_object_or_404(TestPlan, pk=pk)
        form = TestPlanForm(instance=test_plan)
        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    #def post(self, request, pk=None):
    #    reclamo=None
    #    if pk:
    #        reclamo=get_object_or_404(Reclamo, pk=pk)
    #    form = ReclamoForm(data=request.POST, instance=reclamo)
        #
        #    if form.is_valid():
        #        form.save()
        #       return HttpResponseRedirect(reverse('reclamos'))
        #
        #context={
        #    'form':form
        #}
        #return render(request, self.template_name, context)