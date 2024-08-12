# from turtle import pen
from PIL import Image, ImageDraw, ImageFont

def add_text(image, text:str, position:tuple, fontname:str, fontsize:int, alignment:str='left', fill:tuple=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    #text_width, text_height = draw.textlength(text,font=font)
    # 设置字体
    font = ImageFont.truetype(fontname, fontsize)  # 字体文件路径和字体大小

    #font = ImageFont.truetype("msjh.ttf", fontsize)  # 字体文件路径和字体大小
    left, top, right, bottom=font.getbbox(text)
    text_width, text_height = right-left,bottom-top
    #text_width, text_height = draw.textsize(text, font=font)
    
    if alignment == 'center':
        position = (position[0] - text_width // 2, position[1] - text_height // 2)
    elif alignment == 'right':
        position = (position[0] - text_width, position[1] - text_height)
    # 'left' alignment is the default case, so no need to modify position
    
    draw.text(position, text, font=font, fill=fill)

    # 保存生成的新图像
    #output_filename = 'path_to_save_new_image.png'
    new_im=image.convert('RGB')
    return new_im

def add_texts(imagefile:str,output_filename:str,textsettings:list[dict]):
    image = Image.open(imagefile)
    for d in textsettings:
        try:
            image=add_text(image,**d)
        except:
            print(f'wrong:{d}')
    image.save(output_filename)
    #image.show()

    return image

if __name__ == '__main__':
    import os
    os.system('cls')
    # 加载图像
    image_path = '蔡森升級計畫.png'
    output_filename='output.png'
    #image = Image.open(image_path)

    # d1={'text':'觀自在菩薩行深般羅蜜多時','position':(1250,1450),'fontname':'sensors\\addfont\msjh.ttf','fontsize':100,'alignment':'center','fill':(255, 0, 0)} # type: ignore
    # d2={'text':'照見五蘊皆空度一切苦厄','position':(1250,1600),'fontname':'sensors\\addfont\msjh.ttf','fontsize':100,'alignment':'center','fill':(0, 255, 0)} # type: ignore
    d1={'text':'數位存款','position':(850,300),'fontname':'msjh.ttf','fontsize':150,'alignment':'center','fill':(0, 0, 255)}
    d2={'text':'台幣','position':(420,1950),'fontname':'msjh.ttf','fontsize':160,'alignment':'center','fill':(0, 0, 255)}
    d3={'text':'外匯','position':(1250,1950),'fontname':'msjh.ttf','fontsize':160,'alignment':'center','fill':(0, 0, 255)}
    d4={'text':'基金','position':(2100,1950),'fontname':'msjh.ttf','fontsize':160,'alignment':'center','fill':(0, 0, 255)}
    d5={'text':'+0.215%','position':(420,2200),'fontname':'msjh.ttf','fontsize':90,'alignment':'center','fill':(255, 0, 0)}
    d6={'text':'3.5%','position':(1250,2200),'fontname':'msjh.ttf','fontsize':90,'alignment':'center','fill':(255, 0, 0)}
    d7={'text':'3.9折','position':(2100,2200),'fontname':'msjh.ttf','fontsize':90,'alignment':'center','fill':(255, 0, 0)}
    #image=add_texts(image_path,output_filename,[{'text'='觀自在菩薩行深般羅蜜多時','position'=(400,500),'fontname'='msjh.ttf','fontsize'=45,'alignment'='center','fill'=(0, 0, 255)}, # type: ignore,
    #                                            {'text'='照見五蘊皆空度一切苦厄','position'=(400,580),'fontname'='msjh.ttf','fontsize'=35,'alignment'='center','fill'=(0, 0, 255)} # type: ignore
    #                                            ])
    image=add_texts(image_path,output_filename,[d1,d2,d3,d4,d5,d6,d7])
    # 添加左对齐文字
    #image=add_text(image, "觀自在菩薩行深般羅蜜多時", (400, 500), "msjh.ttf", fontsize=45, alignment='center', fill=(0, 0, 255))
    #image=add_text(image, "照見五蘊皆空度一切苦厄", (400, 580), "msjh.ttf", fontsize=35, alignment='center', fill=(0, 0, 255))

    #image.save(output_filename)
        #image.save(output_path)

        # 显示图像（可选）
    image.show()

    # 添加居中对齐文字
    #add_text(image_path, "居中對齊文字", (image.width // 2, image.height // 2), "msjh.ttf", alignment='center', fill=(0, 255, 0),'path_to_save_new_image.png')

    # 添加右对齐文字
    #add_text(image_path, "右對齊文字", (image.width - 50, image.height - 50), "msjh.ttf", alignment='right', fill=(0, 0, 255),'path_to_save_new_image.png')


