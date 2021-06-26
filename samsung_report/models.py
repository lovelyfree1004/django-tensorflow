from konlpy.tag import Okt
from nltk.tokenize import word_tokenize
import nltk
import re
import pandas as pd
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from icecream import ic

class SamsungReport(object):

    def __init__(self):
        self.okt = Okt()

    def read_file(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        fname = './data/kr-Report_2018.txt'
        with open(fname, 'r', encoding='utf-8') as f:
            texts = f.read()
        return texts

    def extract_hangeul(self, texts):
        temp = texts.replace('\n', ' ')
        tokenizer = re.compile(r'[^ ㄱ-힣]+')
        return tokenizer.sub('',temp)

    def change_token(self, texts):
        return word_tokenize(texts)

    def extract_noun(self):
        # 삼성전자의 스마트폰은 -> 삼성전자 스마트폰
        noun_tokens = []
        tokens = self.change_token(self.extract_hangeul(self.read_file()))
        for i in tokens:
            pos = self.okt.pos(i)
            temp = [j[0] for j in pos if j[1] == 'Noun']
            if len(''.join(temp)) > 1 :
                noun_tokens.append(''.join(temp))
        texts = ' '.join(noun_tokens)
        ic(texts[:100])
        return texts

    def read_stopword(self):
        self.okt.pos("삼성전자 글로벌센터 전자사업부", stem=True)
        fname = './data/stopwords.txt'
        with open(fname, 'r', encoding='utf-8') as f:
            stopwords = f.read()
        return stopwords

    def remove_stopword(self):
        texts = self.extract_noun()
        tokens = self.change_token(texts)
        # print('------- 1 명사 -------')
        # print(texts[:30])
        stopwords = self.read_stopword()
        # print('------- 2 스톱 -------')
        # print(stopwords[:30])
        # print('------- 3 필터 -------')
        texts = [text for text in tokens
                 if text not in stopwords]
        # print(texts[:30])
        return texts

    def find_freq(self):
        texts = self.remove_stopword()
        freqtxt = pd.Series(dict(FreqDist(texts))).sort_values(ascending=False)
        ic(freqtxt[:30])
        return freqtxt

    def draw_wordcloud(self):
        texts = self.remove_stopword()
        wcloud = WordCloud('./data/D2Coding.ttf', relative_scaling=0.2,
                           background_color='white').generate(" ".join(texts))
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    # nltk.download()
    instance = SamsungReport()
    instance.find_freq()
    instance.draw_wordcloud()