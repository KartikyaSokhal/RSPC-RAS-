from django.urls import path
from . import views
from .permissions import unavailable_learner_view

# Fixed content-first release boundary, independent of authentication or settings.
# Historical handlers/models remain available for a separately approved release.
learner_unavailable = unavailable_learner_view(['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'])

urlpatterns = [
    path("health/", views.health),
    path("config/", views.configuration),
    path("search/", views.search_results),
    path("tags/<str:slug>/", views.tag_discovery),
    path("topic/<slug:slug>/context/", views.topic_context),
    path("topic/<slug:slug>/practice/", views.practice_collection),
    path("topic/<slug:slug>/practice/check/", views.practice_collection_check),
    path("resources/<int:resource_id>/", views.resource_detail),
    path("resources/<int:resource_id>/file/", views.resource_file),
    path("topic/<slug:slug>/images/<int:block_id>/", views.topic_image),
    path("topic/<slug:slug>/quiz/check/", views.topic_quiz_check),
    path("topics/", views.topic_root_list),
    path("topic/<slug:slug>/", views.topic_detail),
    path("topic/<slug:slug>/chat/", views.topic_chat),
    path("topic/<slug:slug>/quiz/", views.topic_quiz),
    path("topic/<slug:slug>/quiz/submit/", learner_unavailable),
    path("topic/<slug:slug>/bookmark/", learner_unavailable),
    path("topic/<slug:slug>/progress/", learner_unavailable),
    path("profile/weaknesses/", learner_unavailable),
    path("auth/register/", learner_unavailable),
    path("auth/login/", learner_unavailable),
    path("auth/logout/", learner_unavailable),
    path("auth/status/", learner_unavailable),
    path("dashboard/", learner_unavailable),
    path("bookmarks/", learner_unavailable),
    path("progress/", learner_unavailable),
]

