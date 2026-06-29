from django.urls import path
from . import views

urlpatterns = [
    path("topics/", views.topic_root_list),
    path("topic/<slug:slug>/", views.topic_detail),
    path("topic/<slug:slug>/chat/", views.topic_chat),
    path("topic/<slug:slug>/quiz/", views.topic_quiz),
    path("topic/<slug:slug>/quiz/submit/", views.topic_quiz_submit),
    path("topic/<slug:slug>/bookmark/", views.topic_bookmark),
    path("topic/<slug:slug>/progress/", views.topic_progress),
    path("profile/weaknesses/", views.profile_weaknesses),
]