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
                    "color": "#1A3852"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "$" + str(cT.rt_price),
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": "限定" + str(cT.rt_limit) + "人",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852",
                        "gravity": "center",
                        "align": "end"
                    }
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
                        "text": cT.rt_description,
                        "wrap": True,
                        "weight": "bold",
                        "flex": 0,
                        "size": "md"
                    }
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
                    "type": "uri",
                    "label": "我要訂房",
                    "uri": "https://www.google.com"
                    },
                    "color": "#D5A07E"
                }]
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="房型選擇",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

    return ""

def carServiceCheck():
    return ""