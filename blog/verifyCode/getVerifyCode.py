import string
import random
from platform import system
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def get_random_color():
    """ 随机生成颜色 """
    color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
    return color


def get_random_word():
    """ 随机生成字符 """
    words = string.ascii_letters + string.digits
    word = random.choice(words)
    return word


def get_verify_code_img(request):
    """ 随机生成验证码 """
    verify_code_img = Image.new('RGB', (160, 50), color=(222, 222, 222))
    verify_code_str = ''

    # 生成验证码图片
    if system() == 'Windows':
        path_ttc = 'C:\\Windows\\Fonts\\msyh.ttc'
    else:
        path_ttc = '/System/Library/Fonts/Supplemental/Songti.ttc'
    font = ImageFont.truetype(path_ttc, 30)
    for i in range(4):
        word = get_random_word()
        color = get_random_color()
        ImageDraw.Draw(verify_code_img).text(xy=(i * 40 + 10, 5), text=word, font=font, fill=color)
        verify_code_str += word

    # 保存验证码文本到session
    request.session['verify_code_str'] = verify_code_str

    # 增加噪点
    for i in range(10):
        x1 = random.randint(0, 200)
        x2 = random.randint(0, 200)
        y1 = random.randint(0, 50)
        y2 = random.randint(0, 50)
        ImageDraw.Draw(verify_code_img).line((x1, y1, x2, y2), fill=get_random_color())
    for i in range(500):
        x = random.randint(0, 200)
        y = random.randint(0, 50)
        ImageDraw.Draw(verify_code_img).point((x, y), fill=get_random_color())

    # 获取图片对象
    f = BytesIO()
    verify_code_img.save(f, 'png')
    verify_code_img_obj = f.getvalue()

    return verify_code_img_obj
