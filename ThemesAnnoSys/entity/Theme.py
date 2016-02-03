class ThemeBasicInfo():
    theme_name = ""
    theme_id = 0
    theme_index = 0
    theme_version_list = []
    theme_lastest_version = ""
    theme_article_count = 0
    
    def __init__(self, theme_name, theme_id, theme_index, theme_version_list, theme_lastest_version, theme_article_count):
        self.theme_name = theme_name
        self.theme_id = theme_id
        self.theme_index = theme_index
        self.theme_version_list = theme_version_list
        self.theme_lastest_version = theme_lastest_version
        self.theme_article_count = theme_article_count

    def __lt__(self, other):
        return self.theme_name < other.theme_name

class ThemeArticleAnnoBasicInfo():
    #type: ThemeBasicInfo
    theme_basic_info = None
    theme_anno_count = 0
    theme_news_anno_count = 0
    theme_anno_accuracy = 100
    
    def __init__(self, theme_basic_info, theme_anno_count, theme_news_anno_count, theme_anno_accuracy):
        self.theme_basic_info = theme_basic_info
        self.theme_anno_count = theme_anno_count
        self.theme_news_anno_count = theme_news_anno_count
        self.theme_anno_accuracy = theme_anno_accuracy


class UserBasicInfo():
    user_name = ""
    user_id = 0


class UserThemeArticleAnnoBasicInfo():
    #type: ThemeArticleAnnoBasicInfo
    theme_article_anno_info = None
    user_name = ""

    user_theme_anno_count = 0
    user_theme_last_anno_index = 0

    def __init__(self, theme_article_anno_info, user_name, user_theme_anno_count, user_theme_last_anno_index):
        self.theme_article_anno_info = theme_article_anno_info
        self.user_name = user_name
        self.user_theme_anno_count = user_theme_anno_count
        self.user_theme_last_anno_index = user_theme_last_anno_index

