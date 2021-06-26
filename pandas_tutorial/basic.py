import pandas as pd
import numpy as np
import random
import string
from icecream import ic

np.random.seed(50)

'''
pd.Series : 배열
pd.DataFrame : 배열 + 배열 -> 행렬( := 엑셀 시트, 테이블 )
데이터프레임은 컬럼, 인덱스, 데이터(=values) 로 이뤄진다.
'''

pd.DataFrame({}, index=[])
# {} 딕셔너리로 생성하는 방법
df = pd.DataFrame({"a" : [1, 2], "b" : [3, 4],  "c" : [5, 6] }, index=[1,2]) # "" 컬럼, [] 데이터, index 인덱스

# [] 리스트로 생성하는 방법
df2 = pd.DataFrame([[1, 2, 3],[4, 5, 6]], index=[1,2], columns=['a','b','c'])


def id(): return ''.join(random.choice(string.ascii_letters) for i in range(5))
def score(): return np.random.randint(0,101)
# 데이터프레임을 생성자로 생성한 방식
grade = pd.DataFrame([[score() for i in range(1, 5)] for i in range(1,11) ],
             index= [id() for i in range(1,11)],
             columns = ['국어','영어','수학','과학'])

# ic(grade)

# 딕셔너리 + loc 를 활용해서 생성하는 방법
grade2 = pd.DataFrame({"국어":score(), "영어":score(), "수학":score(), "과학":score() }, index=[id()])
for i in range(1,11):
    grade2.loc[id()] = {"국어":score(), "영어":score(), "수학":score(), "과학":score() }

ic(grade2)