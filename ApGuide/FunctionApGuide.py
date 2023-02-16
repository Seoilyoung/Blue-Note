from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
# AP가이드 파일
# 현상수배 티켓도 추가 예정
# 일정에 추가 기능 - 버튼(gui로 구현)

# 배경이미지
# <a href="https://kr.freepik.com/free-photo/white-crumpled-paper-texture-for-background_1189775.htm">
# 작가 aopsan</a> 출처 Freepik

# 입력 변수 정의
# ------------------------------------------------------------------
event_name = '백야당'
update_time_start = datetime(2023,1,31,11)
update_time_end = datetime(2023,1,31,17)
# ------------------------------------------------------------------

# 날짜 변수 정의
remain_time = 3
ap_remain = 0
ap_post = 0
login_time = update_time_end+timedelta(hours=remain_time)

# 이미지 변수 정의
img_table = Image.open('ApGuide/ap_background.webp')
d = ImageDraw.Draw(img_table)
fnt_title = ImageFont.truetype("BMJUA_ttf.ttf",40)
fnt_content = ImageFont.truetype("BMJUA_ttf.ttf",25)
fnt_underline = ImageFont.truetype("BMJUA_ttf.ttf",25)

txt_content_ap =''
txt_content_underline =''

txt_title = event_name + ' AP 가이드'

txt_content_day1 = (login_time-timedelta(days=3)+timedelta(minutes=120)).strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
txt_content_day1 += '1. 카페 AP 수령\n'
txt_content_day1 += (login_time-timedelta(days=3)+timedelta(minutes=180)).strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
txt_content_day1 += '2. 보유 AP 소모\n'
txt_content_day1 += '\n\n'
ap_remain = 0
txt_content_ap += '\n\n\n보유 AP : ' + str(ap_remain) + '\n\n\n'

txt_content_day2 = (login_time-timedelta(days=2)+timedelta(minutes=60)).strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
txt_content_day2 += '1. 자연회복 220AP\n'
txt_content_day2 += 'AP패키지 150AP\n'
txt_content_day2 += 'AP 3회 충전, 360AP\n'
txt_content_day2 += '일일임무 150AP\n'
txt_content_day2 += '카페 513AP\n'
txt_content_day2 += '\n\n'
ap_remain += 220
txt_content_ap += '\n보유 AP : ' + str(ap_remain)
ap_remain += 150
txt_content_ap += '\n보유 AP : ' + str(ap_remain)
ap_remain += 120*3
txt_content_ap += '\n보유 AP : ' + str(ap_remain)
ap_remain += 150
txt_content_ap += '\n보유 AP : ' + str(ap_remain)
ap_remain += 513
if ap_remain >1000:
    ap_post = ap_remain-999
    ap_remain -=ap_post
txt_content_ap += '\n보유 AP : ' + str(ap_remain) + ' / ' + str(ap_post) + '\n\n\n'

txt_content_day3 = (login_time-timedelta(days=1)+timedelta(minutes=50)).strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
txt_content_day3 += 'AP패키지 150AP, 우편함으로 이동\n'
txt_content_day3 += '우편함의 24시간 이내 AP 사용\n'
txt_content_day3 += '카페 AP, 대항전 수령\n'
txt_content_day3 += '일일임무 150AP\n'
txt_content_day3 += '전술코인 4회 충전, 360AP\n'
txt_content_day3 += '\n\n'
ap_post += 150
txt_content_ap += '\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post)
ap_post = 150
txt_content_ap += '\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post)
ap_post += 513
txt_content_ap += '\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post)
ap_post += 150
txt_content_ap += '\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post)
ap_post += 360
txt_content_ap += '\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post) + '\n\n\n'

txt_content_day4 = update_time_start.strftime('%Y/%m/%d %H시 %M분') + ' 이내 접속\n'
txt_content_day4 += '점검전 카페 호감도 가능\n'
txt_content_day4 += 'AP패키지 150AP\n'
txt_content_day4 += login_time.strftime('%Y/%m/%d %H시 %M분') + ' 접속\n'
txt_content_day4 += '점검 완료 및 AP 소모\n'
txt_content_day4 += '\n\n'
ap_post += 150
txt_content_ap += '\n\n보유 AP :' + str(ap_remain) + ' / ' + str(ap_post)

txt_content_etc = '- 3일차 AP사용량에 따른 약간의 오차 가능성이 있습니다.\n'
txt_content_etc +='- 서클 AP 모으기\n' + '- 점검 후 주간 임무 AP 수령\n'

txt_content = txt_content_day1+txt_content_day2+txt_content_day3+txt_content_day4+txt_content_etc
count_underline = txt_content.count('\n')
for i in range(0,count_underline) :
    txt_content_underline += '------------------------------------------------------\n'

d.text((60,60), txt_title,font=fnt_title, fill=(0,0,0))
d.text((60,120), txt_content,font=fnt_content, fill=(0,0,0))
d.text((500,120), txt_content_ap,font=fnt_content, fill=(0,0,0))
d.text((60,134),txt_content_underline,font=fnt_content, fill=(200,200,200))

img_table.save('ApGuide/ap_result.webp')