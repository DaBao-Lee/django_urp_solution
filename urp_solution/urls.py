from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('error/', error, name='error'),
    path('notallow/', notallow, name='notallow'),
    path('allowance/', allowance, name='allowance'),
    path('grades/', show_grade, name='show_grade'),
    path('credits/', show_credits),
    path('evaluation/', startEval),
    path('evaluationInfo/', getEvalInfo),
]
