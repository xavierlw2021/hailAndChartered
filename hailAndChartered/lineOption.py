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
                            "data": f"action=carCheck&chId={cT.id}"
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

def carServiceCheck(cId,Num,chDt): #包車預約確認
    carId = cId
    cartype = models.charteredOption.objects.get(id=int(carId))  
    passengerAmount = Num
    appointmentDate = chDt.replace('T',' ')
    message = FlexSendMessage(
        alt_text="包車預約單",
        contents={
            "type": "carousel",
            "contents": [{
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": cartype.carImgUrl
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [                        
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [ 
                            {
                                "type": "text",
                                "text": "預約車種",
                                "size": "md",
                                "weight": "bold",
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": cartype.carType,
                                "size": "xl",
                                "weight": "bold"
                            }
                        ]
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
                                        "text": "預約時間",
                                        "color": "#000000",
                                        "size": "lg",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": appointmentDate,
                                        "wrap": True,
                                        "color": "#000000",
                                        "size": "lg",
                                        "flex": 2
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
                                        "text": "預計人數",
                                        "color": "#000000",
                                        "size": "lg",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": passengerAmount+" 人",
                                        "wrap": True,
                                        "color": "#000000",
                                        "size": "lg",
                                        "flex": 2
                                    }
                                ]
                            }
                        ]
                    }]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "半天(5小時)",
                                        "color": "#000000",
                                        "flex": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "$"+str(cartype.chtdStartPrice)
                                    }
                                ],
                                "spacing": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "全天(10小時)",
                                        "color": "#000000",
                                        "flex": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "$"+str(cartype.chtdAlldayPrice)
                                    }
                                ],
                                "spacing": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "逾時",
                                        "color": "#000000",
                                        "flex": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "$"+str(cartype.timeOutPrice)+"/小時",
                                        "size": "sm"
                                    }
                                ],
                                "spacing": "sm"
                            }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "確認預約",
                            "data": f"action=chtdBooking&cId={cId}&Num={Num}&chDt={chDt}"
                        },
                        "color": "#4F709C"
                    }
                    ],
                    "margin": "lg"
                }
                }]})
    return message