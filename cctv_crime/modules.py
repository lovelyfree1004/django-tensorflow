from dataclasses import dataclass
from abc import *
import pandas as pd
import numpy as np
import json
import googlemaps
from sklearn import preprocessing
import folium

@dataclass
class File(object):
    context: str
    fname: str
    dframe: object

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def dframe(self) -> str: return self._dframe

    @dframe.setter
    def dframe(self, dframe): self._dframe = dframe

class ReaderBase(metaclass=ABCMeta):

    @abstractmethod
    def new_file(self):
        pass

    @abstractmethod
    def csv(self):
        pass

    @abstractmethod
    def xls(self):
        pass

    @abstractmethod
    def json(self):
        pass

class PrinterBase(metaclass=ABCMeta):

    @abstractmethod
    def dframe(self):
        pass

class Reader(ReaderBase):

    def new_file(self, file) -> str:
        return file.context + file.fname

    def csv(self, file) -> object:
        return pd.read_csv(f'{self.new_file(file)}.csv', encoding='UTF-8', thousands=',')

    def xls(self, file, header, usecols) -> object:
        return pd.read_excel(f'{self.new_file(file)}.xls', header=header, usecols=usecols)

    def json(self, file) -> object:
        return json.load(open(f'{self.new_file(file)}.json', encoding='UTF-8'))

    def gmaps(self) -> object:
        return googlemaps.Client(key='AIzaSyCmfXM1pd-g-WsNCdWNJwfMOuFR828y5IE')

class Printer(PrinterBase):
    def dframe(self, this):
        print('*' * 100)
        print(f'1. Target type \n {type(this)} ')
        print(f'2. Target column \n {this.columns} ')
        print(f'3. Target top 1개 행\n {this.head(1)} ')
        print(f'4. Target bottom 1개 행\n {this.tail(1)} ')
        print(f'4. Target null 의 갯수\n {this.isnull().sum()}개')
        print('*' * 100)

'''
**************************************** crime in seoul ****************************************************
1. Target type 
 <class 'pandas.core.frame.DataFrame'> 
2. Target column 
 Index(['관서명', '살인 발생', '살인 검거', '강도 발생', '강도 검거', '강간 발생', '강간 검거', '절도 발생',
       '절도 검거', '폭력 발생', '폭력 검거'],
      dtype='object') 
3. Target top 1개 행
    관서명  살인 발생  살인 검거  강도 발생  강도 검거  강간 발생  강간 검거  절도 발생  절도 검거  폭력 발생  폭력 검거
0  중부서      2      2      3      2    105     65   1395    477   1355   1170 
4. Target bottom 1개 행
     관서명  살인 발생  살인 검거  강도 발생  강도 검거  강간 발생  강간 검거  절도 발생  절도 검거  폭력 발생  폭력 검거
30  수서서     10      7      6      6    149    124   1439    666   1819   1559 
4. Target null 의 갯수
 관서명      0
살인 발생    0
살인 검거    0
강도 발생    0
강도 검거    0
강간 발생    0
강간 검거    0
절도 발생    0
절도 검거    0
폭력 발생    0
폭력 검거    0
dtype: int64개
********************************************* cctv in seoul ***************************************************
1. Target type 
 <class 'pandas.core.frame.DataFrame'> 
2. Target column 
 Index(['기관명', '소계', '2013년도 이전', '2014년', '2015년', '2016년'], dtype='object') 
3. Target top 1개 행
    기관명    소계  2013년도 이전  2014년  2015년  2016년
0  강남구  2780       1292    430    584    932 
4. Target bottom 1개 행
     기관명   소계  2013년도 이전  2014년  2015년  2016년
24  중랑구  660        509    121    177    109 
*****************************************  pop_in_seoul  *****************************************
1. Target type 
 <class 'pandas.core.frame.DataFrame'> 
2. Target column 
 Index(['자치구', '계', '계.1', '계.2', '65세이상고령자'], dtype='object') 
3. Target top 1개 행
   자치구           계        계.1       계.2   65세이상고령자
0  합계  10197604.0  9926968.0  270636.0  1321458.0 
4. Target bottom 1개 행
     자치구   계  계.1  계.2  65세이상고령자
26  NaN NaN  NaN  NaN       NaN 
'''

