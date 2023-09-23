from linebot.models import *
from hailAndChartered import models
from urllib.parse import quote

def HeilList():
    return ""

def CharteredList():
    carTypes = models.charteredOption.objects.all()
    bubbles = []

    for cT in carTypes:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": cT.carImgUrl
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": cT.carType,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "半天(5小時)$" + str(cT.chtdStartPrice),
                                "wrap": True,
                                "weight": "bold",
                                "size": "xl",
                                "color": "#1A3852"},
                            {
                                "type": "text",
                                "text": "全天(10小時)$" + str(cT.chtdAlldayPrice),
                                "wrap": True,
                                "weight": "bold",
                                "size": "xl",
                                "color": "#1A3852"},
                            {
                                "type": "text",
                                "text": "逾時$" + str(cT.timeOutPrice) + "/小時",
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "align": "end"}
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xl",
                        "contents": [
                            {
                                "type": "text",
                                "text": "test",
                                "wrap": True,
                                "weight": "bold",
                                "flex": 0,
                                "size": "md"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "確定",
                            "data": f"action=charteredCheck&id={cT.id}"
                            },
                        "color": "#D5A07E"
                    }]
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="包車選擇",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def CharteredOption():
    return "work"

def carServiceCheck():
    return ""