#encoding=utf-8
import sys
import os
import inspect


SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
local_module_dirs = ["entity", "business"]

for module_dir in local_module_dirs:
        sys.path.append(os.path.join(SCRIPT_DIR, module_dir))

import db_api
import Theme
import file_tools

"""
tools for getting data from database
"""



"""
get all themes' annotation basic informations from db;
@Param
@Return dict: theme_anno_count_dict, key: (theme_name, theme_version_id), value: [anno count of current theme and version, ...]
"""
def get_all_themes_anno_basic_info():
    get_theme_anno_basic_info_group_by_theme_sql = "select ThemeName as theme_name, ThemeVersionID as theme_version_id, count(*) as theme_anno_count, count(distinct NewsID) as theme_news_anno_count, sum(if(AnnoCorr='Strong', 1, 0)) as corr_strong, sum(if(AnnoCorr='Weak', 1, 0)) as corr_weak, sum(if(AnnoCorr='Not', 1, 0)) as corr_not from theme_news_anno group by ThemeName, ThemeVersionID"
    cursor, conn = db_api.conn()
    db_api.query(cursor, get_theme_anno_basic_info_group_by_theme_sql)
    theme_anno_count_dict = {}
    row = db_api.fetch_one_row(cursor)
    while row != None:
        theme_name = row['theme_name']
        theme_version_id = row['theme_version_id']
        theme_anno_count = row['theme_anno_count']
        theme_news_anno_count = row['theme_news_anno_count']
        theme_news_anno_strong_count = row['corr_strong']
        theme_news_anno_weak_count = row['corr_weak']
        theme_news_anno_not_count = row['corr_not']

        theme_anno_count_dict[(theme_name, theme_version_id)] = [theme_anno_count, theme_news_anno_count, theme_news_anno_strong_count, theme_news_anno_weak_count, theme_news_anno_not_count]
        row = db_api.fetch_one_row(cursor)

    db_api.close(cursor)
        
    return theme_anno_count_dict





def get_theme_anno_basic_info(theme_name):
    """
    get some theme's anno basic information from db with it's name
    @Param str: theme's name
    @Return dict: key: version_id, value: list [...]
    """
    get_theme_anno_basic_info_sql = "select ThemeVersionID as theme_version_id, count(*) as theme_anno_count, count(distinct NewsID) as theme_news_anno_count, sum(if(AnnoCorr='Strong', 1, 0)) as corr_strong, sum(if(AnnoCorr='Weak', 1, 0)) as corr_weak, sum(if(AnnoCorr='Not', 1, 0)) as corr_not from theme_news_anno where ThemeName='%s' group by ThemeVersionID"
    
    cursor, conn = db_api.conn()
    db_api.query(cursor, get_theme_anno_basic_info_sql)
    theme_anno_count_dict = {}
    row = db_api.fetch_one_row(cursor)
    while row != None:
        theme_version_id = row['theme_version_id']
        theme_anno_count = row['theme_anno_count']
        theme_news_anno_count = row['theme_news_anno_count']
        theme_news_anno_strong_count = row['corr_strong']
        theme_news_anno_weak_count = row['corr_weak']
        theme_news_anno_not_count = row['corr_not']

        theme_anno_count_dict[theme_version_id] = [theme_anno_count, theme_news_anno_count, theme_news_anno_strong_count, theme_news_anno_weak_count, theme_news_anno_not_count]
        row = db_api.fetch_one_row(cursor)

    db_api.close(cursor)

    return theme_anno_count_dict


def get_user_anno_basic_info(user_name):
    """
    get some user's annotation information, like how much article have he or she remarked;
    @Param str: user's name
    @Return int: count of annotations of the user;
    """
    get_user_anno_basic_info_sql = "select count(*) as user_anno_count from theme_news_anno where UserName='%s'"
    cursor, conn = db_api.conn()
    db_api.query(cursor, get_user_anno_basic_info_sql % user_name)
    row = db_api.fetch_one_row(cursor)
    user_anno_count = row['user_anno_count']

    db_api.close(cursor)
    return user_anno_count



