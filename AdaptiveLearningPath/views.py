from django.shortcuts import render
from AdaptiveLearningPath import models as alp

# Create your views here.
def index(request):
    rawAllCourseAvailable = alp.Course.objects.all()
    AllCourseAvailable = [str(anu) for anu in rawAllCourseAvailable]
    rawUser_knowledge= alp.User_Knowledge.objects.all()
    user_knowledge= [str(anu) for anu in rawUser_knowledge]
    rawUser_completed= alp.User_CompletedCourse.objects.all()
    user_completed= [str(anu) for anu in rawUser_completed]


    goal=alp.Course.objects.get(nama='Restful API')
    path=alp.AdaptiveLearningPath(nodeGoal=goal)
    path=path.generatePath()

    #path=alp.AdaptiveLearningPath(goal)
    #path=path.test(goal)

    result = {
        'userKnowledge' : user_knowledge,
        'userComplete' : user_completed,
        'allCourseAvailable' : AllCourseAvailable,
        'path' : path
    }
    return render(request,'AdaptiveLearningPath/index.html', result)

def viz(request):

    result={}
    return render(request, 'AdaptiveLearningPath/visualize LP.html', result)
    pass