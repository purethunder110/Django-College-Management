from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.models import User,Group
# Create your views here.
from .models import *
from datetime import datetime,date
import calendar

'''internal functions'''
def usercategorisation(user):
    if user.is_superuser:
        return 0
    elif user.groups.filter(name="PRINCIPAL").exists():
        return 1
    elif user.groups.filter(name="HOD").exists():
        return 2
    elif user.groups.filter(name="TEACHER").exists():
        return 3
    elif user.groups.filter(name="STUDENT").exists():
        return 4
    else:
        return -1
    
#internal service
def remove_mark(l,symbol):
    m=[]
    s=""
    for i in l:
        if i==symbol:
            m.append(s)
            s=""
        else:
            s+=i
    m.append(s)
    return m

def get_dates(year, month):
    cal = calendar.monthcalendar(year, month)
    dates_list = []
    for week in cal:
        for day in week:
            if day != 0:
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                dates_list.append(date_str)

    return dates_list

#initial Setup
def initusersetup():
    group_manage=Group.objects.get_or_create(name="PRINCIPAL")
    group_manage=Group.objects.get_or_create(name="HOD")
    group_manage=Group.objects.get_or_create(name="TEACHER")
    group_manage=Group.objects.get_or_create(name="STUDENT")
    defaultprincipal=User.objects.create_user(username="princ",password="12345")
    defaultprincipal.save()
    group_manage=Group.objects.get_or_create(name="PRINCIPAL")
    group_manage[0].user_set.add(defaultprincipal)
    defaultprincipal.save()
    libuser=User.objects.create_user(username="LibUser",password="Admin123")
    libuser.save()
    group_manage=Group.objects.get_or_create(name="LIBRARY")
    group_manage[0].user_set.add(libuser)
    libuser.save()

'''django special function'''
def login_page(request):
    if request.method=="GET":
        try:
            initusersetup()
        except:
            pass
        return render(request,"htmldocs/login.html")
    if request.method=="POST":
        name=request.POST.get("username")
        password=request.POST.get("password")
        login_type=request.POST.get("typeselect")
        user_auth=authenticate(username=name,password=password)
        if user_auth:
            login(request,user_auth)
            type=str(request.user.groups.all()[0])
            if type=="STUDENT":
                return redirect("/studentDashboard")
            elif type=="TEACHER":
                return redirect("/teacherDashboard")
            elif type=="HOD":
                return redirect("hodDashboard")
            elif type=="PRINCIPAL":
                return redirect("/principalDashboard")
            elif type=="LIBRARY":
                return redirect("/librarySystem")
            else:
                return HttpResponse("error 404 occured!!")
        else:
            return HttpResponse("login details incorrect")

