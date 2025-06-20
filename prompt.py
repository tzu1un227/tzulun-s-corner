import os
os.system('cls')
socialMedia='LINE'
Audience='一般大眾'
style='感性'
intro='(產品介紹)'

socialMedia_dict={'facebook':[450,50],'LINE':[100,20],'Instagram':[200,50]}
Audience_dict={'一般大眾':'加入一些諧音笑話','上班族':'穿插一些英文單字','狀老年':'使用一些閩南語','學生':'使用一些網路用語'}
Style_dict={'感性':'正向、友善且溫暖，用字中性且擅長情境描述及情感抒發','嚴謹':'專業、知性且穩定，用字精準且在意數據及證明','活潑':'樂觀、年輕且有趣，用字較口語輕鬆，喜歡分享與表達自己'}

'''
{intro}
請基於上述的產品介紹，邀請大家使用此產品，如有連結鼓勵點擊，文末鼓勵按讚留言分享
平台是{socialMedia} 受眾為{Audience} 廣告風格是{style}
若平台是facebook，把字數控制在 450 字以內，並在前 50 字有吸引人的標題
若平台是LINE，把字數控制在 100 字以內，並在前 20 字有吸引人的標題
若平台是Instagram，把字數控制在 200 字以內，並在前 50 字有吸引人的標題
若受眾是一般大眾(18到65歲)，加入一些諧音笑話
若受眾是上班族(25到40歲)，穿插一些英文單字
若受眾是狀老年(40到60歲)，使用一些閩南語
若受眾是學生(15到22歲)，使用一些網路用語
若廣告風格是感性，正向、友善且溫暖，用字中性且擅長情境描述及情感抒發
若廣告風格是嚴謹，專業、知性且穩定，用字精準且在意數據及證明
若廣告風格是活潑，樂觀、年輕且有趣，用字較口語輕鬆，喜歡分享與表達自己
'''


prompt2=f'現在有一個產品, 產品內容是\n"\n{intro}\n"\n目標平台是{socialMedia}，請基於下列條件，產生廣告邀請大家使用此產品:\n(1)字數控制在 {socialMedia_dict[socialMedia][0]} 字以內，並在前 {socialMedia_dict[socialMedia][1]} 字內含有吸引人的標題\n(2)受眾是{Audience}，請在廣告中{Audience_dict[Audience]}\n(3)廣告風格是{style}，請使用{style_dict[style]}的語氣，並加入一些emoji讓整個文字活潑一點\n(4)如產品介紹內容有連結，請在文末鼓勵按讚留言分享\n(5)若目標平台是facebook或是Instagram，請產生中文Hashtag，否則不要產生Hashtag'

print(prompt2)