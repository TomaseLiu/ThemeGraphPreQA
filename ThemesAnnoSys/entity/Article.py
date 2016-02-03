from django.db import models


class Article():
    file_name = ""
    news_id = ""
    title = ""
    pub_time_src = ""
    body = ""
    index = 0

    next_unremark_page_index = 0

    remark_num = 0
    good_words = []
    bad_words = []
    my_good_words = []
    my_bad_words = []

    def __init__(self, file_name, news_id, title, pub_time_src, body, index=0):
        self.file_name = file_name
        self.news_id = news_id
        self.title = title
        self.pub_time_src = pub_time_src
        self.body = body
        self.index = index


    def __lt__(self, other):
        return int(self.index) < int(other.index)
