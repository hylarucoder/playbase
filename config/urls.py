from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.urls import re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView
from django.views.generic import TemplateView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
                  # url for index
                  re_path(r'^$', TemplateView.as_view(template_name="index.html")),
                  re_path(r'^api/', include('yaapi.urls')),
                  re_path(r'^favicon\.ico$', favicon_view),
                  re_path(settings.ADMIN_URL, admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception("Bad Request!")}),
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        re_path(r'^500/$', default_views.server_error),
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
