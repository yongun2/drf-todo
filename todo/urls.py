from django.urls import path

from todo.views import TodoAPIView, TodoDetailAPIView


urlpatterns = [
    # 리스트 조회, 생성
    path("", TodoAPIView.as_view()),
    # 단일 조회, 수정, 삭제
    path("<int:pk>/", TodoDetailAPIView.as_view()),
]
