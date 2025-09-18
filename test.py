{
  "type": "flex",
  "altText": "預約系統 - 選擇時間與位置",
  "contents": {
    "type": "carousel",
    "contents": [
      {
        "type": "bubble",
        "hero": {
          "type": "image",
          "url": "https://i.imgur.com/8QJ0X5X.jpg",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "📅 預約服務",
              "weight": "bold",
              "size": "xl",
              "color": "#1DB446"
            },
            {
              "type": "text",
              "text": "請選擇您方便的預約時間\n我們將為您安排專業服務",
              "size": "md",
              "wrap": true,
              "margin": "md"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "datetimepicker",
                "label": "選擇預約時間",
                "data": "action=reserve&service=consultation",
                "mode": "datetime",
                "initial": "2025-09-18T09:00",
                "min": "2025-09-18T09:00",
                "max": "2025-12-31T18:00"
              },
              "height": "sm",
              "color": "#1DB446"
            },
            {
              "type": "button",
              "style": "secondary",
              "action": {
                "type": "location",
                "label": "分享我的位置",
                "data": "action=location&service=consultation"
              },
              "height": "sm",
              "color": "#00BFFF"
            },
            {
              "type": "spacer"
            },
            {
              "type": "text",
              "text": "預約時間：9:00 - 18:00",
              "size": "xs",
              "color": "#AAAAAA",
              "margin": "md",
              "align": "center"
            }
          ]
        }
      },
      {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "📋 預約確認資訊",
              "weight": "bold",
              "size": "xl",
              "color": "#1DB446"
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "text",
              "text": "預約人：",
              "size": "md",
              "weight": "bold",
              "margin": "sm"
            },
            {
              "type": "text",
              "text": "陳小姐",
              "size": "md",
              "margin": "none"
            },
            {
              "type": "text",
              "text": "聯絡電話：",
              "size": "md",
              "weight": "bold",
              "margin": "sm"
            },
            {
              "type": "text",
              "text": "0912-345-678",
              "size": "md",
              "copyable": true,
              "margin": "none",
              "color": "#1DB446"
            },
            {
              "type": "text",
              "text": "預約服務：",
              "size": "md",
              "weight": "bold",
              "margin": "sm"
            },
            {
              "type": "text",
              "text": "諮詢服務",
              "size": "md",
              "margin": "none"
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "text",
              "text": "⏰ 預約時間",
              "size": "lg",
              "weight": "bold",
              "margin": "sm",
              "color": "#FF6600"
            },
            {
              "type": "text",
              "text": "2025-09-18 14:30",
              "size": "lg",
              "weight": "bold",
              "copyable": true,
              "margin": "none",
              "color": "#1DB446"
            },
            {
              "type": "text",
              "text": "📍 服務地址",
              "size": "lg",
              "weight": "bold",
              "margin": "sm",
              "color": "#00BFFF"
            },
            {
              "type": "text",
              "text": "台北市信義區松仁路 68 號\n台北 101 大樓 85 樓",
              "size": "md",
              "copyable": true,
              "wrap": true,
              "margin": "none",
              "color": "#1DB446"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "uri",
                "label": "導航到服務地點",
                "uri": "https://maps.google.com/?q=25.0330,121.5654"
              },
              "height": "sm",
              "color": "#00BFFF"
            },
            {
              "type": "button",
              "style": "secondary",
              "action": {
                "type": "datetimepicker",
                "label": "修改預約時間",
                "data": "action=modify&service=consultation",
                "mode": "datetime",
                "initial": "2025-09-18T14:30",
                "min": "2025-09-18T09:00",
                "max": "2025-12-31T18:00"
              },
              "height": "sm"
            },
            {
              "type": "button",
              "style": "link",
              "action": {
                "type": "uri",
                "label": "分享完整預約資訊",
                "uri": "line://msg/text/?%F0%9F%93%8F%20%E9%A0%90%E7%B4%84%E7%A2%BA%E8%AA%8D%EF%B8%B1%0A%E9%A0%90%E7%B4%84%E6%99%82%E9%96%93%EF%BC%9A2025-09-18%2014%3A30%0A%E8%81%AF%E7%B9%AB%E9%9B%BB%E8%A9%B1%EF%BC%9A0912-345-678%0A%E6%9C%8D%E5%8B%99%E5%9C%B0%E5%9D%80%EF%BC%9A%E5%8F%B0%E5%8C%97%E5%B8%82%E4%BF%A1%E7%BE%A9%E5%8D%80%E6%9D%BE%E4%BB%81%E8%B7%AF%2068%E8%99%9F"
              },
              "height": "sm"
            }
          ]
        }
      },
      {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "📍 位置確認",
              "weight": "bold",
              "size": "xl",
              "color": "#00BFFF"
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "text",
              "text": "我們需要您的位置資訊來：",
              "size": "md",
              "color": "#666666",
              "margin": "md"
            },
            {
              "type": "box",
              "layout": "vertical",
              "margin": "md",
              "contents": [
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "icon",
                      "url": "https://example.com/icon_check.png",
                      "size": "md",
                      "margin": "none"
                    },
                    {
                      "type": "text",
                      "text": "確認服務範圍",
                      "size": "md",
                      "margin": "md",
                      "flex": 1
                    }
                  ]
                },
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "icon",
                      "url": "https://example.com/icon_check.png",
                      "size": "md",
                      "margin": "none"
                    },
                    {
                      "type": "text",
                      "text": "安排最適合的服務時間",
                      "size": "md",
                      "margin": "md",
                      "flex": 1
                    }
                  ]
                },
                {
                  "type": "box",
                  "layout": "horizontal",
                  "contents": [
                    {
                      "type": "icon",
                      "url": "https://example.com/icon_check.png",
                      "size": "md",
                      "margin": "none"
                    },
                    {
                      "type": "text",
                      "text": "提供交通指引",
                      "size": "md",
                      "margin": "md",
                      "flex": 1
                    }
                  ]
                }
              ]
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "text",
              "text": "🔒 您的位置資訊僅用於預約服務，\n不會儲存超過預約完成後 24 小時",
              "size": "xs",
              "color": "#999999",
              "wrap": true,
              "align": "center"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "location",
                "label": "分享目前位置",
                "data": "action=share_location&service=consultation"
              },
              "height": "sm",
              "color": "#00BFFF"
            },
            {
              "type": "button",
              "style": "link",
              "action": {
                "type": "uri",
                "label": "我會自行前往服務地點",
                "uri": "https://yourdomain.com/confirm-location?manual=true"
              },
              "height": "sm",
              "color": "#FF6600"
            },
            {
              "type": "text",
              "text": "📍 台北市信義區松仁路 68 號",
              "size": "xs",
              "color": "#AAAAAA",
              "margin": "md",
              "align": "center",
              "copyable": true
            }
          ]
        }
      },
      {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "📄 重要提醒事項",
              "weight": "bold",
              "size": "xl",
              "color": "#FF6600"
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "box",
              "layout": "vertical",
              "margin": "md",
              "contents": [
                {
                  "type": "text",
                  "text": "• 請攜帶身分證件",
                  "size": "md",
                  "wrap": true
                },
                {
                  "type": "text",
                  "text": "• 提前 10 分鐘報到",
                  "size": "md",
                  "wrap": true
                },
                {
                  "type": "text",
                  "text": "• 服務地址：台北市信義區松仁路 68 號",
                  "size": "md",
                  "copyable": true,
                  "wrap": true,
                  "color": "#1DB446"
                },
                {
                  "type": "text",
                  "text": "• 客服專線：0800-123-456",
                  "size": "md",
                  "copyable": true,
                  "wrap": true,
                  "color": "#1DB446"
                },
                {
                  "type": "text",
                  "text": "• 停車資訊：台北101地下停車場 B1",
                  "size": "md",
                  "copyable": true,
                  "wrap": true,
                  "color": "#1DB446"
                }
              ]
            },
            {
              "type": "separator",
              "margin": "lg"
            },
            {
              "type": "text",
              "text": "預約編號：RES-20250918-001",
              "size": "lg",
              "weight": "bold",
              "copyable": true,
              "margin": "md",
              "color": "#1DB446",
              "align": "center"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "location",
                "label": "即時導航",
                "data": "action=navigation&service=consultation"
              },
              "flex": 1,
              "height": "sm",
              "color": "#00BFFF"
            },
            {
              "type": "button",
              "style": "link",
              "action": {
                "type": "uri",
                "label": "聯絡客服",
                "uri": "https://line.me/R/ti/p/%40yourbot"
              },
              "flex": 1,
              "height": "sm"
            }
          ]
        }
      }
    ]
  }
}