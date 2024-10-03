from PIL import Image, ImageDraw, ImageFont

def add_text(image, text: str, position: tuple, fontname: str, max_fontsize: int, min_fontsize: int, line_spacing: int, box_size: tuple, alignment='left', fill=(255, 0, 0), line_limit: int = 5):
    draw = ImageDraw.Draw(image)
    
    # 設定框寬度和高度
    max_width = box_size[0]
    max_height = box_size[1]
    
    # 初始字體大小
    font_size = max_fontsize
    font = ImageFont.truetype(fontname, font_size)

    # 確保文字可以適應框的大小
    while True:
        # 測量文字的大小
        if len(text) > line_limit:  # 根據需求換行
            lines = [text[:line_limit], text[line_limit:]]
        else:
            lines = [text]

        total_height = 0
        widths = []
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            widths.append(text_width)
            total_height += bbox[3] - bbox[1] + line_spacing
        
        if max(max(widths), total_height) <= max_width and total_height <= max_height:
            break  # 文字可以適應框的大小，退出循環
        else:
            # 縮小字體大小並重新設置字體
            font_size -= 1
            if font_size < min_fontsize:
                raise ValueError("Text cannot fit within the specified box size.")
            font = ImageFont.truetype(fontname, font_size)

    # 繪製文字
    y_position = position[1] + (max_height - total_height + line_spacing) // 2  # 置中Y軸
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if alignment == 'center':
            x_position = position[0] + (max_width - text_width) // 2
        elif alignment == 'right':
            x_position = position[0] + max_width - text_width
        else:  # 預設 'left'
            x_position = position[0]

        draw.text((x_position, y_position), line, font=font, fill=fill)
        y_position += bbox[3] - bbox[1] + line_spacing  # 更新y位置

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

    d1 = {
        'text': '一二三四五六七八九十',
        'position': (510, 210),
        'fontname': 'msjh.ttf',
        'max_fontsize': 150,
        'min_fontsize': 100,
        'line_spacing': 5,
        'box_size': (669, 257),
        'alignment': 'left',
        'fill': (0, 115, 209),  # #0073D1
        'line_limit': 5  # 超過5個字換行
    }

    d2 = {
        'text': '一二三四五六七八',
        'position': (250, 1875),
        'fontname': 'msjh.ttf',
        'max_fontsize': 150,
        'min_fontsize': 70,
        'line_spacing': 15,
        'box_size': (320, 156),
        'alignment': 'center',
        'fill': (23, 42, 135),  # #172A87
        'line_limit': 4  # 超過4個字換行
    }

    d3 = {
        'text': '一二三',
        'position': (1080, 1875),
        'fontname': 'msjh.ttf',
        'max_fontsize': 120,
        'min_fontsize': 70,
        'line_spacing': 15,
        'box_size': (320, 156),
        'alignment': 'center',
        'fill': (23, 42, 135),  # #172A87
        'line_limit': 4  # 超過4個字換行
    }

    d4 = {
        'text': '一',
        'position': (1920, 1875),
        'fontname': 'msjh.ttf',
        'max_fontsize': 120,
        'min_fontsize': 70,
        'line_spacing': 15,
        'box_size': (320, 156),
        'alignment': 'center',
        'fill': (23, 42, 135),  # #172A87
        'line_limit': 4  # 超過4個字換行
    }

    d5 = {
        'text': '一二三四五六七八九十',
        'position': (225, 2100),
        'fontname': 'msjh.ttf',
        'max_fontsize': 120,
        'min_fontsize': 80,
        'line_spacing': 10,
        'box_size': (402, 160),
        'alignment': 'center',
        'fill': (229, 0, 18),  # #E50012
        'line_limit': 5  # 超過5個字換行
    }

    d6 = {
        'text': '一二三四五',
        'position': (1050, 2100),
        'fontname': 'msjh.ttf',
        'max_fontsize': 120,
        'min_fontsize': 80,
        'line_spacing': 10,
        'box_size': (402, 160),
        'alignment': 'center',
        'fill': (229, 0, 18),  # #E50012
        'line_limit': 5  # 超過5個字換行
    }

    d7 = {
        'text': '一二三',
        'position': (1890, 2100),
        'fontname': 'msjh.ttf',
        'max_fontsize': 120,
        'min_fontsize': 80,
        'line_spacing': 10,
        'box_size': (402, 160),
        'alignment': 'center',
        'fill': (229, 0, 18),  # #E50012
        'line_limit': 5  # 超過5個字換行
    }

    image = add_texts(image_path, 'output', [d1, d2, d3, d4, d5, d6, d7])
    image.show()
