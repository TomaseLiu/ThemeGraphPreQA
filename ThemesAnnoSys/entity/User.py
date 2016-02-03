class UserBasicInfo():
    user_name = ""
    user_id = ""
    user_group = ""


    def __init__(self, user_name, user_id, user_group):
        self.user_name = user_name
        self.user_id = user_id
        self.user_group = user_group


class UserAnnoInfo(UserBasicInfo):
    user_anno_articles_count = 0
    user_anno_keywords_count = 0
    user_anno_themes_count = 0

    def __init__(self, user_name, user_id, user_group, user_anno_articles_count, user_anno_keywords_count, user_anno_themes_count):
        UserBasicInfo.__init__(user_name, user_id, user_group)
        self.user_anno_articles_count = user_anno_articles_count
        self.user_anno_keywords_count = user_anno_keywords_count
        self.user_anno_themes_count = user_anno_themes_count
    
