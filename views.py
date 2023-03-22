from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.db.models import Q
import copy
import random

# Create your views here.
#request --> response (response handler)

def thankyou(request):
    stu_name = request.POST['fname']
    return render(request, 'thankyou.html', {"name": stu_name})

def form(request):
    if request.method == "POST":
        submission = StudentForm(request.POST or None)
        if submission.is_valid():
            submission.save() 
            return thankyou(request)
    else:
        return render(request, 'form.html', {}) #return the page

def create_tables(students, groups):
    students = copy.copy(students)
    if groups > len(students):
        print("bad input llalala")
    else:
        tables = []
        studentsize = len(students)
        extra = studentsize%groups
        substuds = []
        for i in range(groups):
            if extra != 0:
                for j in range(studentsize//groups + 1):
                    substuds.append(students[0])
                    students.remove(students[0])
                tables.append(substuds)
                substuds = []
                extra -= 1
            else:
                for k in range(studentsize//groups):
                    substuds.append(students[0])
                    students.remove(students[0])
                tables.append(substuds)
                substuds = []
        
        return tables

def create_rows(tables, students):
    rows = []
    tablecopy = copy.deepcopy(tables)
    studentcopy = copy.copy(students)
    tablenum = len(tables)
    if tablenum <=3:
        rows.append(studentcopy)
        return rows
    numrows = tablenum//11 + 2
    subrow = []
    extra = tablenum%numrows
    for i in range(numrows):
            if extra != 0:
                for j in range(tablenum//numrows + 1):
                    for p in tablecopy[0]:
                        subrow.append(p)
                    tablecopy.remove(tablecopy[0])
                rows.append(subrow)
                subrow = []
                extra -= 1
            else:
                for k in range(tablenum//numrows):
                    for o in tablecopy[0]:
                        subrow.append(o)
                    tablecopy.remove(tablecopy[0])
                rows.append(subrow)
                subrow = []
        
    return rows

def finalrows(tableslist):
    rows = []
    tablenum = len(tableslist)
    if tablenum <=3:
        rows.append(tableslist)
        return rows
    numrows = tablenum//11 + 2
    subrow = []
    extra = tablenum%numrows
    for i in range(numrows):
            if extra != 0:
                for j in range(tablenum//numrows + 1):
                    subrow.append(tableslist[0])
                    tableslist.remove(tableslist[0])
                rows.append(subrow)
                subrow = []
                extra -= 1
            else:
                for k in range(tablenum//numrows):
                    subrow.append(tableslist[0])
                    tableslist.remove(tableslist[0])
                rows.append(subrow)
                subrow = []
    return rows

def socialsort(list):
    name_list = []
    for stu in list:
        name_list.append(stu.fname)
        name_list.append(stu.lname)
        
    orderlist = Student.objects.filter(fname__in=name_list).filter(lname__in=name_list)
    orderlist = orderlist.order_by('socialrank')
    newlist =[]
    for student in orderlist:
        newlist.append(student)
    return newlist

def mixsort(list):
    name_list = []
    for stu in list:
        name_list.append(stu.fname)
        name_list.append(stu.lname)
        
    orderlist = Student.objects.filter(fname__in=name_list).filter(lname__in=name_list)
    orderlist = orderlist.order_by('socialrank')
    newlist = []
    for student in orderlist:
        newlist.append(student)
    
    newnewlist = []
    for i in range(len(newlist)):
        index = random.randint(0,len(newlist)-1)
        newnewlist.append(newlist[index])
        newlist.remove(newlist[index])
    
    return newnewlist

def focussort(list):
    name_list = []
    for stu in list:
        name_list.append(stu.fname)
        name_list.append(stu.lname)
        
    orderlist = Student.objects.filter(fname__in=name_list).filter(lname__in=name_list)
    orderlist = orderlist.order_by('focus')
    newlist =[]
    for student in orderlist:
        newlist.append(student)
    return newlist

def envsort(list):
    name_list = []
    for stu in list:
        name_list.append(stu.fname)
        name_list.append(stu.lname)
        
    orderlist = Student.objects.filter(fname__in=name_list).filter(lname__in=name_list)
    orderlist = orderlist.order_by('sound_env')
    newlist =[]
    for student in orderlist:
        newlist.append(student)
    return newlist

def sort(rowslist, sortby):
    studentlist = []
    for row in rowslist:
        if sortby in "socialrank":
            newrow = socialsort(row)
        elif sortby in 'socialrankmixed':
            newrow = mixsort(row)
        elif sortby in 'focus':
            newrow = focussort(row)
        elif sortby in "soundenv":
            newrow = envsort(row)
        for poo in newrow:
            studentlist.append(poo)
    return studentlist


def todirectory(request):
    nameteach = request.GET['teachname']
    namelist = nameteach.split(" ")
    firstname = namelist[0]
    lastname = namelist[len(namelist)-1]
    all_students = Student.objects.filter(Q(teachername__icontains=lastname) | Q(teachername__icontains=firstname) | Q(teachername__icontains=lastname.lower()) | Q(teachername__icontains=firstname.lower()) | Q(teachername__icontains=firstname.lower()) | Q(teachername__icontains=firstname.upper()) | Q(teachername__icontains=firstname.capitalize()) | Q(teachername__icontains=lastname.capitalize()))
    if len(all_students) > 0:
        all_students = all_students.order_by('board_distance') #list
        return render(request, "home.html", {'info': all_students, 'teach': lastname.capitalize()})
    else:
        home(request)
        return HttpResponse("You currently have no students in your directory")


def home(request):
    return render(request, 'startpage.html', {})


def seating(request):
    return render(request, 'seating.html', {})


def makechart(request):
    nameteach = request.GET['teachnameagain']
    sorttype = request.GET['type']
    namelist = nameteach.split(" ")
    firstname = namelist[0]
    lastname = namelist[len(namelist)-1]
    all_students = Student.objects.filter(Q(teachername__icontains=lastname) | Q(teachername__icontains=firstname) | Q(teachername__icontains=lastname.lower()) | Q(teachername__icontains=firstname.lower()) | Q(teachername__icontains=firstname.lower()) | Q(teachername__icontains=firstname.upper()) | Q(teachername__icontains=firstname.capitalize()) | Q(teachername__icontains=lastname.capitalize())).order_by('board_distance')
    groupnum = int(request.GET['groupsize'])
    studentlist = []
    for student in all_students:
        studentlist.append(student)
    tables = create_tables(studentlist, groupnum)
    rowslist = create_rows(tables, studentlist)
    sortedstudentlist = sort(rowslist, sorttype)
    
    finaltables = create_tables(sortedstudentlist, groupnum) 
    finalseats = finalrows(finaltables)
    return render(request, "seating.html", {'poo': finalseats})
