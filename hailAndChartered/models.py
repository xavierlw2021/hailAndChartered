from django.db import models
from django.utils import timezone

# 叫車清單
class hailOption(models.Model):
    agencyName = models.CharField(max_length=50)   #車行名
    agencyNumber = models.CharField(max_length=10)  #車行電話
    onOff = models.BooleanField(default=True) #開關

# 包車清單
class charteredOption(models.Model):
    carType = models.CharField(max_length=50)   #車種    
    chtdStartPrice = models.IntegerField(default=2000) #起跳價
    driverName = models.CharField(max_length=50)   #司機名
    driverPhone = models.CharField(max_length=10)  #司機電話
    onOff = models.BooleanField(default=True) #開關

# 客戶紀錄
class questProfile(models.Model):
    quest_phone = models.CharField(max_length=10)
    line_userId = models.CharField(max_length=40, blank=True, null=True)   #官方內建ID 
    quest_linename = models.CharField(max_length=40, blank=True, null=True)    
    lineid = models.CharField(max_length=120, blank=True, null=True)    #使用者設定ID
    order_times = models.PositiveIntegerField(default=0) #消費次數-自動累計
    total_cost = models.IntegerField(default=0) #消費金額-自動累計    
    total_mileage = models.PositiveIntegerField(default=0) #里程總計-自動累計
    signUp_time = models.DateTimeField(default=timezone.now)    #建立時間

    class Meta:
        ordering = ('-signUp_time',)    
    def __str__(self):
        return f'{self.quest_phone}'        

# 消費紀錄
class car_order(models.Model):     
    pub_datetime = models.DateTimeField(default=timezone.now)   #登錄時間
    serviceType = models.CharField(max_length=20)   #服務種類-叫車or包車
    mileage = models.PositiveIntegerField(default=0) #預約里程
    total_cost = models.IntegerField(default=0)  #消費總金額
    is_pay = models.BooleanField(default=False) #繳費與否
    quest_phone = models.ForeignKey(questProfile, on_delete=models.CASCADE, related_name='to_order')
    transaction_id = models.CharField(max_length=50, blank=True, null=True) #使用LinePay時, 串接官方的回傳值
    be_canceled = models.BooleanField(default=False)    #訂單取消與否

    class Meta:
        ordering = ('-pub_datetime',)
    def __str__(self):
        return f'{self.pub_datetime}, 電話:{self.quest_phone}, 消費金額:{self.total_cost}'
