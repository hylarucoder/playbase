from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, path
from django.views import defaults as default_views
from django.views.generic import RedirectView

from components.greeting import Greeting
from components.nested.vcalendar.vcalendar import CalendarNested
from components.todo.todo import Calendar
from components.vcalendar.vcalendar import CalendarRelative
from playbase.apps.home.views import home_page
from playbase.apps.user.urls import urlpatterns as user_urlpatterns

favicon_view = RedirectView.as_view(url="/static/favicon.ico", permanent=True)

urlpatterns = (
        [
            path("", home_page, ),
            path("api/", include(user_urlpatterns)),
            path("favicon.ico", favicon_view),
            path(settings.ADMIN_URL, admin.site.urls),
            path("greeting/", Greeting.as_view(), name="greeting"),
            path("calendar/", Calendar.as_view(), name="calendar"),
            path("calendar-relative/", CalendarRelative.as_view(), name="calendar-relative"),
            path("calendar-nested/", CalendarNested.as_view(), name="calendar-nested"),
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
