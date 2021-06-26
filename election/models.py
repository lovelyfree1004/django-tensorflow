from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib import rc
from django.db import models
import numpy as np
import folium
import json
import warnings
# from monaco.common.models import FileDTO, Printer, Reader
from matplotlib import font_manager, rc
import pandas as pd
from icecream import ic

@dataclass
class File(object):
    context: str
    fname: str
    url: str
    dframe: object
    @property
    def context(self) -> str: return self._context
    @context.setter
    def context(self, context):
        self._context = context
    @property
    def fname(self) -> str: return self._fname
    @fname.setter
    def fname(self, fname): self._fname = fname
    @property
    def dframe(self) -> object: return self._dframe
    @dframe.setter
    def dframe(self, dframe): self._dframe = dframe
    @property
    def url(self) -> object: return self._url
    @url.setter
    def url(self, url): self._url = url
class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def dframe(self):
        pass
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
class ScraperBase(metaclass=ABCMeta):
    @abstractmethod
    def driver(self):
        pass
class Printer(PrinterBase):
    def dframe(self, this):
        ic(type(this))
        ic(this.columns)
        ic(this.head())
        ic(this.isnull().sum())
class Reader(ReaderBase):
    def new_file(self, file) -> str:
        return file.context + file.fname
    def csv(self, file) -> object:
        return pd.read_csv(f'{self.new_file(file)}.csv', encoding='UTF-8', thousands=',')
    def xls(self, file, header, usecols) -> object:
        return pd.read_excel(f'{self.new_file(file)}.xls', header=header, usecols=usecols)
    def csv_header(self, file, header) -> object:
        return pd.read_csv(f'{self.new_file(file)}.csv', encoding='UTF-8', thousands=',', header=header)
    def json(self, file) -> object:
        return json.load(open(f'{self.new_file(file)}.json', encoding='UTF-8'))

class Election_19th(object):

    def __init__(self):
        self.file = File()
        self.reader = Reader()
        self.printer = Printer()
        self.BORDER_LINES = [[(5, 1), (5,2), (7,2), (7,3), (11,3), (11,0)], # 인천
    [(5,4), (5,5), (2,5), (2,7), (4,7), (4,9), (7,9),
     (7,7), (9,7), (9,5), (10,5), (10,4), (5,4)], # 서울
    [(1,7), (1,8), (3,8), (3,10), (10,10), (10,7),
     (12,7), (12,6), (11,6), (11,5), (12, 5), (12,4),
     (11,4), (11,3)], # 경기도
    [(8,10), (8,11), (6,11), (6,12)], # 강원도
    [(12,5), (13,5), (13,4), (14,4), (14,5), (15,5),
     (15,4), (16,4), (16,2)], # 충청북도
    [(16,4), (17,4), (17,5), (16,5), (16,6), (19,6),
     (19,5), (20,5), (20,4), (21,4), (21,3), (19,3), (19,1)], # 전라북도
    [(13,5), (13,6), (16,6)], # 대전시
    [(13,5), (14,5)], #세종시
    [(21,2), (21,3), (22,3), (22,4), (24,4), (24,2), (21,2)], #광주
    [(20,5), (21,5), (21,6), (23,6)], #전라남도
    [(10,8), (12,8), (12,9), (14,9), (14,8), (16,8), (16,6)], #충청북도
    [(14,9), (14,11), (14,12), (13,12), (13,13)], #경상북도
    [(15,8), (17,8), (17,10), (16,10), (16,11), (14,11)], #대구
    [(17,9), (18,9), (18,8), (19,8), (19,9), (20,9), (20,10), (21,10)], #부산
    [(16,11), (16,13)], #울산
    [(27,5), (27,6), (25,6)],]

    def draw_data(self, tar_dara, campname):
        file = self.file
        reader = self.reader
        BORDER_LINES = self.BORDER_LINES
        file.context = './data/'
        file.fname = 'final_elect_data'
        elec = reader.csv(file)
        gamma = 0.75
        whitelabelmin = 20.
        datalabel = tar_dara
        tmp_max = max([np.abs(min(elec[tar_dara])),
                       np.abs(max(elec[tar_dara]))])
        vmin, vmax = -tmp_max, tmp_max
        mapdata = elec.pivot_table(index='y', columns='x', values=tar_dara)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)
        # plt.rc('font', family='NanumGothic')
        plt.rc('font', family=font_manager
               .FontProperties(fname='C:/Windows/Fonts/H2GTRM.TTF')
               .get_name())
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=(9, 11))
        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=campname,
                   edgecolor='#aaaaaa', linewidth=0.5)
        # 지역 이름 표시
        for idx, row in elec.iterrows():
            # 광역시는 구 이름이 겹치는 경우가 많아서 시단위 이름도 같이 표시
            # (중구, 서구)
            if len(row['ID'].split()) == 2:
                dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
            elif row['ID'][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row['ID']
            # 서대문구, 서귀포시 같이 이름이 3자 이상인 경우에 작은 글자로 표시
            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.
            annocolor = 'white' if np.abs(row[tar_dara]) > whitelabelmin else 'black'
            plt.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)
        # 시도 경계
        for path in BORDER_LINES:
            ys, xs = zip(*path)
            plt.plot(xs, ys, c='black', lw=2)
        plt.gca().invert_yaxis()
        plt.axis('off')
        cb = plt.colorbar(shrink=.1, aspect=10)
        cb.set_label(datalabel)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    e = Election_19th()
    # e.draw_data('moon_vs_hong','RdBu')
    e.draw_data('moon_vs_ahn', 'RdBu')
    # e.draw_data('ahn_vs_hong', 'RdBu')