from django.db import models

# Create your models here.
class Course(models.Model):
    nama= models.CharField(max_length=38)
    waktu= models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nama

class Course_Prerequisit(models.Model):
    coursePemilik= models.ForeignKey('Course', related_name='cpPemilik')
    coursePrereq= models.ForeignKey('Course',related_name='cpPrereq')

    def __str__(self):
        return str(self.coursePemilik)+'-'+str(self.coursePrereq)

class Course_Alternative(models.Model):
    coursePemilik= models.ForeignKey('Course', related_name='caPemilik')
    courseAlternate= models.ForeignKey('Course', related_name='caAlternate')

    def __str__(self):
        return str(self.coursePemilik)+'-'+str(self.courseAlternate)

class UserStatus(models.Model):
    learningStyle= models.ForeignKey('LearningStyle')

class User_CompletedCourse(models.Model):
    user= models.ForeignKey('UserStatus')
    course= models.ForeignKey('Course')

    def save(self, *args, **kwargs):
        super(User_CompletedCourse, self).save(*args, **kwargs) # Call the "real" save() method.
        #apakah course merupakan alternative?
        if len(Course_Alternative.objects.filter(courseAlternate=self.course))>0:
            user=User_CompletedCourse()
            user.user=self.user
            #jika iya maka cari pemilik dan pemilik dimasukan kedalam user completed
            for alternateCourseObject in Course_Alternative.objects.filter(courseAlternate=self.course):
                user.course= alternateCourseObject.coursePemilik
                user.save()
            pass


    def __str__(self):
        return str(self.course)

class User_Knowledge(models.Model):
    user= models.ForeignKey('UserStatus')
    knowledge= models.ForeignKey('Concept')

    def __str__(self):
        return str(self.knowledge)
    #============================================================================OVER HERE!!!!
    #kalau user knowledge nambah berarti course diatasnya dirubah
    #cek kalau course diatasnya bobot 0 berarti pake yang initial
    #kala course bobotnya ada berarti update
    def save(self, *args, **kwargs):
        super(User_Knowledge, self).save(*args, **kwargs) # Call the "real" save() method.
        coursePemilikKnowledge= self.knowledge.course
        apl=AdaptiveLearningPath(coursePemilikKnowledge)
        if coursePemilikKnowledge.waktu==0:
            apl.weightingCourse(coursePemilikKnowledge)
        else:
            apl.weightingCourse(coursePemilikKnowledge, self.knowledge)
    #=========================================================================================

class LearningStyle(models.Model):
    nama= models.CharField(max_length=38)

class Concept(models.Model):
    course= models.ForeignKey('Course', blank=True, null=True)
    nama= models.CharField(max_length=38)
    waktuDiperlukan= models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.course)+'-'+self.nama+'-'+str(self.waktuDiperlukan)

class EdgeConcept(models.Model):
    dari= models.ForeignKey('Concept', related_name='dari')
    ke= models.ForeignKey('Concept', related_name='ke')
    bobot= models.FloatField(blank=True, null=True)

class AdaptiveLearningPath:
    #for every prereq yang belum dipelajari dan sudah diurutkan
        #prereq dengan urutan lp n-1
        #recursive
        #cek apakah dia sudah dipelajar?
            # kalau belum dan tidak ada alternative maka dimasukan ke stack
            #jika ada alternative cek apakah alternativenya sudah ada yang di[elajari
                #jika sudah tidak perlu dimasukan ke stack
                #jika belum masukan alt ke stack
    def __init__(self, nodeGoal):
        self.goal = nodeGoal
        self.path = []

    def test(self, node):
        return Course_Prerequisit.objects.filter(coursePemilik= node)[0].coursePrereq

    #untested
    def weightingCourse(self, course, iConcept=None):
        if iConcept!=None:
            #masuk sini kalau concept baru masuk ke knowledge
            #untuk setiap course yang nampung concept ini
            #kurangi total weight dengan waktu yang baru dimasukin ini
            course=iConcept.course
            waktuPengurang= iConcept.waktuDiperlukan
            course.waktu -= waktuPengurang
            course.save()
     #===============================================
            #masuk sini untuk itung initial course
        #buat var penampung
        #panggil setiap concept yang belum dipelajari untuk course yang dihitung
            #totalkan setiap bobot pada concept
        #update bobot course dengan jumlah
        else:
            totalWeight=0
            concepts=Concept.objects.filter(course=course)
            for concept in concepts:
                if self.isConceptDipelajari(concept) == False:
                    totalWeight+=concept.waktuDiperlukan
            course.waktu=totalWeight
            course.save()



    def isConceptDipelajari(self, concept):
        if len(User_Knowledge.objects.filter(knowledge=concept))>0:
            return True
        return False

    def isCourseDipelajari(self, tujuan=None):
        #jika jumlah di completedCourse lebih dari0 berarti sudah dipelajari, return true

        if len(User_CompletedCourse.objects.filter(course= tujuan))>0:
            return True
        return False

    def generatePath(self, goal=None):
        if goal==None:
            goal=self.goal
        result=[]
        result.append(goal)
        prereqCurrent= Course_Prerequisit.objects.filter(coursePemilik=goal)
        #cek apakah goal sudah dipelajari
        if self.isCourseDipelajari(goal) == True:
            return result
        #============================================================================OVER HERE!!!!
        #cek weight yang bersangkutan
        #kalau weight yang bersangkutan 0 panggil set weight diatas
            #kalau ga punya alternativ itung weightnya kalau punya jangan
        if goal.waktu==None:
            if len(Course_Alternative.objects.filter(coursePemilik=goal))==0:
                self.weightingCourse(goal)
        #=========================================================================================
        #cek apakah goal merupakan course besar?
        jumlahAlter=len(Course_Alternative.objects.filter(coursePemilik=goal))
        if jumlahAlter > 0:
            #jika cpurse besar, untuk setiap prerequisit dari alternate course check apakah prerequisit tersebut sudah dipelajar jika belum ulangi atas
            for courseAlternativeDariPemilik in Course_Alternative.objects.filter(coursePemilik=goal).order_by('-courseAlternate__waktu'):
                #jika belum dipelajari
                if self.isCourseDipelajari(tujuan=courseAlternativeDariPemilik.courseAlternate) == False:
                #masuk ke fungsi sendiri dan hasilnya di append ke path
                    result+=self.generatePath(courseAlternativeDariPemilik.courseAlternate)
                    break
        #jika bukan course besar maka cek prerequisitnya
        elif jumlahAlter == 0:
            #untuk setiap prereq dari course besar check apakah pre req sudah dipelajari? jika belum masukan ke fungsi recursive
            for prereqCourseBesar in prereqCurrent:
                if self.isCourseDipelajari(tujuan=prereqCourseBesar.coursePrereq) == False:

                    result+=self.generatePath(prereqCourseBesar.coursePrereq)

        self.path=result
        return self.path

class Simulation:
    #set default LS
    #set defrault complete
    #set default knowledge
    #hitung ulang initial weight
    def setDefaultLS(self):
        pass
    def setDefaultComplete(self):
        pass
    def setDefaultKnowledge(self):
        pass
    def initialCourseWeight(self):
        #get all
        pass
    def reset(self):
        pass