class Service(Reader):

    def __init__(self):
        self.file = File()
        self.reader = Reader()
        self.printer = Printer()

        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

    def save_police_pos(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        file.context = './data/'
        file.fname = 'crime_in_seoul'
        crime = reader.csv(file)
        # printer.dframe(crime)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps()
        for name in station_names:
            temp = gmaps.geocode(name, language='ko')
            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
            # print(f'name{temp[0].get("formatted_address")}')
        gu_names = []
        for name in station_addrs:
            t = name.split()
            gu_name = [gu for gu in t if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        # 구와 경찰서 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] == '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] == '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] == '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] == '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] == '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] == '강남구'
        crime.to_csv('./saved_data/police_pos.csv')

    def save_cctv_pop(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        file.context = './data/'
        file.fname = 'cctv_in_seoul'
        cctv = reader.csv(file)
        # printer.dframe(cctv)
        file.fname = 'pop_in_seoul'
        pop = reader.xls(file, 2, 'B, D, G, J, N')
        # printer.dframe(pop)
        cctv.rename(columns={cctv.columns[0]: '구별'},inplace=True)
        pop.rename(columns={
            pop.columns[0]: '구별',
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자'
        }, inplace=True)
        pop.drop([26],inplace=True)
        pop['외국인비율'] = pop['외국인'].astype(int) / pop['인구수'].astype(int) * 100
        pop['고령자비율'] = pop['고령자'].astype(int) / pop['인구수'].astype(int) * 100
        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], 1, inplace=True)
        cctv_pop = pd.merge(cctv, pop, on='구별')
        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        print(f'고령자비율과 CCTV의 상관계수 {str(cor1)} \n'
              f'외국인비율과 CCTV의 상관계수 {str(cor2)} ')
        """
         고령자비율과 CCTV 의 상관계수 [[ 1.         -0.28078554]
                                     [-0.28078554  1.        ]] 
         외국인비율과 CCTV 의 상관계수 [[ 1.         -0.13607433]
                                     [-0.13607433  1.        ]]
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        고령자비율 과 CCTV 상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
                                    [-0.28078554  1.        ]]
        외국인비율 과 CCTV 상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
                                    [-0.13607433  1.        ]]                        
         """
        cctv_pop.to_csv('./saved_data/cctv_pop.csv')

    def save_police_norm(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        file.context = './saved_data/'
        file.fname = 'police_pos'
        police_pos = reader.csv(file)
        police = pd.pivot_table(police_pos, index='구별', aggfunc=np.sum)
        police['살인검거율'] = (police['살인 검거'].astype(int) / police['살인 발생'].astype(int)) * 100
        police['강도검거율'] = (police['강도 검거'].astype(int) / police['강도 발생'].astype(int)) * 100
        police['강간검거율'] = (police['강간 검거'].astype(int) / police['강간 발생'].astype(int)) * 100
        police['절도검거율'] = (police['절도 검거'].astype(int) / police['절도 발생'].astype(int)) * 100
        police['폭력검거율'] = (police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int)) * 100
        police.drop(columns={'살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'}, axis=1, inplace=True)
        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, 1] = 100  # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        }, inplace=True)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """          
        스케일링은 선형변환을 적용하여          
        전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
        정규화 normalization         
        많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나         
        분포(스케일)를 유사하게 만드는 작업
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_columns, index=police.index)
        police_norm[self.crime_rate_columns] = police[self.crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv('./saved_data/police_norm.csv', sep=',', encoding='UTF-8')

    def folium_test(self):
        file = self.file
        reader = self.reader
        printer = self.printer
        file.context = './data/'
        file.fname = 'us_unemployment'
        state_data = reader.csv(file)
        file.fname = 'us-states'
        state_geo = reader.json(file)

        bins = list(state_data["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))

        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="BuPu",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name="Unemployment Rate (%)",
            bins=bins,
            reset=True,
        ).add_to(m)

        m.save('./saved_data/Unemployment.html')

    def draw_crime_map(self):
        file = self.file
        reader = self.reader
        file.context = './saved_data/'
        file.fname = 'police_norm'
        police_norm = reader.csv(file)
        file.context = './data/'
        file.fname = 'geo_simple'
        state_geo = reader.json(file)
        file.fname = 'crime_in_seoul'
        crime = reader.csv(file)
        file.context = './saved_data/'
        file.fname = 'police_pos'
        police_pos = reader.csv(file)
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps()
        for name in station_names:
            temp = gmaps.geocode(name, language='ko')
            station_addrs.append(temp[0].get('formatted_address'))
            t_loc = temp[0].get('geometry')
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])

        police_pos['lat'] = station_lats
        police_pos['lng'] = station_lngs
        col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        tmp = police_pos[col] / police_pos[col].max()
        police_pos['검거'] = np.sum(tmp, axis=1)

        folium_map = folium.Map(location=[37.5502, 126.982], zoom_start=12, title='Stamen Toner')

        folium.Choropleth(
            geo_data=state_geo,
            data=tuple(zip(police_norm['구별'],police_norm['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True,
        ).add_to(folium_map)
        for i in police_pos.index:
            folium.CircleMarker([police_pos['lat'][i], police_pos['lng'][i]],
                                radius=police_pos['검거'][i] * 10,
                                fill_color='#0a0a32').add_to(folium_map)

        folium_map.save('./saved_data/crime_map.html')


if __name__ == '__main__':

    s = Service()
    # s.save_police_pos()
    # s.save_cctv_pop()
    # s.save_police_norm()
    # s.folium_test()
    s.draw_crime_map()