#studentDashboard
@user_passes_test(lambda user:usercategorisation(user)==4)
def studentDashboard(request):
    if request.method=="GET":
        announcementData=announcement_model.objects.all()
        studentModel=student_model.objects.get(student_name=request.user.username)
        StudentData=student_attendance_model.objects.filter(student_id=studentModel)
        courseTaken=studentModel.student_course.course_name
        SendDate=get_dates(datetime.now().year,datetime.now().month)
        booklist=book_model.objects.all()
        bookIssued=book_issue_model.objects.filter(username=studentModel)
        issuedbook=book_issue_model.objects.all()
        sendBook=[]
        for i in booklist:
            flag=True
            for j in issuedbook:
                if i.id==j.book.id:
                    flag=False
            if flag:
                sendBook+=[i]
        presentData={}
        for i in SendDate:
            flag=False
            for j in StudentData:
                if str(j.date_of_attendance)==i:
                    presentData[i]="Present"
                    flag=True
            if flag==False:
                presentData[i]="Absent"
        send_data={
            "studentModel":studentModel,
            'announcementData':announcementData,
            'PresentData':presentData,
            "courseTaken":courseTaken,
            "BookList":sendBook,
            "issuedbook":bookIssued,
                }
        return render(request,"htmldocs/student_dashboad.html",send_data)
    if request.method=="POST":
        #saving issue books
        if "bookissue" in request.POST:
            bookissue=request.POST.get("bookissue")
            for i in bookissue:
                bookobj=book_model.objects.get(id=i)
                user=student_model.objects.get(student_name=request.user.username)
                newissue=book_issue_model(username=user,book=bookobj,date_issued=date.today())
                newissue.save()
        
        if "IssueID" in request.POST:
            IssueID=request.POST.get("IssueID")
            issueobj=book_issue_model.objects.get(id=IssueID)
            issueobj.delete()
            
        #display data
        announcementData=announcement_model.objects.all()
        studentModel=student_model.objects.get(student_name=request.user.username)
        StudentData=student_attendance_model.objects.filter(student_id=studentModel)
        courseTaken=studentModel.student_course.course_name
        SendDate=get_dates(datetime.now().year,datetime.now().month)
        booklist=book_model.objects.all()
        bookIssued=book_issue_model.objects.filter(username=studentModel)
        issuedbook=book_issue_model.objects.all()
        sendBook=[]
        for i in booklist:
            flag=True
            for j in issuedbook:
                if i.id==j.book.id:
                    flag=False
            if flag:
                sendBook+=[i]
        presentData={}
        for i in SendDate:#'StudentData':
            flag=False
            for j in StudentData:
                #print("\ntest=",str(j.date_of_attendance)==i)
                if str(j.date_of_attendance)==i:
                    presentData[i]="Present"
                    flag=True
            if flag==False:
                presentData[i]="Absent"
        send_data={
            'announcementData':announcementData,
            'PresentData':presentData,
            "courseTaken":courseTaken,
            "BookList":sendBook,
            "issuedbook":bookIssued,
                }
        return render(request,"htmldocs/student_dashboad.html",send_data)



#teacher dashboard
@user_passes_test(lambda user:usercategorisation(user)==3)
def teacherDashboard(request):
    if request.method=="GET":
        Teacher=teacher_model.objects.get(teacher_name=request.user.username)
        image=Teacher_picture.objects.get(teacher=Teacher)
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        #AttendanceData=student_attendance_model.objects.filter(date_of_attendance=datetime.now())
        StudentData=student_model.objects.all()
        send_data={'announcementData':announcementData,"courseData":courseData,'studentAttendance':StudentData,"Profilepic":image}
        return render(request,"htmldocs/teacher_dashboard.html",send_data)
    if request.method=="POST":
        datacollect=request.POST
        #announcement title
        if "announcementTitle" in request.POST:
            title=request.POST.get("announcementTitle")
            body=request.POST.get("announcementBody")
            announcementData=announcement_model(title=title,designation="Teacher",announcement=body)
            announcementData.save()
        #attendance date
        if "AttendanceStudentID" in request.POST:
            StudentID=datacollect.get("AttendanceStudentID")
            StudentID=remove_mark(StudentID,',')
            StudentName=datacollect.get("StudentName")
            DateSelected=datacollect.get("DateSelected")
            if DateSelected=='':
                DateSelected=datetime.now().date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    try:
                        check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    except:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()
            else:
                Dates=remove_mark(DateSelected,"-")
                DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    if check_flag.is_valid:
                        pass
                    else:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()
        
        #display data
        Teacher=teacher_model.objects.get(teacher_name=request.user.username)
        image=Teacher_picture.objects.get(teacher=Teacher)
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        StudentData=student_model.objects.all()
        send_data={'announcementData':announcementData,"courseData":courseData,'studentAttendance':StudentData,"Profilepic":image,}
        return render(request,"htmldocs/teacher_dashboard.html",send_data)

