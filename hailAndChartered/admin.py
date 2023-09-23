from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import hailOption, charteredOption, questProfile, car_order

class hailOptionAdmin(ImportExportModelAdmin):
    list_display = ('id','agencyName','agencyNumber','onOff',)
    ordering = ('id',)

class charteredOptionAdmin(ImportExportModelAdmin):
    list_display = ('id','carType','chtdStartPrice','driverName','driverPhone','onOff',)
    ordering = ('id',)

class questProfileAdmin(ImportExportModelAdmin):
    list_display = ('id','quest_phone','line_userId','quest_linename','lineid',\
                    'order_times','total_cost','total_mileage','signUp_time',)
    ordering = ('signUp_time',)

class carOrderAdmin(ImportExportModelAdmin):
    list_display = ('id','pub_datetime','serviceType','mileage','total_cost',\
                    'is_pay','quest_phone','transaction_id','be_canceled',)
    ordering = ('pub_datetime',)

admin.site.register(hailOption, hailOptionAdmin)
admin.site.register(charteredOption, charteredOptionAdmin)
admin.site.register(questProfile, questProfileAdmin)
admin.site.register(car_order, carOrderAdmin)