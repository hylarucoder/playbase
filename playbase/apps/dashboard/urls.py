from django.urls import path

from playbase.apps.dashboard.views import page_text, page_home, page_cards, page_music, page_auth, \
    page_form, page_mail, page_tasks, page_playground, page_chat

urlpatterns = [
    path("", page_home, name="dashboard_home"),
    path("bill", page_text, name="dashboard_bill"),
    path("projects", page_text, name="dashboard_projects"),
    path("orders", page_text, name="dashboard_orders"),
    path("analytics", page_text, name="dashboard_analytics"),
    path("settings", page_text, name="dashboard_settings"),
    path("profile", page_text, name="dashboard_profile"),
    path("chat", page_chat, name="dashboard_chat"),
    # path("image", page_image, name="image_view"),
    # path("text", page_text, name="text"),
    path("login", page_auth, name="login"),
    path("cards", page_cards, name="dashboard_cards"),
    path("form", page_form, name="dashboard_form"),
    path("mail", page_mail, name="dashboard_mail"),
    path("music", page_music, name="dashboard_music"),
    path("tasks", page_tasks, name="dashboard_tasks"),
    path("playground", page_playground, name="dashboard_playground"),
]
