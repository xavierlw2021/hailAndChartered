from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import qrcode_storage

class qrcodeStorageAdmin(ImportExportModelAdmin):    
    list_display = ('id','pub_datetime','start_datetime','limit_datetime','finish_datetime', \
                     'main_userId','family_userId','be_canceled',)
    ordering = ('pub_datetime',)

admin.site.register(qrcode_storage, qrcodeStorageAdmin)
