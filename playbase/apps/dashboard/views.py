import datetime

import requests
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from playbase.apps.home.views import HtmxHttpRequest
from playbase.models import MockTask, Message

menus = [
    {"name": "Dashboard", "view_name": "dashboard_home", "icon": "dashboard"},
    {"name": "Orders", "view_name": "dashboard_orders", "icon": "order", "count": 5},
    {"name": "Projects", "view_name": "dashboard_projects", "icon": "projects"},
    {"name": "Bill", "view_name": "dashboard_bill", "icon": "bill"},
    {"name": "Analytics", "view_name": "dashboard_analytics", "icon": "analytics"},
    {"name": "Chat", "view_name": "dashboard_chat", "icon": "analytics"},
    {"name": "Settings", "view_name": "dashboard_settings", "icon": "analytics"},
    {"name": "Profile", "view_name": "dashboard_profile", "icon": "analytics"},
    # {"name": "Image", "view_name": "image_view", "icon": "image"},
    # {"name": "Text", "view_name": "text", "icon": "text"},
    # {"name": "Login", "view_name": "login", "icon": "analytics"},
    {"name": "Cards", "view_name": "dashboard_cards", "icon": "analytics"},
    {"name": "Form", "view_name": "dashboard_form", "icon": "analytics"},
    {"name": "Mail", "view_name": "dashboard_mail", "icon": "analytics"},
    {"name": "Music", "view_name": "dashboard_music", "icon": "analytics"},
    {"name": "Tasks", "view_name": "dashboard_tasks", "icon": "analytics"},
    {"name": "Playground", "view_name": "dashboard_playground", "icon": "analytics"},

]


@require_GET
def page_home(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/index.html",
        {
            "title": "Dashboard",
            "menus": menus,
        },
    )


@require_GET
def page_image(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/image.html",
        {
            "title": "image",
            "menus": menus,
        },
    )


@require_GET
def page_text(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/text.html",
        {"title": "about", "menus": menus},
    )


@require_GET
def page_bill(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/text.html",
        {"title": "Bill", "menus": menus, },
    )


@require_GET
def page_tasks(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/text.html",
        {"title": "about", "menus": menus, },
    )


@require_GET
def page_cards(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/text.html",
        {"title": "about", "menus": menus, },
    )


@require_GET
def page_playground(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/playground.html",
        {"title": "about", "menus": menus, },
    )


@require_GET
def page_settings(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/text.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_auth(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/auth.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_cards(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/cards.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_form(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/form.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_mail(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/mail.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_music(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/dashboard/music.html",
        {"title": "about", "menus": menus, "now": datetime.datetime.now()},
    )


@require_GET
def page_tasks(request: HtmxHttpRequest) -> HttpResponse:
    qs = MockTask.objects.all().order_by("id")
    page = request.GET.get("page", 1)
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)
    if request.htmx:
        template_name = "pages/dashboard/tasks_partial.html"
    else:
        template_name = "pages/dashboard/tasks.html"

    return render(
        request,
        template_name,
        {
            "title": "Tasks",
            "page_obj": page_obj,
            "menus": menus,
        },
    )


def get_ai_response(user_input: str) -> str:
    endpoint = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": "Bearer pplx-",
        "Content-Type": "application/json",
    }

    messages = get_existing_messages()
    messages.append({"role": "user", "content": f"{user_input}"})
    data = {"model": "mistral-7b-instruct", "messages": messages, "temperature": 0.7}
    response = requests.post(endpoint, headers=headers, json=data)
    print(f"{response.text=}")
    response_data = response.json()
    print(f"{response_data = }")
    ai_message = response_data["choices"][0]["message"]["content"]
    return ai_message


def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API.
    """
    formatted_messages = []

    for message in Message.objects.values("user_message", "bot_message"):
        formatted_messages.append({"role": "user", "content": message["user_message"]})
        formatted_messages.append(
            {"role": "assistant", "content": message["bot_message"]}
        )

    return formatted_messages


def page_chat(request: HtmxHttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_message = get_ai_response(user_message)
        Message.objects.create(user_message=user_message, bot_message=bot_message)
        messages = Message.objects.all()
        return render(request, "pages/dashboard/chat_partial.html", {"messages": messages})
    messages = Message.objects.all()
    return render(request, "pages/dashboard/chat.html", {"messages": messages, "menus": menus, })
