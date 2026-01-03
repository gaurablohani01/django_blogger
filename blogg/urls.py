from django.urls import path
from blogg import views
urlpatterns = [
    path('home/', views.home_page, name="home"),
    path('create/', views.create_blog, name='createblog'),
    path('update/<int:id>/', views.update_blog, name="updateblog"),
    path('delete/<int:id>/', views.delete_blog, name="deleteblog")

]
