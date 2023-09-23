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
from hailAndChartered.lineOption import *
import uuid, requests, json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

PAY_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/request'   #測試
CONFIRM_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/{}/confirm'    #測試

LINE_PAY_ID = '1657362199'   #((需要改))
LINE_PAY_SECRET = '171192f29cdc223d91da297cb60c87bc'   #((需要改))
STORE_IMAGE_URL = 'https://i.imgur.com/mrO4VRZ.jpg'   #((需要改))

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

                elif '@搭車出門' in msgtext:                    
                    message.append(TextSendMessage(
                        text='請問您要叫車? 還是包車出遊呢?',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label='我要叫車',
                                        display_text='我要叫車',
                                        data='action=heil')),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label='我要包車',
                                        display_text='我要包車',
                                        data='action=chartered')),
                            ]
                        )
                    ))

            elif isinstance(event, PostbackEvent):
                data = dict(parse_qsl(event.postback.data)) #先將postback中的資料轉成字典
                p_action = data.get('action') #get action裡面的值
                if p_action == "heil":  #叫車選單
                    message.append(HeilList())
                #包車選項流程    
                elif p_action == "chartered":  #選單
                    message.append(CharteredList())                    
                elif p_action == "charteredCheck": 
                    chId = data.get('chId')
                    nowT = datetime.datetime.today().date()
                    # date_list = []
                    # for d in range(7):
                    #     newDate = nowT + datetime.timedelta(days=d)
                    #     date_list.append(
                    #         QuickReplyButton(
                    #             action=PostbackAction(
                    #                 label = f"{newDate}",
                    #                 display_text = f"{newDate}",
                    #                 data=f'action=ch2Date&chId={chId}&chdt={newDate}')))
                    date_list = [   #7天內的日期按鈕串列
                        (QuickReplyButton(
                            action=PostbackAction(
                                label=f'{nowT + datetime.timedelta(days=d)}',
                                display_text=f'{nowT + datetime.timedelta(days=d)}',
                                data=f'action=ch2Date&chId={chId}&chdt={nowT + datetime.timedelta(days=j)}'))) for d in range(7)]
                    message.append(TextSendMessage(
                        text='請問您哪一天要包車呢?',
                        quick_reply=QuickReply(items=date_list)
                    ))
                elif p_action == "ch2Date":
                    message.append(TextSendMessage(text="ch2Date成功"))
                elif p_action == "checkout":
                    message.append(carServiceCheck())
                elif p_action == 'carOpyionPay':  #結帳 
                    message.append(linePay_confirm(event)) 
    
            if message:
                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
def linePay_confirm(event):     #支付流程
    data = dict(parse_qsl(event.postback.data))
    order_id = data.get('order_id')
    order = models.car_order.objects.get(id=order_id)
    if order.is_pay == False:
        order_uuid = uuid.uuid4().hex
        total_cost = order.total_cost

        line_pay = LinePay()
        info = line_pay.pay(product_name='carTest',
                            amount=total_cost,
                            order_id=order_uuid,
                            product_image_url=STORE_IMAGE_URL)  
        pay_web_url = info['paymentUrl']['web'] 
        transaction_id = info['transactionId']
        order.transaction_id = transaction_id   #登錄官方回傳值
        order.save()
        msg = TemplateSendMessage(
            alt_text='Thanks message',
            template=ButtonsTemplate(
                text='請點選下方金額進行LinePay支付',
                actions=[
                    URIAction(label=f'Pay NT${total_cost}', uri=pay_web_url)
                ]
            )
        )

    elif order.is_pay == True:        
        msg = TextSendMessage(text=f"此訂單您已經付款")

    return msg

class LinePay():
    def __init__(self, currency='TWD'):
        self.channel_id = LINE_PAY_ID
        self.secret = LINE_PAY_SECRET
        self.redirect_url = 'https://cartest-cuk4.onrender.com/confirm'   #((需要改))
        self.currency = currency

    def _headers(self, **kwargs): #會自動帶入上述三個設定
        return {**{'Content-Type': 'application/json',
                   'X-LINE-ChannelId': self.channel_id,
                   'X-LINE-ChannelSecret': self.secret},
                **kwargs}

    def pay(self, product_name, amount, order_id, product_image_url=None):
        data = {    #pay方法用字典帶入我們所需要的值
            'productName': product_name,
            'amount': amount,
            'currency': self.currency,
            'confirmUrl': self.redirect_url,
            'orderId': order_id,
            'productImageUrl': product_image_url
        }
        #把上面資料轉換成json格式並帶入headers，利用post方法送出資料
        response = requests.post(PAY_API_URL, headers=self._headers(), data=json.dumps(data).encode('utf-8'))
        #response就是line的回應
        return self._check_response(response)   #取得回應後透過_check_response確認

    def confirm(self, transaction_id, amount):  #首先會接收transaction_id, total_cost
        data = json.dumps({#接著把這些資料轉成json格式
            'amount': amount,
            'currency': self.currency
        }).encode('utf-8')
        response = requests.post(CONFIRM_API_URL.format(transaction_id), headers=self._headers(), data=data)

        return self._check_response(response)

    def _check_response(self, response):
        res_json = response.json()
        print(f"returnCode: {res_json['returnCode']}")
        print(f"returnMessage: {res_json['returnMessage']}")

        if 200 <= response.status_code < 300:
            if res_json['returnCode'] == '0000':#確認狀態為0000再return res_json['info']
                return res_json['info']
        #裡面的資料包含有付款的URL & transaction_id
        raise Exception('{}:{}'.format(res_json['returnCode'], res_json['returnMessage']))