from django.db import models


# Create your models here.
from manager_testing import Constants


class AccessPoint(models.Model):
    name = models.CharField(max_length=127)
    url = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class QueryParam(models.Model):
    access_point = models.ForeignKey(AccessPoint, on_delete=models.CASCADE)
    key = models.CharField(max_length=127)
    value = models.CharField(max_length=127)

    def __str__(self):
        return u"%s: %s" % (self.key, self.value)


class Carrier(models.Model):
    site = models.CharField(max_length=3, choices=Constants.CHOICES_SITES)
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=127)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s" % (self.site, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'site': self.site,
            'code': self.code,
            'name': self.name,
            'enabled': self.enabled
        }


class Service(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=127)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s - %s - %s - %s" % (self.carrier.site, self.carrier.code, self.carrier.name, self.code, self.name)

    def to_json(self):
        return {
            'id': self.id,
            'carrier': self.carrier.to_json(),
            'code': self.code,
            'name': self.name,
            'enabled': self.enabled
        }


class Test(models.Model):
    access_point_a = models.ForeignKey(AccessPoint, on_delete=models.CASCADE, related_name="access_point_a")
    access_point_b = models.ForeignKey(AccessPoint, on_delete=models.CASCADE, related_name="access_point_b")
    release = models.CharField(max_length=127, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    is_running = models.BooleanField(default=False)
    running_start_date = models.DateTimeField(null=True, blank=True)
    running_end_date = models.DateTimeField(null=True, blank=True)
    total_tests = models.IntegerField(default=0)
    success_test = models.IntegerField(default=0)
    fail_test = models.IntegerField(default=0)

    def __str__(self):
        return self.release

    def get_url_access_point_a(self):
        url = self.access_point_a.url

        query_params = QueryParam.objects.filter(access_point=self.access_point_a)

        string_query = ""
        for param in query_params:
            string_query += "&%s=%s" % (param.key, param.value)

        url = url + "?" + string_query
        return url

    def get_url_access_point_b(self):
        url = self.access_point_b.url

        query_params = QueryParam.objects.filter(access_point=self.access_point_b)

        string_query = ""
        for param in query_params:
            string_query += "&%s=%s" % (param.key, param.value)

        url = url + "?" + string_query
        return url


def to_json(self):
        return {
            'id': self.id,
            'release': self.release,
            'creation_date': self.creation_date,
            'is_running': self.is_running,
            'running_start_date': self.running_start_date,
            'running_end_date': self.running_end_date,
            'total_tests': self.total_tests,
            'success_test': self.success_test,
            'fail_test': self.fail_test
        }


class TestPlan(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    logistic_type = models.CharField(max_length=20, choices=Constants.CHOICES_LOGISTIC_TYPES, null=True, blank=True)
    response_type = models.CharField(max_length=4, choices=Constants.CHOICES_RESPONSE_TYPE, null=True, blank=True)
    shipment_id = models.BigIntegerField(null=True, blank=True)
    dpmm = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return u"%s - %s" % (self.service, self.logistic_type)

    def isPdf(self):
        return True if self.response_type == Constants.RESPONSE_TYPE_PDF else False

    def isZpl(self):
        return True if self.response_type == Constants.RESPONSE_TYPE_ZPL else False

    def isJson(self):
        return True if self.response_type == Constants.RESPONSE_TYPE_JSON else False

    def to_json(self):
        return {
            'id': self.id,
            'service': self.service.to_json(),
            'logistic_type': self.logistic_type,
            'response_type': self.response_type,
            'shipment_id': self.shipment_id,
            'dpmm': self.dpmm,
            'width': self.width,
            'height': self.height
        }


class TestPlanResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_plan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    pass_test = models.BooleanField(default=False)


class StepResult(models.Model):
    test_plan_result = models.ForeignKey(TestPlanResult, on_delete=models.CASCADE)
    step = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    result = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.result


class ImageResult(models.Model):
    test_plan_result = models.ForeignKey(TestPlanResult, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    image_a = models.ImageField(null=True, blank=True, upload_to='images/')
    image_b = models.ImageField(null=True, blank=True, upload_to='images/')





