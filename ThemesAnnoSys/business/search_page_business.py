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

def search_article_by_key_word(theme_name, version_id, key_word, page_id):
    try:
        news_id2index_dict, news_obj_list = file_tools.get_news_id2index_dict_and_obj_list(themes_data_dir, theme_name, version_id)
        
        ori_tag_list = ["highlight_zheshang", "highlight_comm", "highlight_resh", "highlight_comp"]
        hit_word_tag = "<highlight_red>" + key_word + "</highlight_red>"

        key_word_tag_list = ['<' + ori_tag_list[i] + '>' + key_word + '</' + ori_tag_list[i] + '>' for i in range(0, len(ori_tag_list))]

        theme_article_count = len(news_obj_list)
        news_obj_filtered_list = []
        for article in news_obj_list:

            if key_word != "all":
                hit = False
                for key_word_tag in key_word_tag_list: 
                    hit = (hit or (key_word_tag in article.body))
                if not hit: 
                    continue

            #print(article.body)
            for key_word_tag in key_word_tag_list:
                article.body = article.body.replace(key_word_tag, hit_word_tag)
            news_obj_filtered_list.append(article)

        article_search_result_count = len(news_obj_filtered_list)
        limit = 10
        paginator = Paginator(news_obj_filtered_list, limit)
        page_id = page_id
        paginator_article_list = paginator.page(page_id)
        return paginator_article_list, theme_article_count, article_search_result_count
    except Exception as e:
        print(e)
        return None
            

