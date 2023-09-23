from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, TemplateView
import base64, pickle

from hailAndChartered import models
import datetime


from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from urllib.parse import quote, parse_qsl
import uuid

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# def confirmed(request):
#     transaction_id = request.GET['transactionId']
#     order = models.car_order.objects.filter(transaction_id = transaction_id).first()
#     if order:
#         line_pay = payService.LinePay()
#         line_pay.confirm(transaction_id=transaction_id, amount=order.total_cost)
                
#         order.is_pay = True #確認收款無誤時,改成已付款
#         order.save()
        
#         #傳收據給用戶
#         message = payService.receipt(order) 
#         line_bot_api.push_message(to=order.quest_phone.line_userId, messages=message)
#         thxMsg = '付款已完成，感謝您的消費'
#         return render(request, 'paySuccess.html', {'thxMsg': thxMsg}) #((要改))render之類的

@csrf_exempt
def callback(request):
    if request.method=='POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message = []

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                name = profile.display_name                
                msgtext = event.message.text
                
                #訊息判斷區
                if '@關於我們' in msgtext:
                    message.append(TextSendMessage(text="本聊天室為包車叫車測試"))
    
            if message:
                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()