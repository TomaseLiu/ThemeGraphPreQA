import os
import sys                                                                                            
import inspect                                                                                        

from django.core.paginator import Paginator
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))                                                                                                                                                                                                         
module_dirs = ["entity", "business"]                                                                  

for module_dir in module_dirs:
    sys.path.append(os.path.join(SCRIPT_DIR, module_dir))

theme_data_dir = os.path.join(SCRIPT_DIR, "../data/themes")

import file_tools
import db_tools


def get_theme_keywords(theme_name, version_id, user_name):

    theme_desc = file_tools.read_theme_desc_from_file(theme_data_dir, theme_name, version_id)
    keywords_dict = file_tools.get_theme_keywords(theme_data_dir, theme_name, version_id, user_name)
    keywords_text_dict = {}
    for source in keywords_dict:
        keywords_text_dict[source] = []
        for keyword_str in keywords_dict[source]:
            if keywords_dict[source][keyword_str] == "-1":
                keywords_text_dict[source].append('<del>' + keyword_str + '</del>')
            elif keywords_dict[source][keyword_str] == "1":
                keywords_text_dict[source].append('<add>' + keyword_str + '</add>')
            else:
                keywords_text_dict[source].append(keyword_str)

    keywords_zheshang_text = ""
    keywords_research_text = ""
    keywords_news_text = ""

    if "zheshang" in keywords_dict:
        keywords_zheshang_text = '\n'.join(keywords_text_dict["zheshang"])
    if "research" in keywords_dict:
        keywords_research_text = '\n'.join(keywords_text_dict["research"])
    if "news" in keywords_dict:
        keywords_news_text = '\n'.join(keywords_text_dict["news"])
    return keywords_zheshang_text, keywords_research_text, keywords_news_text, theme_desc


def submit_keywords_modifing(request, theme_name, version_id, user_name):
    if request.method != 'POST':
        return
    #print(request.POST.keys())
    keywords_source = request.POST['keywords_source']
    keywords_text = request.POST['keywords_text']
    keywords_text = keywords_text.replace('del', '').replace('add', '').replace('</', '').replace('<', '').replace('>', '')
    submit_keywords_set = set(keyword_str.strip() for keyword_str in keywords_text.split('\n'))
    file_tools.write_keywords_modifing_into_file(theme_data_dir, theme_name, version_id, user_name, submit_keywords_set, keywords_source)


