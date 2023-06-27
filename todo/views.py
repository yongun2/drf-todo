from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.models import Todo
from todo.serializers import (
    TodoCompactSerializer,
    TodoCreateSerializer,
    TodoDetailSerializer,
)


# 리스트, 생성 뷰
class TodoAPIView(APIView):
    def get(self, request):
        """
        현재까지 작성된 모든 Todo를 description은 제외하고 조회한다.

        Args:
            none

        Params:
            complete (boolean) : Todo 완료 여부, 해당 조건에 따른 Todo list 조회
            값이 넘어오지 않을 경우 모든 Todo 리스트 반환


        Raised:
            KeyError: 쿼리 파라미터로 boolean 값이 아닌 다른 값이 넘어올 경우 400 반환

        Returns:
            Todo : {
                id,
                title,
                important,
                created
            }

        """

        # complete 쿼리 파라미터 미포함일 경우 default는 False
        if not "complete" in request.GET:
            todos = Todo.objects.all()
        else:
            complete = request.GET["complete"]
            # 쿼리 파라미터의 값이 true 혹인 false인 경우 True, False로 변환
            boolParser = {"true": True, "false": False}
            try:
                complete = boolParser[complete]
                todos = Todo.objects.filter(complete=complete)
            except KeyError:
                # complete 파라미터로 true 혹은 false 값이 아닌 잘못된 값이 넘어왔을 경우 400 반환
                return Response(
                    data={"message": "잘못된 쿼리 파라미터"}, status=status.HTTP_400_BAD_REQUEST
                )

        serializer = TodoCompactSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        새로운 todo를 생성한다.

        Args:
            request.data (json): {
                title,
                descripttion,
                important
            }

        Returns:
            Todo : {
                id,
                title,
                important,
                created
            }
        """
        serializer = TodoCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 단일 조회, 수정, 삭제 뷰
class TodoDetailAPIView(APIView):
    def get(self, request, pk: int):
        """
        pk에 해당하는 todo의 모든 정보를 조회한다.

        Args:
            pk (int): todo를 식별하는 고유 키 값

        Raises:
            pk를 만족하는 데이터가 없을 경우 404 반환

        Returns:
            Todo : {
                id,
                title,
                descripttion,
                important,
                created
            }
        """
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int):
        """
        pk에 해당하는 todo의 내용을 수정한다. request로 title, descripttion은 반드시 포함 되어야 한다.
        important는 필수는 아니다.

        Args:
            request.data (json): {
                title,
                descripttion,
                important
            }
            pk (int): todo를 식별하는 고유 키 값

        Returns:
            Todo : {
                id,
                title,
                descripttion,
                important,
                created
            }
        """
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoCreateSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int):
        """
        pk에 해당하는 todo를 삭제한다.

        Args:
            pk (int): todo를 식별하는 고유 키 값

        Raises:
            pk에 해당하는 todo가 없을 경우 404 반환

        Returns:
            Todo : {
                id,
                title,
                descripttion,
                important,
                created
            }
        """
        todo = get_object_or_404(Todo, id=pk)
        serializer = TodoDetailSerializer(todo)
        todo.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
