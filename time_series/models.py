import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pandas_datareader.data as web
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from fbprophet import Prophet
from datetime import datetime
from pandas_datareader import data
import yfinance as yf
yf.pdr_override()
path = "c:/Windows/Fonts/malgun.ttf"
import platform
from matplotlib import font_manager, rc
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')
plt.rcParams['axes.unicode_minus'] = False
'''
시계열 데이터 
: 일련의 순차적으로 정해진 데이터 셋의 집합
: 시간에 관해 순서가 매겨져 있다는 점과, 연속한 관측치는 서로 상관관계를 갖고 있다
회귀분석
: 관찰된 연속형 변수들에 대해 두 변수 사이의 모형을 구한뒤 적합도를 측정해 내는 분석 방법
'''

class Model(object):

    def seasonal(self):
        start_date = '2018-1-4'
        end_date = '2021-6-30'
        KIA = data.get_data_yahoo('000270.KS', start_date, end_date)
        # ic(KIA.head())
        # ic(KIA.tail())

        KIA['Close'].plot(figsize=(12,6),grid=True)

        # 일부데이터로 forecast

        KIA_trunc = KIA[:'2021-12-31']
        df = pd.DataFrame({'ds': KIA_trunc.index,'y': KIA_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']

        ic(df.head())

        m = Prophet(daily_seasonality=True)
        m.fit(df)
        future = m.make_future_dataframe(periods=61)
        future.tail()
        forecast = m.predict(future)

        m.plot(forecast)
        plt.figure(figsize=(12,6))
        plt.plot(KIA.index, KIA['Close'], label='real')
        plt.plot(forecast['ds'], forecast['yhat'], label='forecast')
        plt.grid()
        plt.legend()
        plt.show()

    def forecast(self, df):
        df = df.rename(columns = {"date":"ds", "hit":"y"})
        df.reset_index(inplace=True)
        df['ds'] =pd.to_datetime(df['ds'], format="%y. %m. %d.")
        m = Prophet(yearly_seasonality=True, daily_seasonality=True)
        # 주기성이 연단위 및 일단위로 있다
        m.fit(df)

        future = m.make_future_dataframe(periods=60) # 60일만큼 예측
        ic(future.tail())
        forecase = m.predict(future)
        ic(future.head())

        forecase[['ds','yhat','yhat_lower','yhat_upper']].tail()
        # 확인하고 싶은 변수들만 뽑아내서 확인

        forecase[['ds','yhat','yhat_lower','yhat_upper']].tail()

        # 시각화
        m.plot(forecase)
        m.plot_components(forecase)

    # RMSE(Root Mean Square Error, 표준편차)을 계산해주는 error() 함수를 생성
    # f(x)는 예측값, y는 실제값
    # sqrt-> 제곱근 함수. 루트 역할
    def error(self, f, x, y):
        return np.sqrt(np.mean((f(x) - y) ** 2))

    def regression(self):
        df = pd.read_csv('./data/Web-Traffic.csv', encoding="utf-8",  thousands=",",header=None)  # common.models.py 수정필요!
        df.columns = ['date', 'hit']
        df = df[df['hit'].notnull()]
        print(df.head())
        #  df 시각화
        df['hit'].plot(figsize=(12, 4), grid=True)
        # 주기성 확인위한 작업
        # len은 매개변수의 요소의 개수
        # pinkwink_web index 값으로 이루어진 array 생성
        time = np.arange(0, len(df))
        # 웹 트래픽의 자료를 traffic 변수에 저장
        traffic = df['hit'].values
        # linespace()함수는 두 수 사이를 50개의 균일한 간격의 수를 배열로 만들어준다.
        fx = np.linspace(0, time[-1], 1000)
        '''
        polyfit(x, y, 함수의 차수)
        -> x와  y로 이루어진 그래프에서 함수의 차수의 계수를 찾아 본래 데이터의 기울기와 절편의 값과 
        유사하게 만들어 직선의 그래프로 만들어준다. 
        '''
        #  1차원 다항식
        fp1 = np.polyfit(time, traffic, 1)  # 1차원 다항식으로 생성 후 계수 도출
        f1 = np.poly1d(fp1)  # 도출한 계수로 다시 다항식 생성 후 계수 도출
        #  2차원 다항식
        f2p = np.polyfit(time, traffic, 2)
        f2 = np.poly1d(f2p)
        # 3차원 다항식
        f3p = np.polyfit(time, traffic, 3)
        f3 = np.poly1d(f3p)
        # 15차원 다항식
        f15p = np.polyfit(time, traffic, 15)
        f15 = np.poly1d(f15p)
        # error 함수를 통해 오차의 표준편차 즉, 잔차 제곱합을 구한다.
        # 데이터와 추정 모델 간의 불일치를 측정
        print(f' 1차원 다항식의 불일치 정도: {self.error(f1, time, traffic)}')
        print(f' 2차원 다항식의 불일치 정도: {self.error(f2, time, traffic)}')
        print(f' 3차원 다항식의 불일치 정도: {self.error(f3, time, traffic)}')
        print(f' 15차원 다항식의 불일치 정도: {self.error(f15, time, traffic)}')
        # 각 차원의 다항식 시각화
        plt.figure(figsize=(10, 6))
        plt.scatter(time, traffic, s=10)  # scatter 함수를 통해 그래프 상에 점 찍기
        plt.plot(fx, f1(fx), lw=4, label='f1')  # plot 함수를 통해 그래프 생성
        plt.plot(fx, f2(fx), lw=4, label='f2')
        plt.plot(fx, f3(fx), lw=4, label='f3')
        plt.plot(fx, f15(fx), lw=4, label='f15')
        plt.grid(True, linestyle='-', color='0.75')  # 그래프 상에 격자무늬 표현
        plt.legend(loc=2)
        # 이 그래프가 무엇을 의미하는지 알기 위해, label, scatter 을 plot안에 사용해야하며,
        # 그리고 plt.legend()를 실행해야 한다.
        # plt.show()
        return df



if __name__ == '__main__':
    m = Model()
    # m.seasonal()
    df = m.regression()
    m.forecast(df)