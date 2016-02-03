class Keyword():
    #keyword
    word = ""
    #source of keyword: zheshang, report, news
    keyword_source = ""
    #modifing status code of this keyword: 0, no modifing; 1, added; -1, deleted;
    modify_status = 0
    

    def __init__(self, word, keyword_source, modify_status):
        self.word = word
        self.keyword_source = keyword_source
        self.modify_status = modify_status
