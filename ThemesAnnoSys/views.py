from django.shortcuts import render, render_to_response
from django.template import RequestContext
import sys
import inspect 
import os 
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
local_module_dirs = ["entity", "business"]

for module_dir in local_module_dirs:
    sys.path.append(os.path.join(SCRIPT_DIR, module_dir))

themes_data_dir = os.path.join(SCRIPT_DIR, "data/themes")

# Create your views here.

import Theme
import file_tools
import db_tools
import content_page_business 
import article_anno_business
import search_page_business
import keywords_page_business
def index(request):
    theme_obj_list = file_tools.get_theme_obj_list(themes_data_dir)
    print(theme_obj_list)
    return render(request, 'ThemesAnnoSys/index.html')

@login_required
def outline(request):
    user = request.user
    
    print(user.groups.all())
    if request.method == 'GET':
        try:
            theme_info_list = content_page_business.get_theme_user_anno_info_obj_list(user)
            return render_to_response('ThemesAnnoSys/theme_list.html', locals(), context_instance=RequestContext(request))
        except Exception as e:
            print(e)
            raise Http404

    else:
        try:
            theme_name = request.POST['theme_name']
            key_word = request.POST['key_word']
            version_id = request.POST['version_id']
            return HttpResponseRedirect(reverse('ThemesAnnoSys:search_by_word', args=(theme_name, version_id, key_word, 1)))
        except Exception as e:
            print(e)
            return HttpResponse("error")

@login_required
def article_anno(request, theme_name, version_id, page_id):
    try:
        if int(page_id) <= 0:
            raise Http404
    except Exception as e:
        raise Http404

    user_name = request.user
    if request.method == 'GET':
        try:
            paginator_article_list, process_pencentage, next_unremarked_page_id, this_page_remarked = article_anno_business.get_data_of_article_anno_page(theme_name, version_id, user_name, page_id)
            if next_unremarked_page_id == '0': next_unremarked_page_id = '1'
            return render_to_response('ThemesAnnoSys/detail_task.html', locals(), context_instance=RequestContext(request))    
        except Exception as e:
            raise Http404

    if request.method == 'POST':
        try:
            insert_status = article_anno_business.post_article_anno_data(request, theme_name, version_id, int(page_id), user_name)
            page_id = str(int(page_id) + 1)
            if "Success" == insert_status:
                messages.add_message(request, messages.SUCCESS, '提交成功')
            else:
                messages.add_message(request, messages.ERROR, '提交失败')
            return HttpResponseRedirect(reverse('ThemesAnnoSys:article_anno', args=(theme_name, version_id, page_id)))
        except Exception as e:
            print(e)
            raise Http404
    

@login_required
def search_text(request, theme_name, version_id, key_word, page_id):
    paginator_article_list, theme_article_count, article_search_result_count = search_page_business.search_article_by_key_word(theme_name, version_id, key_word, page_id)
    return render_to_response('ThemesAnnoSys/search_page.html', locals(), context_instance=RequestContext(request))


@login_required
def theme_keywords(request, theme_name, version_id):
    user_name = request.user
    user_name = str(user_name)
    print(user_name)
    if request.method == 'GET':
        keywords_zheshang, keywords_research, keywords_news, theme_desc = keywords_page_business.get_theme_keywords(theme_name, version_id, user_name)

        keywords_list = [keywords_zheshang, keywords_research, keywords_news]
        return render_to_response('ThemesAnnoSys/keywords_page.html', locals(), context_instance=RequestContext(request))

    if request.method == 'POST':
        keywords_page_business.submit_keywords_modifing(request, theme_name, version_id, user_name)
        return HttpResponseRedirect(reverse('ThemesAnnoSys:theme_keywords', args=(theme_name, version_id)))


