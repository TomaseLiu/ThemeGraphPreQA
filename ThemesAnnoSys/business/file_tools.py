import os
import sys
import inspect
from time import gmtime, strftime
import json

SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
entity_module_dir = "entity"

sys.path.append(os.path.join(SCRIPT_DIR, entity_module_dir))

import Theme
import Article
import Keyword
"""
get data from file system
"""

news_folder = "news"
ORI_KEYWORD_FILE_NAME = "keywords.list"
KEYWORD_MODIFY_LOG_FOLDER_NAME = "keywords_modify_log"
THEME_DESC_FILE_NAME = "desc.txt"
def get_theme_id2name_dict(theme_data_folder_path):
    """
    get themes in file system
    @Param str: data folder which contains all themes' data
    @Return dict: theme_id to theme_name dict 
    """
    theme_list = os.listdir(theme_data_folder_path)
    theme_list = sorted(theme_list)
    theme_id2name_dict = {}
    theme_id = 0
    for theme_name in theme_list:
        theme_id += 1
        theme_id2name_dict[theme_id] = theme_name

    return theme_id2name_dict


def get_theme_versions(theme_data_folder_path, theme_name):
    """
    get theme's version list
    @Param str: theme data folder
    @Param str: theme's name
    @Return list: theme's version list
    @Return str:: theme's lastest version No.

    """
    if os.path.isdir(os.path.join(theme_data_folder_path, theme_name)):
        version_list = os.listdir(os.path.join(theme_data_folder_path, theme_name))
        version_list = sorted(version_list)
        lastest_version = '0.0'
        if len(version_list) != 0:
            lastest_version = version_list[-1]
        return version_list, lastest_version

    else:
        return None, '0.0'

def get_theme_news_count(theme_data_folder_path, theme_name, version_no):
    """
    get theme's news account;
    @Param str: theme data folder
    @Param str: theme's name
    @Return int: account of theme's news
    """
    if os.path.isdir(os.path.join(theme_data_folder_path, theme_name, version_no, news_folder)):
        news_count = len([news_file for news_root, news_dirs, news_files in os.walk(os.path.join(theme_data_folder_path, theme_name, version_no, news_folder)) for news_file in news_files])
        return news_count
    else:
        return 0

def get_article_obj_from_json_file(json_file_path):
    with open(json_file_path) as json_file_obj:
        json_data = json.load(json_file_obj)
        try:
            fname = json_file_path.split('/')[-1]
            fname_items = fname.split('_')
            #if len(fname_items) != 3:
            #    continue
            news_id = fname_items[0] + '_' + fname_items[1]
            index = fname_items[2]
            article_body = json_data['body']
            article_title = json_data['title']
            article_publish_time = json_data['publish_time'].split('T')[0]
            article_source = json_data['site_name']
            article_time_src = article_publish_time + '\t' + article_source
            

            """
            replace tags in article_body with tags we use in our html files
            """
            article_body = article_body.replace('zheshang>', 'highlight_zheshang>')
            article_body = article_body.replace('research>', 'highlight_resh>')
            article_body = article_body.replace('common>', 'highlight_comm>')
            article_body = article_body.replace('company>', 'highlight_comp>')

            article_obj = Article.Article(fname, news_id, article_title, article_time_src, article_body, index)
            return article_obj
        except Exception as e:
            print(e)
            return None


def get_news_id2index_dict_and_obj_list(theme_data_folder_path, theme_name, version_no):
    """
    get news file name list
    get news id ---> index dict
    @Param str: path to 'theme' folder;
    @Param str: theme's name
    @Param str: theme_version
    @Return dict[str--->int]
    @Return list[Article]
    """
    theme_news_folder_path = os.path.join(theme_data_folder_path, theme_name, version_no, news_folder)
    news_id2index_dict = {}
    article_obj_list = []
    if os.path.isdir(theme_news_folder_path):
        news_file_name_list = [news_file_name for news_root, news_dirs, news_files in os.walk(theme_news_folder_path) for news_file_name in news_files]
        for news_file_name in news_file_name_list:
            #print(news_file_name)
            try:
                news_file_path = os.path.join(theme_data_folder_path, theme_name, version_no, news_folder, news_file_name)
                #print(news_file_path)
                news_file_name_items = news_file_name.split('_')
                if len(news_file_name_items) != 3: continue

                article = get_article_obj_from_json_file(news_file_path)
                if article == None: 
                    continue
                article_obj_list.append(article)

                news_id = news_file_name_items[0] + "_" + news_file_name_items[1]
                news_index = news_file_name_items[2]
                news_id2index_dict[news_id] = int(news_index)
            except Exception as e:
                print(e)
    article_obj_list = sorted(article_obj_list)
    return news_id2index_dict, article_obj_list



def get_theme_obj_list(theme_data_folder_path):
    """
    get entity.theme.ThemeBasicInfo object list from file system
    """
    theme_id2name_dict = get_theme_id2name_dict(theme_data_folder_path)
    theme_obj_list = []
    for theme_id in theme_id2name_dict:
        theme_name = theme_id2name_dict[theme_id]
        version_list, lastest_version = get_theme_versions(theme_data_folder_path, theme_name)
        news_count = get_theme_news_count(theme_data_folder_path, theme_name, lastest_version)
        theme_index = theme_id
        theme = Theme.ThemeBasicInfo(theme_name, theme_id, theme_index, version_list, lastest_version, news_count)

        theme_obj_list.append(theme)
    return theme_obj_list
        


