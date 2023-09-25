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
    cartype = models.charteredOption.objects.get(id=carId)
    appointmentDate = data_list[1]
    passengerAmount = data_list[2]
    spnd = dict(parse_qsl(event.postback.data)).get('spnd')
    spndString = f"{spnd[:5]}..." if spnd != 0 else "無"
    message = FlexSendMessage(
        alt_text="包車預約單",
        contents={
            "type": "carousel",
            "contents": {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": cartype.carImgUrl,
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
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
                                "text": "車種",
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
                                    "text": f"{passengerAmount}人",
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
                                "text": f"{cartype.chtdStartPrice}"
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
                                "text": f"{cartype.chtdAlldayPrice}"
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
                                "text": f"{cartype.timeOutPrice}/小時",
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
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": "確認預約",
                        "uri": f"action=chtdBooking&dscp={dataString}&spnd={spnd}"
                        },
                        "color": "#000000"
                    }
                    ],
                    "margin": "lg"
                }
                }})
    return message
    #                         {
    #                             "type": "box",
    #                             "layout": "horizontal",
    #                             "contents": [
    #                             {
    #                                 "type": "text",
    #                                 "text": "特殊需求",
    #                                 "size": "sm",
    #                                 "color": "#000000",
    #                                 "flex": 0
    #                             },
    #                             {
    #                                 "type": "text",
    #                                 "text": spndString,
    #                                 "size": "sm",
    #                                 "color": "#111111",
    #                                 "align": "end"
    #                             }
    #                             ]
    #                         },
    #                         {
    #                             "type": "box",
    #                             "layout": "horizontal",
    #                             "contents": [
    #                             {
    #                                 "type": "button",
    #                                 "action": {
    #                                 "type": "postback",
    #                                 "label": "確認預約",
    #                                 "data": f"action=chtdBooking&dscp={dataString}&spnd={spnd}"
    #                                 },
    #                                 "style": "primary",
    #                                 "flex": 2,
    #                                 "color": "#2192FF"
    #                             }
    #                             ],
    #                             "spacing": "md"
    #                         },
    #                         {
    #                             "type": "separator",
    #                             "margin": "xxl"
    #                         }]
    #                 }]
    #             },
    #             "styles": {
    #                 "footer": {
    #                 "separator": True
    #                 }
    #             }
    #         }
    #     }
    # ) 
    # return message