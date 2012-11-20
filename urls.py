from django.conf.urls import patterns, include, url

# (?P<year>\d{4})
urlpatterns = patterns( 'classifieds',
    url( r'^add/$', 'views.add', name = 'classifieds-add' ),
    url( r'^edit/(?P<id>\d+)$', 'views.edit', name = 'classifieds-edit' ),
    url( r'^category-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?', 'views.category', name = 'classifieds-category' ),
    url( r'^post-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?', 'views.post', name = 'classifieds-post' ),
    url( r'^ajax/image-upload/$', 'ajax.image_upload', name = 'classifieds-ajax-image-upload' ),
    url( r'^(?:/?page-(?P<page>\d+))?', 'views.home', name = 'classifieds-home' ),
 )

