# -*- coding: utf-8 -*-
from sphinx.search import SearchLanguage
from smallseg import SEG 

class SearchChinese(SearchLanguage):
    lang = 'zh'

    def init(self, options):
        print("reading Chiniese dictionary")
        self.seg = SEG() 

    def split(self, input):
        return self.seg.cut(input) 

    def word_filter(self, stemmed_word):
        return len(stemmed_word) > 1