from django.contrib import admin

from mipha.models.blog import BlogCategory, BlogTag, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass
