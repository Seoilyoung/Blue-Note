import os
import random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
# AP가이드 파일
# 현상수배 티켓도 추가 예정
# 일정에 추가 기능 - 버튼(gui로 구현)

# 배경이미지
# <a href="https://kr.freepik.com/free-photo/white-crumpled-paper-texture-for-background_1189775.htm">
# 작가 aopsan</a> 출처 Freepik

def ImgSave(event_name, date, time_start, time_end, remain_time):

    # 입력 변수 정의
    time_format = '%Y/%m/%d %H:%M'
    update_time_start = datetime.strptime(date + ' ' + time_start, time_format)
    update_time_end = datetime.strptime(date + ' ' + time_end, time_format)

    # 함수 정의
    def CalApMsg(ap_remain, ap_post=0):
        return '보유 AP : {}{}\n'.format(ap_remain, ' / ' + str(ap_post) if ap_post else '')
    def TimeMsg(day,min):
        return (login_time-timedelta(days=day, minutes=-min)).strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
     
    # 날짜 변수 정의
    ap_remain = 0
    ap_post = 0
    login_time = update_time_end+timedelta(hours=remain_time)

    # 이미지 변수 정의
    img_table = Image.open('ApGuide/ap_background.webp')
    d = ImageDraw.Draw(img_table)


    fnt_title = ImageFont.truetype("BMJUA_ttf.ttf",40)
    fnt_content = ImageFont.truetype("BMJUA_ttf.ttf",25)
    fnt_underline = ImageFont.truetype("BMJUA_ttf.ttf",25)

    # 텍스트 변수 정의
    txt_title = event_name + ' AP 가이드'
    txt_content_day = ['' for _ in range(4)]
    txt_content_ap = ''
    txt_content_underline =''


    # day 0
    txt_content_day[0] = TimeMsg(3,120)
    txt_content_day[0] += '  1. 카페 수령\n'
    txt_content_day[0] += TimeMsg(3,180)
    txt_content_day[0] += '  1. 보유 AP 소모\n'
    txt_content_day[0] += '\n\n'
    txt_content_ap += '\n\n\n'+ CalApMsg(ap_remain) + '\n\n\n'

    # day 1
    txt_content_day[1] = TimeMsg(2,60)
    txt_content_day[1] += '  1. 자연회복 220AP\n'
    txt_content_day[1] += '  2. AP패키지 150AP\n'
    txt_content_day[1] += '  3. AP 3회 충전 360AP\n'
    txt_content_day[1] += '  4. 일일임무 150AP\n'
    txt_content_day[1] += '  5. 카페 수령 513AP\n'
    txt_content_day[1] += '\n\n'
    ap_remain += 220
    txt_content_ap += CalApMsg(ap_remain)
    ap_remain += 150
    txt_content_ap += CalApMsg(ap_remain)
    ap_remain += 120*3
    txt_content_ap += CalApMsg(ap_remain)
    ap_remain += 150
    txt_content_ap += CalApMsg(ap_remain)
    ap_remain += 513
    if ap_remain >1000:
        ap_post = ap_remain-999
        ap_remain -=ap_post
    txt_content_ap += CalApMsg(ap_remain,ap_post) + '\n\n\n'

    # day 2
    txt_content_day[2] = TimeMsg(1,50)
    txt_content_day[2] += '  1. AP패키지 150AP, 우편함으로 이동\n'
    txt_content_day[2] += '  2. 우편함의 24시간 이내 AP 사용\n'
    txt_content_day[2] += '  3. 카페 수령, 대항전 수령\n'
    txt_content_day[2] += '  4. 일일임무 150AP\n'
    txt_content_day[2] += '  5. 전술코인 4회 충전, 360AP\n'
    txt_content_day[2] += '\n\n'
    ap_post += 150
    txt_content_ap += CalApMsg(ap_remain,ap_post)
    ap_post = 150
    txt_content_ap += CalApMsg(ap_remain,ap_post)
    ap_post += 513
    txt_content_ap += CalApMsg(ap_remain,ap_post)
    ap_post += 150
    txt_content_ap += CalApMsg(ap_remain,ap_post)
    ap_post += 360
    txt_content_ap += CalApMsg(ap_remain,ap_post) + '\n\n\n'

    # day 3
    txt_content_day[3] = update_time_start.strftime('%Y/%m/%d %H시 %M분') + ' 이내 접속\n'
    txt_content_day[3] += '  1. 점검전 카페 호감도 가능\n'
    txt_content_day[3] += '  2. AP패키지 150AP\n'
    txt_content_day[3] += TimeMsg(0,0)
    txt_content_day[3] += '  1. 점검 완료 및 AP 소모\n'
    txt_content_day[3] += '\n\n'
    ap_post += 150
    txt_content_ap += CalApMsg(ap_remain,ap_post)

    # etc
    txt_content_etc = '- 3일차 AP사용량에 따른 약간의 오차 가능성이 있습니다.\n'
    txt_content_etc +='- 서클 AP 모으기\n' + '- 점검 후 주간 임무 AP 수령\n'

    txt_day = ''.join(txt_content_day)+txt_content_etc

    count_underline = txt_day.count('\n')
    for i in range(0,count_underline) :
        txt_content_underline += '-------------------------------------------------------\n'


    d.text((60,60), txt_title,font=fnt_title, fill=(0,0,0))
    d.text((60,120), txt_day,font=fnt_content, fill=(0,0,0))
    d.text((500,120), txt_content_ap,font=fnt_content, fill=(0,0,0))
    d.text((60,134),txt_content_underline,font=fnt_content, fill=(200,200,200))

        
    sticker_folder_path = './Gui/Useimages/sticker/'
    if os.path.isdir(sticker_folder_path):
        count_sticker = len(os.listdir(sticker_folder_path))
        # 스티커 번호 랜덤
        num_sticker = random.randrange(1,count_sticker)
        img_sticker = Image.open(sticker_folder_path + str(num_sticker) + '.webp')

        # 스티커 사이즈 변경
        img_sticker = img_sticker.resize((100,100))

        # 스티커 회전
        img_sticker = img_sticker.rotate(-20)

        # 동그라미 모양의 마스크 생성
        mask = Image.new('L', img_sticker.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img_sticker.size[0]-1, img_sticker.size[1]-1), fill=255)

        # 마스크를 적용하여 이미지를 원 형태로 변환
        masked_image = Image.new('RGBA', img_sticker.size)
        masked_image.paste(img_sticker, mask=mask)     
        
        # 이미지 추가
        img_table.paste(masked_image, (600, 950), mask=masked_image)

    if not os.path.exists('Images'):
        os.makedirs('Images')
    img_table.save('Images/' + event_name + ' AP 가이드.webp', format='WebP', lossless=True)