import datetime

import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django_htmx.middleware import HtmxDetails

from playbase.models import Message


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def format_seconds(sec: int) -> str:
    minutes = sec // 60
    return f"{minutes}min"


posts = [
    {
        "title": f"{i} -- Guide: Workflow for Creating Animations using animatediff-cli-prompt-travel Step-by-Step",
        "date": "2023-08-15",
        "href": f"/p/mj-geometry-composition-{i}",
        "category": "midjourney",
        "views": i + 10,
        "read_min": format_seconds(169 + 60 * i),
        "tags": [
            "stable diffusion",
            "sd",
            "animation",
            "animatediff-cli-prompt-travel",
        ],
        "summary": "This guide will walk you through the process of creating animations using the animatediff-cli-prompt-travel tool. It's a step-by-step guide that will help you get started with creating animations using the tool.",
        "cover": "https://image.simpleaiart.com/content/images/2023/09/007.webp",
    }
    for i in range(10)
]


@require_GET
def home_page(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/index.html",
        {"title": "J", "posts": posts, "now": datetime.datetime.now()},
    )


@require_GET
async def login(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request,
        "pages/login.html",
        {"title": "All Posts", "posts": posts, "now": datetime.datetime.now()},
    )


@require_GET
async def page_post(request: HtmxHttpRequest, slug) -> HttpResponse:
    return render(
        request,
        "p.html",
        {"title": posts[0]["title"], "post": posts[0], "now": datetime.datetime.now()},
    )