def get_theme_keywords_from_file(keywords_file_path):
    """
    read keywords group by source list from file (original_keywrods_file or modify_keywords_log_file)
    @Param str: keywords file path
    @Return dict[source ---> keyword ---> modify_status]
    """
    keywords_dict = {}
    if os.path.isfile(keywords_file_path):
        keywords_file_obj = open(keywords_file_path)
        for line in keywords_file_obj.readlines():
            items = line.strip().split(' ')
            if len(items) == 2:
                [word, source] = items
                modify_status = '0'
            elif len(items) == 3:
                [word, source, modify_status] = items
            else: continue

            #keyword = Keyword(word, source, modify_status)
            
            if source not in keywords_dict: keywords_dict[source] = {}
            keywords_dict[source][word] = modify_status
        keywords_file_obj.close()
    return keywords_dict


def get_theme_keywords(theme_data_folder_path, theme_name, version_id, user_name):
    """
    return keywords of a theme, together with current users' modifing records
    @Param str: folder path of 'themes'
    @Param str: theme's name
    @Param str: version id
    @Param str: current user's name
    @Return dict[keyword's type ---> keyword ---> modify_status]
    """
    keywords_file_path = ""
    original_keywords_file_path = os.path.join(theme_data_folder_path, theme_name, version_id, ORI_KEYWORD_FILE_NAME)
    if os.path.isfile(original_keywords_file_path):
        keywords_file_path = original_keywords_file_path

    user_keywords_modify_folder_path = os.path.join(theme_data_folder_path, theme_name, version_id, KEYWORD_MODIFY_LOG_FOLDER_NAME, user_name)
    if os.path.isdir(user_keywords_modify_folder_path):
        modify_log_file_list = [modify_file for root, dirs, files in os.walk(user_keywords_modify_folder_path) for modify_file in files]
        if len(modify_log_file_list) != 0:
            modify_log_file_list = sorted(modify_log_file_list)
            keywords_file_path = os.path.join(theme_data_folder_path, theme_name, version_id, KEYWORD_MODIFY_LOG_FOLDER_NAME, user_name, modify_log_file_list[-1])
            #keywords_file_path = modify_log_file_list[-1]

    keywords_dict = get_theme_keywords_from_file(keywords_file_path)

    return keywords_dict
            
        

def write_keywords_dict_into_file(keywords_dict, file_path):
    with open(file_path, 'w') as file_obj:
        for keyword_source in keywords_dict:
            for keyword_str in keywords_dict[keyword_source]:
                keyword_modify_status_code = keywords_dict[keyword_source][keyword_str]
                keyword_items = [keyword_str.strip(), keyword_source.strip(), str(keyword_modify_status_code)]
                line = ' '.join(keyword_items)
                file_obj.write(line + '\n')


def write_keywords_modifing_into_file(theme_data_folder_path, theme_name, version_id, user_name, submit_keywords_set, keywords_source):
    """
    write keywords modifing record into file
    """
    user_keywords_modify_log_folder_path = os.path.join(theme_data_folder_path, theme_name, version_id, KEYWORD_MODIFY_LOG_FOLDER_NAME, user_name)
    if not os.path.exists(user_keywords_modify_log_folder_path):
        os.makedirs(user_keywords_modify_log_folder_path)
    
    pre_keywords_dict = get_theme_keywords(theme_data_folder_path, theme_name, version_id, user_name)

    ori_keywords_file_path = os.path.join(theme_data_folder_path, theme_name, version_id, ORI_KEYWORD_FILE_NAME)
    ori_keywords_dict = get_theme_keywords_from_file(ori_keywords_file_path)

    current_keywords_dict = {}
    for source in pre_keywords_dict:
        if source == keywords_source: continue
        current_keywords_dict[source] = pre_keywords_dict[source]
    current_keywords_dict[keywords_source] = {}


    for keyword_str in submit_keywords_set:
        if keyword_str not in ori_keywords_dict[keywords_source]:
            current_keywords_dict[keywords_source][keyword_str] = '1'

    for keyword_str in ori_keywords_dict[keywords_source]:
        if keyword_str not in submit_keywords_set:
            current_keywords_dict[keywords_source][keyword_str] = '-1'
        else:
            current_keywords_dict[keywords_source][keyword_str] = '0'


    if keywords_source in pre_keywords_dict:
        for keyword_str in pre_keywords_dict[keywords_source]:
            if pre_keywords_dict[keywords_source][keyword_str] == '-1' and current_keywords_dict[keywords_source][keyword_str] == '0':
                current_keywords_dict[keywords_source][keyword_str] = '-1'


    time_now_str = strftime("%Y%m%d-%H%M%S", gmtime())
    
    keywords_modify_file_path = os.path.join(theme_data_folder_path, theme_name, version_id, KEYWORD_MODIFY_LOG_FOLDER_NAME, user_name, time_now_str)

    write_keywords_dict_into_file(current_keywords_dict, keywords_modify_file_path)

    

def read_theme_desc_from_file(theme_data_folder_path, theme_name, version_id):
    """
    read description for theme from file;
    """
    theme_desc = ""
    theme_desc_file_path = os.path.join(theme_data_folder_path, theme_name, version_id, THEME_DESC_FILE_NAME)
    if os.path.isfile(theme_desc_file_path):
        with open(theme_desc_file_path) as file_obj:
            theme_desc = file_obj.read()
    return theme_desc


