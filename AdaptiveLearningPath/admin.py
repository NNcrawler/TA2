from django.contrib import admin
from AdaptiveLearningPath import models as alp

# Register your models here.
admin.site.register(alp.Course)
admin.site.register(alp.UserStatus)
admin.site.register(alp.Concept)
admin.site.register(alp.EdgeConcept)
admin.site.register(alp.LearningStyle)
admin.site.register(alp.Course_Alternative)
admin.site.register(alp.Course_Prerequisit)
admin.site.register(alp.User_CompletedCourse)
admin.site.register(alp.User_Knowledge)