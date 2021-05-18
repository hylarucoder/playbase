from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path
from django.views import defaults as default_views
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from mipha.apps.user.urls import urlpatterns as user_urlpatterns

favicon_view = RedirectView.as_view(url="/static/favicon.ico", permanent=True)

urlpatterns = (
        [
            path("", TemplateView.as_view(template_name="index.html")),
            path("api/", include(user_urlpatterns)),
            path("favicon.ico", favicon_view),
            path(settings.ADMIN_URL, admin.site.urls),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        re_path(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        re_path(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        re_path(r"^500/$", default_views.server_error),
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
