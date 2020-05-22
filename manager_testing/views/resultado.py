from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404

from manager_testing.models import Test, TestPlanResult, StepResult, ImageResult
from manager_testing.tasks import processing_test


class TestPlanResultListView(View):

    def get(self, request, pk):
        template = loader.get_template('resultados.html')
        test = get_object_or_404(Test, pk=pk)
        list_results = TestPlanResult.objects.filter(test=test)
        return HttpResponse(template.render({'list_results': list_results}, request))


class TestPlanSuccessResultListView(View):

    def get(self, request, pk):
        template = loader.get_template('resultados.html')
        test = get_object_or_404(Test, pk=pk)
        list_results = TestPlanResult.objects.filter(
            test=test,
            pass_test=True
        )
        return HttpResponse(template.render({'list_results': list_results}, request))


class TestPlanFailResultListView(View):

    def get(self, request, pk):
        template = loader.get_template('resultados.html')
        test = get_object_or_404(Test, pk=pk)
        list_results = TestPlanResult.objects.filter(
            test=test,
            pass_test=False
        )
        return HttpResponse(template.render({'list_results': list_results}, request))


class TestPlanDetailResultListView(View):

    def get(self, request, pk):
        template = loader.get_template('detalle-resultado.html')
        test_plan_result = get_object_or_404(TestPlanResult, pk=pk)
        step_result = StepResult.objects.filter(
            test_plan_result=test_plan_result
        ).order_by('step')

        images_result = ImageResult.objects.filter(
            test_plan_result=test_plan_result
        ).order_by('order')

        context = {
            'result': test_plan_result,
            'step_result': step_result,
            'images_result': images_result
        }
        return HttpResponse(template.render(context, request))


class TestPlanReloadResultView(View):

    def get(self, request, pk):
        test_plan_result = get_object_or_404(TestPlanResult, pk=pk)
        test = test_plan_result.test
        test_plan = test_plan_result.test_plan
        processing_test(test.id, test_plan.id, 1, 1, False)
        pass_test = test_plan_result.pass_test
        test_plan_result.delete()

        if pass_test:
            return HttpResponseRedirect(reverse('success_results', kwargs={"pk": test.id}))
        else:
            return HttpResponseRedirect(reverse('fail_results', kwargs={"pk": test.id}))
