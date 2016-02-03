from django.conf.urls import url
from . import views

app_name = 'ThemesAnnoSys'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^outline$', views.outline, name="outline"), 
    url(r'^ArticleAnno/(?P<theme_name>[a-zA-Z0-9_\u4e00-\u9fa5]+)/(?P<version_id>[\.0-9]+)/(?P<page_id>[0-9]+)$', views.article_anno, name="article_anno"),
    url(r'^search/(?P<theme_name>[a-zA-Z0-9_\u4e00-\u9fa5]+)/(?P<version_id>[\.0-9]+)/(?P<key_word>[a-zA-Z0-9_\u4e00-\u9fa5]+)/(?P<page_id>[0-9]+)$', views.search_text, name="search_by_word"),
    url(r'keywords/(?P<theme_name>[a-zA-Z0-9_\u4e00-\u9fa5]+)/(?P<version_id>[\.0-9]+)$', views.theme_keywords, name="theme_keywords"),
]
