from django.shortcuts import get_object_or_404

from Quizy.quizzes.models import Question


def is_superuser(user):
    return user.is_superuser


def is_staff(user):
    return user.is_staff or user.is_superuser


def is_anonymous(user):
    return not user.is_authenticated


def is_authenticated(user):
    return user.is_authenticated


def is_staff_or_creator_question(user, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return user.is_staff or user == question.user