#hod dashboard
@user_passes_test(lambda user:usercategorisation(user)==2)
def hodDashboard(request):
    if request.method=="GET":
        DateSelected=datetime.now().date()
        HOD=HOD_model.objects.get(HOD_name=request.user.username)
        image=HOD_picture.objects.get(HOD=HOD)
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        StudentData=student_model.objects.all()
        TeacherData=teacher_model.objects.get(HOD=HOD)
        HOD_course=course_model.objects.get(HOD_undertaken=HOD)
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={"HOD_course":HOD_course,
                   "StudentAttendanceFilter":studentname,
                   'announcementData':announcementData,
                   "courseData":courseData,
                   'studentAttendance':StudentData,
                   "TeacherData":TeacherData,
                   "Profilepic":image
                   }
        return render(request,"htmldocs/HOD.html",send_data)
    
    if request.method=="POST":
        datacollect=request.POST
        DateSelected=datetime.now().date()
        #announcement title
        if "announcementTitle" in request.POST:
            title=datacollect.get("announcementTitle")
            body=datacollect.get("announcementBody")
            announcementData=announcement_model(title=title,designation="HOD",announcement=body)
            announcementData.save()
        #attendance date
        if "LoadDate" in request.POST:
            DateSelected=datacollect.get("LoadDate")
            Dates=remove_mark(DateSelected,"-")
            DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
        
        if "RegisterName" in request.POST:
            typeuser=datacollect.get("RegisterType")
            name=datacollect.get("RegisterName")
            password=datacollect.get("RegisterPassword")
            course=course_model.objects.get(course_name=datacollect.get("CourseSelect"))
            if typeuser=="Student":
                Teacher=teacher_model.objects.get(teacher_name=datacollect.get("ClassTeacher"))
                rno=datacollect.get("Rollno")
                student_register=student_model(student_name=name,password=password,roll_number=rno,student_course=course,student_head=Teacher)
                student_register.save()
                profilepic=request.FILES.get("PictureProfile")
                stdobj=student_model.objects.get(student_name=name)
                imageobj=Student_picture(student=stdobj,picture=profilepic)
                imageobj.save()
                #register the user login
                user_signup=User.objects.create_user(username=name,password=password)
                user_signup.save()
                grp_manage=Group.objects.get_or_create(name="STUDENT")
                grp_manage[0].user_set.add(user_signup)
                user_signup.save()
            else:
                hod=HOD_model.objects.get(HOD_name=request.user)
                Teacher_reg=teacher_model(teacher_name=name,password=password,teacher_course=course,HOD=hod)
                Teacher_reg.save()
                profilepic=request.FILES.get("PictureProfile")
                tobj=teacher_model.objects.get(teacher_name=name)
                imageobj=Teacher_picture(teacher=tobj,picture=profilepic)
                imageobj.save()
                #register the user login
                user_signup=User.objects.create_user(username=name,password=password)
                user_signup.save()
                grp_manage=Group.objects.get_or_create(name="TEACHER")
                grp_manage[0].user_set.add(user_signup)
                user_signup.save()

        #attendance post
        if "AttendanceStudentID" in request.POST:
            StudentID=datacollect.get("AttendanceStudentID")
            StudentID=remove_mark(StudentID,',')
            StudentName=datacollect.get("StudentName")
            DateSelected=datacollect.get("DateSelected")
            if DateSelected=='':
                DateSelected=datetime.now().date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    try:
                        check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    except:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()
            else:
                Dates=remove_mark(DateSelected,"-")
                DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    if check_flag.is_valid:
                        pass
                    else:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()
        #display data
        HOD=HOD_model.objects.get(HOD_name=request.user.username)
        image=HOD_picture.objects.get(HOD=HOD)
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        StudentData=student_model.objects.all()
        TeacherData=teacher_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        HOD_course=course_model.objects.get(HOD_undertaken=HOD)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={"HOD_course":HOD_course,'datetest':DateSelected,"StudentAttendanceFilter":studentname,'announcementData':announcementData,"courseData":courseData,'studentAttendance':StudentData,"TeacherData":TeacherData,"Profilpic":image}
        return render(request,"htmldocs/HOD.html",send_data)
        
 
