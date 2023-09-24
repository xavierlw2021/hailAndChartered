from linebot.models import *
from hailAndChartered import models
from urllib.parse import quote, parse_qsl

def HeilList(): #叫車選單
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
                "url": agcs.imgUrl,                
                "position": "relative",
                "backgroundColor": "#F6F1F1"
            },
            "body": {
                "type": "box",
                "layout": "vertical",                
                "contents": [
                    {
                        "type": "text",
                        "text": agcs.agencyName,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#000000"
                    },                                          
                    {
                        "type": "separator",
                        "margin": "sm"
                    }
                ],                
                "backgroundColor": "#F6F1F1"
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
                        "uri": str(agcs.agencyUrl)
                    },
                    "color": "#146C94"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="叫車選項",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def CharteredList():    #包車選單
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
                "contents": [
                    {
                        "type": "text",
                        "text": cT.carType,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                    }, 
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [ 
                                    {
                                        "type": "text",
                                        "text": "半天(5小時)",
                                        "color": "#1A3852",
                                        "wrap": True,
                                        "weight": "bold",
                                        "size": "md",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "$" + str(cT.chtdStartPrice),
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [                                               
                                    {
                                        "type": "text",
                                        "text": "全天(10小時)",
                                        "color": "#1A3852",
                                        "wrap": True,
                                        "weight": "bold",
                                        "size": "md",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "$" + str(cT.chtdAlldayPrice),
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [                                               
                                    {
                                        "type": "text",
                                        "text": "逾時",
                                        "color": "#1A3852",
                                        "weight": "bold",
                                        "size": "sm",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "$" + str(cT.timeOutPrice)+ "/小時",
                                        "size": "sm",
                                    }
                                ]
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
                            "type": "postback",
                            "label": "選擇",
                            "data": f"action=charteredCheck&chId={cT.id}"
                        },
                        "color": "#4F709C"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "margin": "sm"
                    }
                ],                
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

def carServiceCheck(event): #包車預約確認
    dataString = dict(parse_qsl(event.postback.data)).get('dscp')
    data_list = dataString.split('/')
    carId = data_list[0]
    cartype = models.charteredOption.objects.get(id=carId).carType
    appointmentDate = data_list[1]
    passengerAmount = data_list[2]
    spnd = dict(parse_qsl(event.postback.data)).get('spnd')
    spndString = f"{spnd[:7]}..." if spnd != 0 else "無"
    message = FlexSendMessage(
        alt_text="包車預約單",
        contents={
            "type": "carousel",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [                        
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [                            
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "車種",
                                    "size": "sm",
                                    "color": "#000000",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": cartype,
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "預約日期",
                                    "size": "sm",
                                    "color": "#000000",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": appointmentDate,
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "乘客數",
                                    "size": "sm",
                                    "color": "#000000",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": passengerAmount,
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "特殊需求",
                                    "size": "sm",
                                    "color": "#000000",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": spndString,
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                    "type": "postback",
                                    "label": "確認預約",
                                    "data": f"action=chtdBooking&dscp={dataString}&spnd={spnd}"
                                    },
                                    "style": "primary",
                                    "flex": 2,
                                    "color": "#2192FF"
                                }
                                ],
                                "spacing": "md"
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            }]
                    }]
                },
                "styles": {
                    "footer": {
                    "separator": True
                    }
                }
            }
        }
    ) 
    return message