def get_theme_user_article_info(theme_name, user_name, version_id):
    """
    @Param str: theme name
    @Param str: user name
    @Param str: version id
    """
    print("get_theme_user_article_info")
    get_theme_user_article_anno_count_info_sql = "select count(distinct NewsID) as theme_user_article_anno_count from theme_news_anno where ThemeName = '%s' and ThemeVersionID = '%s' and UserName = '%s'"
    get_theme_user_article_anno_last_page_id_sql = "select NewsPageID as lastest_anno_page_id from theme_news_anno where ThemeName = '%s' and ThemeVersionID = '%s' and UserName = '%s' order by InsertTime desc limit 1"

    cursor, conn = db_api.conn()
    db_api.query(cursor, get_theme_user_article_anno_count_info_sql % (theme_name, version_id, user_name))
    row = db_api.fetch_one_row(cursor)
    theme_user_anno_article_count = 0
    if row != None:
        theme_user_anno_article_count = row['theme_user_article_anno_count']

    db_api.query(cursor, get_theme_user_article_anno_last_page_id_sql % (theme_name, version_id, user_name))
    row = db_api.fetch_one_row(cursor)
    lastest_anno_page_id = 1
    if row != None:
        lastest_anno_page_id = row['lastest_anno_page_id']
    
    
    db_api.close(cursor)
    return theme_user_anno_article_count, lastest_anno_page_id



def get_remarked_news_id_list(theme_name, version_id, user_name):
    """
    @Param str: theme's name;
    @Param str: version id
    @Param str: user name
    @Return list[str]
    """
    print("get_remarked_news_id_list")
    get_article_remarked_sql = "select distinct NewsID as news_id from theme_news_anno where ThemeName = '%s' and ThemeVersionID = '%s' and UserName = '%s'"
    cursor, conn = db_api.conn()
    db_api.query(cursor, get_article_remarked_sql % (theme_name, version_id, user_name))
    row = db_api.fetch_one_row(cursor)
    remarked_article_list = []
    while row != None:
        news_id = row['news_id']
        remarked_article_list.append(news_id)

        row = db_api.fetch_one_row(cursor)

    db_api.close(cursor)
    print("after get_remarked_news_id_list")
    return remarked_article_list


def get_if_news_remarked(theme_name, user_name, news_id):
    """
    get if a news have been annotated by the user;
    @Param str: theme name
    @Param str: user name
    @Param str: NewsID
    """
    print("get_if_news_remarked")
    get_if_news_remarked_sql = "select * from theme_news_anno where ThemeName = '%s' and UserName = '%s' and NewsID = '%s'"
    cursor, conn = db_api.conn()
    db_api.query(cursor, get_if_news_remarked_sql % (theme_name, user_name, news_id))
    row = db_api.fetch_one_row(cursor)

    db_api.close(cursor)
    if row != None:
        return True
    else:
        return False


def insert_article_anno_into_db(theme_name, version_id, news_id, news_page_id, user_name, anno_correlation, anno_add_words, anno_del_words, anno_comment):
    """
    insert article annotation data into database
    @Param str theme_name
    @Param str version_id
    @Param str news_id (eg.IP_3125434)
    @Param int news_page_id
    @Param str anno_corr('Strong', 'Weak', 'Not')
    @Param str anno_added_key_words
    @Param str anno_delete_key_words
    @Param str comment
    @Return str status code
    """
    insert_article_anno_sql = "insert into theme_news_anno (ThemeName, ThemeVersionID, NewsID, NewsPageID, UserName, AnnoCorr, AnnoAdd, AnnoDel, AnnoComment) values ('%s', '%s', '%s', %d, '%s', '%s', '%s', '%s', '%s')"
    try:
        cursor, conn = db_api.conn()
        db_api.insert(cursor, conn, insert_article_anno_sql % (theme_name, version_id, news_id, news_page_id, user_name, anno_correlation, anno_add_words, anno_del_words, anno_comment))
        db_api.close(cursor)
        return "Success"
    except Exception as e:
        print(e)
        return "False"

