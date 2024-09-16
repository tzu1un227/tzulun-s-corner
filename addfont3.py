#文字超過範圍會調整文字大小
from PIL import Image, ImageDraw, ImageFont

def add_text(image, text, position, fontname, fontsize, box_size, alignment='left', fill=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    
    # 設定框寬度和高度
    max_width = box_size[0]
    max_height = box_size[1]

    # 初始字體大小
    font_size = fontsize
    font = ImageFont.truetype(fontname, font_size)

    # 確保文字可以適應框的大小
    while True:
        # 測量文字的大小
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if text_width <= max_width and text_height <= max_height:
            break  # 文字可以適應框的大小，退出循環
        else:
            # 縮小字體大小並重新設置字體
            font_size -= 1
            if font_size <= 0:
                raise ValueError("Text cannot fit within the specified box size.")
            font = ImageFont.truetype(fontname, font_size)

    # 測量文字的大小
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if alignment == 'center':
        x_position = position[0] + (max_width - text_width) // 2
    elif alignment == 'right':
        x_position = position[0] + max_width - text_width
    else:  # 預設 'left'
        x_position = position[0]

    y_position = position[1] + (max_height - text_height) // 2

    # 繪製文字
    draw.text((x_position, y_position), text, font=font, fill=fill)

    return image

def add_texts(imagefile: str, output_filename: str, textsettings: list[dict]):
    image = Image.open(imagefile)
    for d in textsettings:
        try:
            image = add_text(image, **d)
        except Exception as e:
            print(f'Error processing settings: {d}')
            print(e)
    # image.save(output_filename)
    return image

if __name__ == '__main__':
    import os
    os.system('cls') 
    image_path = '蔡森升級計畫.png'  # 替換成你的圖片文件路徑
    output_filename = 'output.png'

    # d4 = {'text': '最低','position': (1900, 1850),'fontname': 'msjh.ttf','fontsize': 150,'box_size': (380, 190),'alignment': 'center','fill': (0, 0, 255)}
    d1={'text':'外匯優利率','position':(510,170),'fontname':'msjh.ttf','fontsize':200,'box_size': (670, 292),'alignment':'center','fill':(0, 0, 255)}
    d2={'text':'手續費','position':(220,1850),'fontname':'msjh.ttf','fontsize':200,'box_size': (412, 157),'alignment':'center','fill':(0, 0, 255)}
    d3={'text':'利率','position':(1066,1850),'fontname':'msjh.ttf','fontsize':200,'box_size': (412, 157),'alignment':'center','fill':(0, 0, 255)}
    d4={'text':'最低存額','position':(1884,1850),'fontname':'msjh.ttf','fontsize':200,'box_size': (412, 157),'alignment':'center','fill':(0, 0, 255)}
    d5={'text':'0元','position':(220,2100),'fontname':'msjh.ttf','fontsize':200,'box_size': (423, 223),'alignment':'center','fill':(255, 0, 0)}
    d6={'text':'3.5%','position':(1066,2100),'fontname':'msjh.ttf','fontsize':200,'box_size': (423, 223),'alignment':'center','fill':(255, 0, 0)}
    d7={'text':'100美元','position':(1884,2100),'fontname':'msjh.ttf','fontsize':200,'box_size': (423, 223),'alignment':'center','fill':(255, 0, 0)}

    image=add_texts(image_path,output_filename,[d1,d2,d3,d4,d5,d6,d7])
    image.show()
