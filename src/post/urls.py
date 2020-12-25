from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path("filter/", CategoriesPostFilterView.as_view(), name='filter'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail_page'),
    path('edit_page/', EditPageView.as_view(), name='edit_page'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('update/<int:pk>', ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete'),
    path('like/', LikeView.as_view(), name='like-post'),
    path('author_article/', AuthorArticleView.as_view(), name='get_author_article'),
]