@user_passes_test(lambda user:usercategorisation(user)==1)
def principalDashboard(request):
    if request.method=="GET":
        DateSelected=datetime.now().date()
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        StudentData=student_model.objects.all()
        TeacherData=teacher_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        HODlist=HOD_model.objects.all()
        studentname=[]
        studentclass=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'datetest':DateSelected,
                   "StudentAttendanceFilter":studentname,
                   'announcementData':announcementData,
                   "courseData":courseData,
                   'studentAttendance':StudentData,
                   "TeacherData":TeacherData,
                   "HODList":HODlist,
                   }
        return render(request,"htmldocs/Principal.html",send_data)
    if request.method=="POST":
        datacollect=request.POST
        #announcement title
        if "announcementTitle" in request.POST:
            title=datacollect.get("announcementTitle")
            body=datacollect.get("announcementBody")
            announcementData=announcement_model(title=title,designation="PRINCIPAL",announcement=body)
            announcementData.save()
        
        #new joining
        if "RegisterName" in request.POST:
            typeuser=datacollect.get("RegisterType")
            name=datacollect.get("RegisterName")
            password=datacollect.get("RegisterPassword")
            if typeuser=="Student":
                course=course_model.objects.get(course_name=datacollect.get("CourseSelect"))
                Teacher=teacher_model.objects.get(teacher_name=datacollect.get("ClassTeacher"))
                rno=datacollect.get("Rollno")
                student_register=student_model(student_name=name,password=password,roll_number=rno,student_course=course,student_head=Teacher)
                student_register.save()
                profilepic=request.FILES.get("PictureProfile")
                stdobj=student_model.objects.get(student_name=name)
                imageobj=Student_picture(student=stdobj,picture=profilepic)
                imageobj.save()
                #register the user login
                user_signup=User.objects.create_user(username=name,password=password)
                user_signup.save()
                grp_manage=Group.objects.get_or_create(name="STUDENT")
                grp_manage[0].user_set.add(user_signup)
                user_signup.save()
            elif typeuser=="Teacher":
                course=course_model.objects.get(course_name=datacollect.get("CourseSelect"))
                hod=HOD_model.objects.get(HOD_name=course.HOD_undertaken.HOD_name)
                Teacher_reg=teacher_model(teacher_name=name,password=password,teacher_course=course,HOD=hod)
                Teacher_reg.save()
                profilepic=request.FILES.get("PictureProfile")
                tobj=teacher_model.objects.get(teacher_name=name)
                imageobj=Teacher_picture(teacher=tobj,picture=profilepic)
                imageobj.save()
                #register the user login
                user_signup=User.objects.create_user(username=name,password=password)
                user_signup.save()
                grp_manage=Group.objects.get_or_create(name="TEACHER")
                grp_manage[0].user_set.add(user_signup)
                user_signup.save()
            elif typeuser=="HOD":
                newHOD=HOD_model(HOD_name=name,password=password)
                newHOD.save()
                HODget=HOD_model.objects.get(HOD_name=name)
                course_name=datacollect.get("CourseInput")
                print(course_name)
                new_course=course_model(course_name=course_name,HOD_undertaken=HODget)
                new_course.save()
                profilepic=request.FILES.get("PictureProfile")
                imageobj=HOD_picture(HOD=HODget,picture=profilepic)
                imageobj.save()
                #register the user login
                user_signup=User.objects.create_user(username=name,password=password)
                user_signup.save()
                grp_manage=Group.objects.get_or_create(name="HOD")
                grp_manage[0].user_set.add(user_signup)
                user_signup.save()
            else:
                return HttpResponse("<h1>Internal Error Occured.Please Report To an Admin<h1>")
        
        #attendance post
        if "AttendanceStudentID" in request.POST:
            StudentID=datacollect.get("AttendanceStudentID")
            StudentID=remove_mark(StudentID,',')
            StudentName=datacollect.get("StudentName")
            DateSelected=datacollect.get("DateSelected")
            if DateSelected=='':
                DateSelected=datetime.now().date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    try:
                        check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    except:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()
            else:
                Dates=remove_mark(DateSelected,"-")
                DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
                for i in StudentID:
                    Studentget=student_model.objects.get(id=i)
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    if check_flag.is_valid:
                        pass
                    else:
                        attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                        attendance_save.save()

        #display data
        DateSelected=datetime.now().date()
        announcementData=announcement_model.objects.all()
        courseData=course_model.objects.all()
        StudentData=student_model.objects.all()
        TeacherData=teacher_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        HODlist=HOD_model.objects.all()
        studentname=[]
        studentclass=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'datetest':DateSelected,
                   "StudentAttendanceFilter":studentname,
                   'announcementData':announcementData,
                   "courseData":courseData,
                   'studentAttendance':StudentData,
                   "TeacherData":TeacherData,
                   "HODList":HODlist,
                   }
        return render(request,"htmldocs/Principal.html",send_data)


