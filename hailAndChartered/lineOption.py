from linebot.models import *
from hailAndChartered import models
from urllib.parse import quote

def HeilList():
    agencys = models.hailOption.objects.all()      
    bubbles = []
    for agcs in agencys:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": agcs.imgUrl
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": agcs.agencyName,
                        "wrap": True,
                        "weight": "bold",
                        "size": "l",
                        "color": "#3C486B"
                    },                                          
                    {
                        "type": "separator",
                        "margin": "sm"
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
                        "label": "連結",
                        "uri": agcs.agencyUrl},
                    "color": "#F9D949"
                }
                ],
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="叫車選項",
        contents={
            "type": "carousel",
            "contents": bubbles}
    )
    return flex_message

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
                        "size": "l",
                        "color": "#1A3852"
                    },                    
                    {
                        "type": "text",
                        "text": "半天(5小時)$" + str(cT.chtdStartPrice),
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": "全天(10小時)$" + str(cT.chtdAlldayPrice),
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": "逾時$" + str(cT.timeOutPrice) + "/小時",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852"
                    },                        
                    {
                        "type": "separator",
                        "margin": "sm"
                    }
                ],
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
                            "label": "選擇",
                            "data": f"action=charteredCheck&chId={cT.id}"},
                        "color": "#146C94"
                    }
                ],
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="包車選擇",
        contents={
            "type": "carousel",
            "contents": bubbles}
    )
    return flex_message

def carServiceCheck():
    return ""