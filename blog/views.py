from typing import Any
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentaryForm
from .models import Post


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("owner").order_by(
        "-created_time"
    )

    paginator = Paginator(posts, 5)
    page_number: str | None = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context: dict[str, Any] = {
        "post_list": page_obj.object_list,
        "page_obj": page_obj,
    }

    return render(request, "blog/index.html", context)


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentaryForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.user = request.user
            commentary.post = post
            commentary.save()
            return redirect("blog:post-detail", pk=pk)
    else:
        form = CommentaryForm()

    context: dict[str, Any] = {
        "post": post,
        "comments": post.comments.all(),
        "form": form,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )
