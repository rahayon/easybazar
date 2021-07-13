from django.contrib import admin
from .models import PostCategory, Post
from mptt.admin import DraggableMPTTAdmin
from django_summernote.admin import SummernoteModelAdmin


class PostCategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_posts_count', 'related_posts_cumulative_count')
    list_display_links = ('indented_title',)
    #list_display = ['name', 'description', 'is_active'] 
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = PostCategory.objects.add_related_count(
                qs,
                Post,
                'category',
                'posts_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = PostCategory.objects.add_related_count(qs,
                 Post,
                 'category',
                 'posts_count',
                 cumulative=False)
        return qs

    def related_posts_count(self, instance):
        return instance.posts_count

    related_posts_count.short_description = 'Related posts (for this specific category)'

    def related_posts_cumulative_count(self, instance):
        return instance.posts_cumulative_count

    related_posts_cumulative_count.short_description = 'Related posts (in tree)'
    
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description', 'is_active'] 
#     prepopulated_fields = {'slug': ('name',)}



class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'author', 'category', 'status','created_at']
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['created_at']
    search_fields = ['title','content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