@login_required(login_url="/")
def HODPastAttendance(request,DateSelected):
    if request.method=="GET":
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,'studentAttendance':StudentData,'courseData':courseData}
        return render(request,"htmldocs/HODpastattendance.html",send_data)
    if request.method=="POST":
        datacollect=request.POST
        StudentID=datacollect.get("AttendanceStudentID")
        StudentID=remove_mark(StudentID,',')
        StudentName=datacollect.get("StudentName")
        if DateSelected=='':
            DateSelected=datetime.now().date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        else:
            Dates=remove_mark(DateSelected,"-")
            DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        #return object
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,'studentAttendance':StudentData,'courseData':courseData}
        return render(request,"htmldocs/HODpastattendance.html",send_data)

@login_required(login_url="/")
def TeacherPastAttendance(request,DateSelected):
    if request.method=="GET":
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,'studentAttendance':StudentData,'courseData':courseData}
        return render(request,"htmldocs/Teacherpastattendance.html",send_data)
    if request.method=="POST":
        datacollect=request.POST
        StudentID=datacollect.get("AttendanceStudentID")
        StudentID=remove_mark(StudentID,',')
        StudentName=datacollect.get("StudentName")
        if DateSelected=='':
            DateSelected=datetime.now().date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        else:
            Dates=remove_mark(DateSelected,"-")
            DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        #return object
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,'studentAttendance':StudentData,'courseData':courseData}
        return render(request,"htmldocs/Teacherpastattendance.html",send_data)

#principalPastattendance
@login_required(login_url="/")
def PrincipalPastattendance(request,DateSelected):
    if request.method=="GET":
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,
                   'studentAttendance':StudentData,
                   'courseData':courseData}
        return render(request,"htmldocs/principalPastattendance.html",send_data)
    if request.method=="POST":
        datacollect=request.POST
        StudentID=datacollect.get("AttendanceStudentID")
        StudentID=remove_mark(StudentID,',')
        StudentName=datacollect.get("StudentName")
        if DateSelected=='':
            DateSelected=datetime.now().date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        else:
            Dates=remove_mark(DateSelected,"-")
            DateSelected=datetime(int(Dates[0]),int(Dates[1]),int(Dates[2])).date()
            for i in StudentID:
                Studentget=student_model.objects.get(id=i)
                try:
                    check_flag=student_attendance_model.objects.get(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                except:
                    attendance_save=student_attendance_model(date_of_attendance=DateSelected,student_id=Studentget,mark_attendance=True)
                    attendance_save.save()
        #return object
        StudentData=student_model.objects.all()
        courseData=course_model.objects.all()
        Attendance_student=student_attendance_model.objects.filter(date_of_attendance=DateSelected)
        studentname=[]
        studentclass=[]
        StudentID=[]
        for i in StudentData:
            for j in Attendance_student:
                if i==j.student_id:
                    studentname.append(i.student_name)
                    studentclass.append(i.student_course)
        send_data={'StudentAttendanceFilter':studentname,
                   'studentAttendance':StudentData,
                   'courseData':courseData}
        return render(request,"htmldocs/principalPastattendance.html",send_data)

@login_required(login_url="/")
def librarybookadd(request):
    if request.method=="GET":
        bookData=book_model.objects.all()
        issuedata=book_issue_model.objects.all()
        sendData={
            "BookData":bookData,
            "issueData":issuedata,
        }
        return render(request,"htmldocs/libsystem.html",sendData)
    if request.method=="POST":
        bookname=request.POST.get("bookName")
        author=request.POST.get("author")
        year=request.POST.get("publishYear")
        book=book_model(name=bookname,author=author,publish_year=year)
        book.save()
        #display data
        bookData=book_model.objects.all()
        issuedata=book_issue_model.objects.all()
        sendData={
            "BookData":bookData,
            "issueData":issuedata,
        }
        return render(request,"htmldocs/libsystem.html",sendData)

@login_required(login_url="/")
def logoutpage(request):
    logout(request)
    return redirect("/")