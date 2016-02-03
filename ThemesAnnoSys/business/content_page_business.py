import os
import sys
import inspect

SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))

module_dirs = ["entity", "business"]

for module_dir in module_dirs:
    sys.path.append(os.path.join(SCRIPT_DIR, module_dir))


themes_data_dir = os.path.join(SCRIPT_DIR, "../data/themes")


import Theme
import file_tools
import db_tools

def get_theme_user_anno_info_obj_list(user_name):
    """
    get themes' annotation infomation (article count, account of annotated articles, account of articles which have been annotated by current user, accuracy ....)
    @Param str: login user's name
    @Return list: list[Theme.UserThemeArticleAnnoBasicInfo]
    """
    theme_obj_list = file_tools.get_theme_obj_list(themes_data_dir)
    all_themes_anno_basic_info_dict = db_tools.get_all_themes_anno_basic_info()

    theme_user_anno_info_obj_list = []

    for theme in theme_obj_list:
        theme_user_anno_article_count, lastest_anno_page_id = db_tools.get_theme_user_article_info(theme.theme_name, user_name, theme.theme_lastest_version)
        theme_anno_count = 0
        theme_news_anno_count = 0
        theme_anno_accuracy = 100
        if (theme.theme_name, theme.theme_lastest_version) in all_themes_anno_basic_info_dict:
            [theme_anno_count, theme_news_anno_count, theme_news_anno_strong_count, theme_news_anno_weak_count, theme_news_anno_not_count] = all_themes_anno_basic_info_dict[(theme.theme_name, theme.theme_lastest_version)]
            theme_anno_accuracy = int(100*(1 + float(theme_news_anno_strong_count + theme_news_anno_weak_count))/(1 + float(theme_news_anno_strong_count + theme_news_anno_weak_count + theme_news_anno_not_count)))

        theme_article_anno_basic_info_obj = Theme.ThemeArticleAnnoBasicInfo(theme, theme_anno_count, theme_news_anno_count, theme_anno_accuracy)
        user_theme_anno_basic_info_obj = Theme.UserThemeArticleAnnoBasicInfo(theme_article_anno_basic_info_obj, user_name, theme_user_anno_article_count, lastest_anno_page_id)

        theme_user_anno_info_obj_list.append(user_theme_anno_basic_info_obj)

    return theme_user_anno_info_obj_list
