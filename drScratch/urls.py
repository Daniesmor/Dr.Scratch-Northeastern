# from django.conf.urls import *
# from django.conf.urls import url, include
from django.urls import re_path as url
from django.urls import include, path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.generic import RedirectView
from app import views as app_views
from django.conf.urls.static import static
from django.views.static import serve
admin.autodiscover()


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),

    # Statics
    # url(r'^/v3/static/(?P<path>.*)$' , serve,
    #                              {'document_root': settings.MEDIA_ROOT}),
    url(r'^(.*)/static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # BABIA PROJECTS
    url(r'^get_babia/$', app_views.get_babia, name='get_babia'),
    
    # API ANALYSIS
    url(r'^get_analysis_d/(?P<skill_points>.{1,6})?$', app_views.get_analysis_d, name='get_analysis_d'),

    # API RECOMMENDER
    url(r'^get_recommender/.*$', app_views.get_recommender, name='get_recommender'),
    
    
    # CONTACT FORM
    url(r'^process_contact_form/$', app_views.process_contact_form, name='contact_form'),


    # CSVS (BATCH)
    url(r'^(.*)/csvs/(?P<path>.*)$',serve, {'document_root': settings.BASE_DIR + '/csvs'}),

    # BATCH RAW html -> str
    #url(r'^batch/raw/(?P<csv_identifier>[-\w]+)$', app_views.batch_email, name='batch_raw'),
    # BATCH)
    url(r'^batch/(?P<csv_identifier>.*)$',app_views.batch, name='batch'),
    
    # Statistics
    url(r'^statistics$', app_views.statistics, name='statistics'),

    # Collaborators
    url(r'^collaborators$', app_views.collaborators, name='collaborators'),

    # Contest: Temporary url
    url(r'^contest$', app_views.contest, name='contest'),

    # Blog
    url(r'^blog$', 
        RedirectView.as_view(url='https://drscratchblog.wordpress.com')),
    
    # Rubric personalized
    url(r'^rubric_creator/students', app_views.rubric_creator_students, name='rubric_creator'),
    url(r'^rubric_creator/teachers', app_views.rubric_creator_teachers, name='rubric_creator'),
    url(r'^rubric_creator', app_views.rubric_creator, name='rubric_creator'),
    url(r'^(?P<skill_points>.{1,6})$', app_views.upload_personalized, name='upload_personalized'),

    # C_Mode
    url(r'^compare_uploader', app_views.compare_uploader, name='compare_uploader'),
        
    # Dashboards
    url(r'^show_dashboard/(?P<skill_points>.{1,6})?$', app_views.show_dashboard, name='show_dashboard'),
    url(r'^download_certificate', app_views.download_certificate, name='certificate'),

    # Conact form
    url(r'^contact', app_views.contact, name='contact'),

    # Translation
    url(r'^i18n/', include('django.conf.urls.i18n'), name="translation"),
    url(r'^blocks$', app_views.blocks, name='blocks'),
    url(r'^blocks_v3/$', app_views.blocks_v3, name='blocks_v3'),

    # Organizations
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        app_views.reset_password_confirm, name='reset_password_confirm'),
    url(r'^change_pwd$', app_views.change_pwd, name='change_pwd'),
    # url(r'^organization_hash', 'app.views.organization_hash',),
    url(r'^sign_up_organization$', app_views.sign_up_organization, name='sign_up_organizations'),
    url(r'^organization/stats/(\w+)', app_views.stats, name='organization_stats'),
    url(r'^organization/downloads/(.*)', app_views.downloads, name='organization_downloads'),
    #url(r'^organization/settings/(\w+)', app_views.account_settings, name='organization_settings'),
    url(r'^organization/(.*)', app_views.organization, name='organization'),
    url(r'^login_organization$', app_views.login_organization, name='organization_login'),
    url(r'^logout_organization$', app_views.logout_organization, name='organization_logout'),

    # Coders
    url(r'^coder_hash', app_views.coder_hash, name='coder_hash'),
    url(r'^sign_up_coder$', app_views.sign_up_coder, name='sign_up_coder'),
    url(r'^coder/stats/(\w+)', app_views.stats, name='coder_stats'),
    url(r'^coder/downloads/(.*)', app_views.downloads, name='coder_downloads'),
    #url(r'^coder/settings/(\w+)', app_views.account_settings, name='coder_settings'),
    url(r'^coder/(.*)', app_views.coder, name='coder'),
    url(r'^login_coder$', app_views.login_coder, name='coder_login'),
    url(r'^logout_coder$', app_views.logout_coder, name='coder_logout'),
    
    # Upload a .CSV
    url(r'^analyze_CSV$', app_views.analyze_csv, name='csv'),

    # Plugins
    url(r'^plugin/(.*)', app_views.plugin, name='plugin'),

    # Discuss
    url(r'^discuss$', app_views.discuss, name='discuss'),

    # Ajax
    url(r'search_email/$', app_views.search_email, name='search_email'),
    url(r'search_username/$', app_views.search_username, name='search_username'),
    url(r'search_hashkey/$', app_views.search_hashkey, name='search_hashkey'),

    # Error pages
    #url(r'^500', 'app.views.error500',),
    #url(r'^404', 'app.views.error404',),

    # Learn
    url(r'^learn/(Modes|Dimensions|BadSmells)/(\w+)', app_views.learn, name='learn'),
    url(r'^$', app_views.main, name='main'),
    url(r'^documents/(?P<filename>[\w\-\.]+\.pdf)$', app_views.serve_document_pdf, name='serve_document_pdf'),
    #url(r'^.*', app_views.redirect_main, name='redirect_main'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
