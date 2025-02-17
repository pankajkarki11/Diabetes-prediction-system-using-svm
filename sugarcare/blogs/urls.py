from django.urls import path
from . import views
from . views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView


    #path('', views.home, name="bloghome"),
urlpatterns = [
    path('', PostListView.as_view(), name="bloghome"),  # Root URL
    path('about/', views.about, name="blogabout"),
    path('post/new', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('contact/', views.contact, name="contact"),
    path('pretest/test/', views.test, name="test"),
    path('pretest/', views.pretest,name='pretest'),
    path('pretest/test/result', views.result),
    path('explore/', views.explore, name="explore"),
    path('meds/', views.meds, name="meds"),
    path('consult/', views.consult, name="consult"),
    path('post/<int:pk>/addcomment', CommentCreateView.as_view(), name="addcomment"),
    path('exercise/', views.exercises, name="exercise"),
]

