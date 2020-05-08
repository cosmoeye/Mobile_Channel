# CM채널 청약단계별 소요 시간 분석

## Data Import & Preprocessing
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

raw = pd.read_csv('path from os.getcwd()',encoding='euc-kr')
test = raw.sort_values(by = ['접속ID'],'업무단계순서')

test['처리시간'] = pd.to_datetime(test['처리일시']) # 처리시간을 str type -> datetime type으로 변환
test.drop(['처리일시'],axis=1,inplace=True)
test.head()

# 루프문에서 활용하기 위해 청약단계를 끝까지 진행한 고객만 list로 추림
acc_ID = list(test[test['업무단계순서']==61]['접속ID'])
steps = list(set(test['업무단계순서']))

df = pd.DataFrame([],columns=['ID','time']) # 접속 ID와 청약시간만 받아오기 위한 DataFrame 생성

# 보험료 계산하기부터 청약완료 단계까지 평균 소요시간 및 소요시간 분포를 확인
for ID in acc_ID:
    df = df.append(
        {'ID':ID,'time':str(
        (max(test[test['접속ID']==ID)&(test['업무단계순서']==61)].처리시간) -
         min(test[test['접속ID']==ID)&(test['업무단계순서']==11)].처리시간)))}
    ,ignore = True) # ignore_True를 옵션으로 주어야 에러가 안남

# 청약하는데 하루가 넘어가는 outlier는 제외
time = pd.DataFrame([],columns = ['소요시간'])
for i in range(len(df)):
    if df.time[i][:5]=='0 day':  # 소요시간이 0 day인 것만 따로 추출
        time = time.append({'소요시간':df.time[i][6:]},ignore_True)
    i+=1

# 소요시간을 seconds로 환산
total_minute = 0
for i in range(len(time)):
    total_minute += pd.to_numeric(time.소요시간[i][4:6])
    i+=1

total_second = 0
for i in range(len(time)):
    total_second += pd.to_numeric(time.소요시간[i][7:10])
    i+=1

time_to_second = (total_minute * 60 + total_second0 ) / len(time)
print(time_to_second)  # 청약시작부터 완료까지 총 소요된 시간을 seconds로 환산한 값

# 소요시간별로 분포 확인
minutes_1 = []
minutes_2 = []
minutes_3 = []
minutes_4 = []
minutes_5 = []
minutes_6 = []
minutes_7 = []
minutes_8 = []
minutes_9 = []
minutes_10 = []
minutes_10_over = []

for i in len(range(time)):
    if time.소요시간[i][4:6]=='01':
        minutes_1.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='02':
        minutes_2.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='03':
        minutes_3.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='04':
        minutes_4.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='05':
        minutes_5.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='06':
        minutes_6.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='07':
        minutes_7.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='08':
        minutes_8.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='09':
        minutes_9.append(time.소요시간[i])
    elif time.소요시간[i][4:6]=='10':
        minutes_10.append(time.소요시간[i])
    elif time.소요시간[i][4:6]>'10':
        minutes_10_over.append(time.소요시간[i])

    i+=1

# 한글폰트 load
import platform
from matplotlib import rc
rc('font',family = 'NanumGothic')

# Visualization
plt.figure(figsize=(8,5))
plt.plot(['1분','2분','3분','4분','5분','6분','7분','8분','9분','10분','10분초과'],
         [len(minutes_1),len(minutes_2),len(minutes_3),len(minutes_4),len(minutes_5),len(minutes_6),
          len(minutes_7),len(minutes_8),len(minutes_9),len(minutes_10),len(minutes_10_over)])
plt.xlabel('소요시간')
plt.ylabel('접속ID수')
plt.show()
plt.tight_layout


# 단계별 청약소요시간
청약완료 = list(test[test['업무단계순서']==61]['접속ID'])
test_final = test[test['업무단계순서']==61]['접속ID'].isin(청약완료)  # 청약완료까지 진행한 접속ID 데이터

# 각 단계별로 도달한 접속 ID 수가 다르므로 루프문을 돌리기 위해서는 단계별 list parsing이 필요함
보험상품가입 = list(set(test_final[(test_final['업무단계순서']==12)]['접속ID']))
본인인증 = list(set(test_final[(test_final['업무단계순서']==21)]['접속ID']))
가입설계동의 = list(set(test_final[(test_final['업무단계순서']==32)]['접속ID']))

from tqdm import tqdm

df = pd.DataFrame([],columns = ['ID','time'])

for ID in tqdm(청약완료):
    df = df.append({'ID':ID,'time':str(
        (min(test[(test['접속ID']==ID)&(test['업무단계순서']==도달단계업무순서)].처리시간 -  # 각 ID별로 여러번 단계별 접속 log가 남으므로
         max(test[(test['접속ID']==ID)&(test['업무단계순서']==출발단계업무순서)].처리시간))  # 다음단계로 넘어가는 가장 짧은 경로로 소요시간을 계산
    )},ignore_index = True)                                               # (가장 최근 도달시간 - 가장 마지막 출발시간)

time = pd.DataFrame([],columns = ['소요시간'])

for i in range(len(df)):
    if df.time[i][:5] == '0day':
        time = time.append({'소요시간':df.time[i][6:]},ignore_index=True)
    i+=1

total_minute = 0
for i in range(len(time)):
    total_minute += pd.to_numeric(time.소요시간[i][4:6])
    i+=1

total_second = 0
for i in range(len(time)):
    total_second += pd.to_numeric(time.소요시간[i][7:10])
    i+=1

time_to_second = (total_minute * 60 + total_second)/len(time)
print(time_to_second)