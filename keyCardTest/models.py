from django.db import models
from django.utils import timezone

# 房卡密碼庫
class qrcode_storage(models.Model):   
    pwd = models.CharField(max_length=50)   #密碼暫存
    pub_datetime = models.DateTimeField(default=timezone.now)   #登錄時間
    start_datetime = models.DateTimeField(blank=True, null=True)    #生效開始時間
    limit_datetime = models.DateTimeField(blank=True, null=True)    #終止新增id時間
    finish_datetime = models.DateTimeField(blank=True, null=True)    #終止效用時間
    main_userId = models.CharField(max_length=40, blank=True, null=True)   #官方內建ID
    family_userId = models.CharField(max_length=400, blank=True, null=True)   #關聯者ID list
    be_canceled = models.BooleanField(default=True)    #生效與否

    class Meta:
        ordering = ('-pub_datetime',)
