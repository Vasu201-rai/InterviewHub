from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('add-question/', views.add_question, name='add_question'),
    
    path('edit-question/<int:id>/',views.edit_question,name='edit_question'),
    
    path('delete-question/<int:id>/',views.delete_question,name='delete_question'),
    
    path('bookmark/<int:id>/',views.toggle_bookmark,name='toggle_bookmark'),
    
    path('bookmarks/',views.bookmarked_questions,name='bookmarks'),
    
    path('question/<int:id>/',views.question_detail,name='question_detail'),
    
]