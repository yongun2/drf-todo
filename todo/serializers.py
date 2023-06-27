from rest_framework import serializers

from todo.models import Todo


class TodoCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("id", "title", "complete", "important")


class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "id",
            "title",
            "descripttion",
            "created",
            "complete",
            "important",
        )


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "title",
            "descripttion",
            "important",
        )
