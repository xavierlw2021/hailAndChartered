from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from urllib.parse import quote, parse_qsl
from urllib.request import urlopen
import secrets, qrcode, requests, json, datetime
from io import BytesIO
import base64

from keyCardTest import models

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

PAY_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/request'   #測試
CONFIRM_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/{}/confirm'    #測試

LINE_PAY_ID = '1657362199'   #((需要改))
LINE_PAY_SECRET = '171192f29cdc223d91da297cb60c87bc'   #((需要改))
STORE_IMAGE_URL = 'https://i.imgur.com/mrO4VRZ.jpg'   #((需要改))

class KeyCardService():
    def work(self, userId, userName, startDatetime, endDatetime):
        try:
            if isinstance(startDatetime, datetime.datetime):
                limit_datetime = startDatetime + datetime.timedelta(minutes=20)
            elif isinstance(startDatetime, str):
                startDatetime = datetime.datetime.strptime(startDatetime, '%Y-%m-%d %H:%M')
                limit_datetime = startDatetime + datetime.timedelta(minutes=20)
        except:
            return "" , "時間格式錯誤"
        
        n_pwd = secrets.token_urlsafe()
        # print(a, len(a))
        # n_qr = self.qrcode_src_gen(n_pwd)   #生成QRCode的source
        # n_quest = models.qrcode_storage.objects.create(pwd = n_pwd, 
        #                                                start_datetime = startDatetime,
        #                                                limit_datetime = limit_datetime,
        #                                                finish_datetime = endDatetime,
        #                                                main_userId = userId,
        #                                                main_userName = userName)
        # return n_pwd, limit_datetime, n_quest.id
        #=========================
        return n_pwd, limit_datetime
        #=========================
    
    def add_family(self, pwd, userId):
        # questCard_data = models.qrcode_storage.objects.filter(pwd = pwd).first()
        time_state = self.timeout_check(pwd)
        if time_state == "True":
            # questCard_data.family_userId += f'{userId},'
            msg = f"共用密碼完成，您的密碼為:{pwd}"
        else:
            msg = "失敗，已超過可新增時間"
        return msg

    def qrcode_src_gen(self, pwd):
        qr = qrcode.QRCode(version=7, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=6, border=7)
        qr.add_data(pwd)
        img = qr.make_image(fill_color="black", back_color="white")
        # print(img, type(img))
        buf = BytesIO()
        img.save(buf)        
        # plt.savefig(buf, format='png')
        img_data = buf.getvalue()
        # print(img_data, type(img_data))   #byte type
        img_string = base64.b64encode(img_data).decode()
        # print(img_string, type(img_string))   #string type
        img_data = "data:image/png;base64,"+ img_string
        return img_data 

    def timeout_check(seif, pwd):
        questCard_data = models.qrcode_storage.objects.filter(pwd = pwd).first()
        res = urlopen('http://just-the-time.appspot.com/')
        result_str = res.read().strip().decode('utf-8')
        result_local = datetime.datetime.strptime(result_str, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)
        if questCard_data.start_datetime < result_local < questCard_data.limit_datetime:
            questCard_data.be_alive = True
            questCard_data.save()
            return "True"
        elif questCard_data.limit_datetime < result_local < questCard_data.finish_datetime:            
            questCard_data.be_alive = True
            questCard_data.save()
            return "Restricted" #不可再共用密碼
        elif result_local > questCard_data.finish_datetime:
            questCard_data.be_alive = False
            questCard_data.save()
            return "False"
        else:
            questCard_data.be_alive = False
            questCard_data.save()
            return "False"

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
                    message.append(TextSendMessage(text="本聊天室為房卡測試"))  

                elif '@生成QRcode' in msgtext:
                    fake_startDt = datetime.datetime.now() - datetime.timedelta(days=1)
                    fake_finishDt = datetime.datetime.now() + datetime.timedelta(days=1)
                    # n_pwd, closeTime, wid = KeyCardService().work(uid, name, fake_startDt, fake_finishDt)
                    #=========================
                    n_pwd, closeTime = KeyCardService().work(uid, name, fake_startDt, fake_finishDt)
                    #=========================
                    message.append(TextSendMessage(text=f"您的房卡密碼為:{n_pwd}/在{str(closeTime)[:16]}前，您可以將此封訊息轉傳給您的同行家人或朋友，讓他們按下密碼共用，他們將可以與您共用此密碼與QRCode"))
                    message.append(TextSendMessage(text="顯示QRCode",
                                                   quick_reply=QuickReply(
                                                       items=[QuickReplyButton(
                                                                action=URIAction(
                                                                    label="顯示QRCode",
                                                                    # uri=f'/yourQRCode/{wid}',
                                                                    #=========================
                                                                    uri='https://cartest-cuk4.onrender.com/yourQRCode/1',
                                                                    #=========================
                                                               )
                                                           )
                                                       ]
                                                   )))

                elif '您的密碼為:' in msgtext:
                    getPwd = msgtext.split(':')[1].split('/在')[0]
                    providerName = models.qrcode_storage.objects.filter(pwd = getPwd).first().main_userName
                    message.append(TextSendMessage(text=f"您將與 {providerName} 共用房卡密碼，請確認?",
                                                   quick_reply=QuickReply(
                                                       items=[
                                                            QuickReplyButton(
                                                                action=PostbackAction(
                                                                    label='密碼共用',
                                                                    display_text='密碼共用',
                                                                    data=f'action=pwdAddFamily&pwd={getPwd}'))
                                                       ])))
                    # message.append(ImageSendMessage(
                    #     original_content_url=n_qr,
                    #     preview_image_url=n_qr
                    # ))

            elif isinstance(event, PostbackEvent):
                uid = event.source.user_id
                data = dict(parse_qsl(event.postback.data)) #先將postback中的資料轉成字典
                p_action = data.get('action') #get action裡面的值
                if p_action == "pwdAddFamily": 
                    pwd = data.get('pwd')
                    msg = KeyCardService().add_family(pwd, uid)
                    message.append(TextSendMessage(text=msg))               
    
            if message:
                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
    
def show_QRCode(request, qid):
    # Pwd = models.qrcode_storage.objects.get(id = qid).pwd
    # QRCode_data = KeyCardService.qrcode_src_gen(Pwd)
    #=========================
    Pwd = secrets.token_urlsafe()
    QRCode_data = KeyCardService.qrcode_src_gen(Pwd)
    #=========================
    return render(request, 'yourQRCode.html', {'QRCode_data': QRCode_data})