import os
import sys
import inspect

from django.core.paginator import Paginator

SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))

module_dirs = ["entity", "business"]

for module_dir in module_dirs:
    sys.path.append(os.path.join(SCRIPT_DIR, module_dir))

themes_data_dir = os.path.join(SCRIPT_DIR, "../data/themes")

import Article
import file_tools
import db_tools

def get_news_obj_list_and_unremark_page_id(theme_name, version_id, user_name):

    news_id2index_dict, news_obj_list = file_tools.get_news_id2index_dict_and_obj_list(themes_data_dir, theme_name, version_id)

    remarked_news_id_set = set(db_tools.get_remarked_news_id_list(theme_name, version_id, user_name))

    ori_news_id_set = set(news_id2index_dict.keys())

    unremark_news_id_set = ori_news_id_set - remarked_news_id_set
    next_unremark_article_page_id = 0
    if len(unremark_news_id_set) != 0:
        next_unremark_article_page_id = min([news_id2index_dict[news_id] for news_id in unremark_news_id_set])

    return news_obj_list, next_unremark_article_page_id


def get_data_of_article_anno_page(theme_name, version_id, user_name, page_id):

    print("get_data_of_article_anno_page")
    try:
        news_obj_list, next_unremark_article_page_id = get_news_obj_list_and_unremark_page_id(theme_name, version_id, user_name)

        #print(news_obj_list)
        #print(next_unremark_article_page_id)
        limit = 1
        if int(page_id) > len(news_obj_list):
            return None
        paginator = Paginator(news_obj_list, limit)
        page = page_id
        paginator_article_list = paginator.page(page_id)
        process_pencentage = 100*(float(page_id)/float(paginator_article_list.paginator.num_pages))

        #print("after process_pencentage")

        if int(page_id) > len(news_obj_list) or int(page_id) < 1:
            return None

        news_id = news_obj_list[int(page_id)-1].news_id
        print(len(news_obj_list))
        this_page_remarked = db_tools.get_if_news_remarked(theme_name, user_name, news_id)
        
        return paginator_article_list, process_pencentage, str(next_unremark_article_page_id), this_page_remarked


    except Exception as e:
        print(e)
        return None



def post_article_anno_data(request, theme_name, version_id, news_page_id, user_name):
    if request.method != 'POST':
        return None
    try:
        selected_corr = request.POST['choice']
        good_words = request.POST['add_words']
        bad_words = request.POST['del_words']
        comment = request.POST['comment']
        news_id = request.POST['news_id']
        insert_status = db_tools.insert_article_anno_into_db(theme_name, version_id, news_id, news_page_id, user_name, selected_corr, good_words, bad_words, comment)
        return insert_status
    except Exception as e:
        print(e)
        return "False"


