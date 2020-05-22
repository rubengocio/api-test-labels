from django.contrib import admin

# Register your models here.
from manager_testing.models import Test, TestPlan, Carrier, Service, TestPlanResult, StepResult, QueryParam, \
    AccessPoint, Facility


class CarrierAdmin(admin.ModelAdmin):
    list_display = (
        'site',
        'code',
        'name'
    )
    list_filter = ('site',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'carrier',
        'code',
        'name'
    )

    list_filter = ('carrier__site',)


class TestPlanAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'logistic_type',
        'shipment_id',
        'response_type',
        'facility',
        'caller_id'
    )

    list_filter = ('service__carrier__site', )
    search_fields = ('shipment_id', )


class TestPlanResultAdmin(admin.ModelAdmin):
    list_display = (
        'test',
        'test_plan',
        'pass_test',
    )


class QueryParamAdmin(admin.TabularInline):
    model = QueryParam


class AccessPointAdmin(admin.ModelAdmin):
    inlines = [QueryParamAdmin, ]


class TestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'release',
        'access_point_a',
        'access_point_b'
    )


admin.site.register(Test, TestAdmin)
admin.site.register(StepResult)
admin.site.register(Facility)
admin.site.register(Carrier, CarrierAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(TestPlan, TestPlanAdmin)
admin.site.register(TestPlanResult, TestPlanResultAdmin)
admin.site.register(AccessPoint, AccessPointAdmin)
