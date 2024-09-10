from PIL import Image, ImageDraw, ImageFont

def add_text(image, text, position, fontname, fontsize, box_size, alignment='left', fill=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontname, fontsize)
    
    # 設定框寬度和高度
    max_width = box_size[0]
    max_height = box_size[1]
    
    # 初始化行和行高度
    lines = []
    line = ""

    # 將每個字逐個加入行
    for char in text:
        # 預測加入新字後的行寬度
        test_line = line + char
        # 使用 textbbox 來測量文字大小
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]  # 文字寬度
        
        if width <= max_width:
            line = test_line  # 加入行中
        else:
            lines.append(line.strip())  # 添加行並重置
            line = char  # 新行開始
    if line:  # 確保最後一行不會遺漏
        lines.append(line.strip())

    # 繪製文字行
    y_offset = position[1]
    for line in lines:
        # 使用 textbbox 來測量文字大小
        bbox = draw.textbbox((0, 0), line, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        if alignment == 'center':
            x_position = position[0] + (max_width - width) // 2
        elif alignment == 'right':
            x_position = position[0] + max_width - width
        else:  # 預設 'left'
            x_position = position[0]
        
        # 繪製文字並檢查高度限制
        if y_offset + height <= position[1] + max_height:
            draw.text((x_position, y_offset), line, font=font, fill=fill)
            y_offset += height
        else:
            break  # 超出框高度限制則停止

    return image

def add_texts(imagefile: str, output_filename: str, textsettings: list[dict]):
    image = Image.open(imagefile)
    for d in textsettings:
        try:
            image = add_text(image, **d)
        except Exception as e:
            print(f'Error processing settings: {d}')
            print(e)
    image.save(output_filename)
    return image

if __name__ == '__main__':
    import os
    os.system('cls') 
    image_path = '蔡森升級計畫.png'  # 替換成你的圖片文件路徑
    output_filename = 'output.png'

    d4 = {
        'text': '12345678987654321',
        'position': (2100, 1950),
        'fontname': 'msjh.ttf',  # 請確保這個字體文件存在
        'fontsize': 100,
        'box_size': (300, 300),
        'alignment': 'center',
        'fill': (0, 0, 255)
    }

    image = add_texts(image_path, output_filename, [d4])
    image.show()
