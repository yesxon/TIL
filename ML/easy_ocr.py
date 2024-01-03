import cv2
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import easyocr
import re

#한글로 된 결과물을 보기 위해서는 nanum폰트를 설치해야 합니다.

reader = easyocr.Reader(['ko', 'en'])
img = cv2.imread('./han_account.jpg')

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
denoised_img = cv2.medianBlur(binary_img, 5)
result = reader.readtext(denoised_img)


img = Image.fromarray(img)
font = ImageFont.truetype("NanumBarunGothic", 100)
draw = ImageDraw.Draw(img)

ocr_results = {}

for idx, i in enumerate(result):
  x = i[0][0][0] #좌측 상단 x좌표
  y = i[0][0][1] #좌측 상단 y좌표
  w = i[0][1][0] - x #바운딩 박스의 너비
  h = i[0][2][1] - y #바운딩 박스의 높이

  draw.rectangle(((x, y), (x+w, y+h)), outline="blue", width=2)
  draw.text((int((x+x+w)/2), y - 50), str(i[1]), font=font, fill="blue")
  if idx == 0:
    ocr_results['account'] = i[1]
  elif idx == 1:
    ocr_results['bank'] = i[1]

# 은행 계좌 번호 패턴 정의
bank_patterns = {
    '농협은행': r'.{3}-.{4}-.{4}-.{2}',
    '(구)신한은행': r'.{3}-.{2}-.{6}',
    '(신)신한은행': r'.{3}-.{3}-.{6}',
    '국민은행': r'.{6}-.{2}-.{6}',
    '우리은행': r'.{4}-.{3}-.{6}',
    '기업은행': r'.{3}-.{6}-.{2}-.{3}',
    '하나은행': r'.{3}-.{6}-.{5}',
    '대구은행': r'.{3}-.{2}-.{6}-.{1}',
    '부산은행': r'.{3}-.{4}-.{4}-.{2}',
    '산업은행': r'.{3}-.{4}-.{4}-.{3}',
}

# OCR 결과에서 'account' 값 추출
account_number = ocr_results.get('account', '')

# 은행 계좌 번호 패턴에 따라 'bank' 값을 업데이트
bank_found = False
for bank_name, pattern in bank_patterns.items():
    if re.match(pattern, account_number):
        ocr_results['bank'] = bank_name
        bank_found = True
        break

if not bank_found:
    ocr_results['bank'] = "계좌의 은행을 찾을 수 없습니다. 다시 확인해주세요"

# 결과 출력
    
# plt.figure(figsize=(12, 10))
# plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(gray_img, cv2.COLOR_BGR2RGB)), plt.title('Gray Scale')
# plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(binary_img, cv2.COLOR_BGR2RGB)), plt.title('Binary Image')
# plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(denoised_img, cv2.COLOR_BGR2RGB)), plt.title('Denoised Image')
    
print(ocr_results)
plt.imshow(img)