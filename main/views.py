from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from models_project.models import Group, Student
from sorl.thumbnail import get_thumbnail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login(request):
    arg={}
    arg.update(csrf(request))
    if request.POST:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            arg['login_error'] = "User not found"
            return render_to_response('login.html', arg)
    else:
        return render_to_response('login.html', arg)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args={}
    args.update(csrf(request))
    args['form']= UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html',args)


def groups(request):
    template = loader.get_template('groups.html')
    list_groups=[]
    groups = Group.objects.all()
    for i in range(1,len(groups)+1):
        context={}
        if bool(Student.objects.filter(group = groups[i-1])):
            context['name_group'] = Group.objects.filter(id=i).values('name_group')[0]['name_group']
            context['count'] = Student.objects.filter(group = groups[i-1]).count()
            id_praerostor = Group.objects.filter(id=i).values('praepostor')[0]['praepostor']
            context['praepostor'] = Student.objects.get(id=id_praerostor)
            context['id_group'] = Group.objects.filter(id=i).values('id')[0]['id']
        else:
            context['name_group'] = Group.objects.filter(id=i).values('name_group')[0]['name_group']
            context['count'] = 0
            context['praepostor'] = ""
            context['id_group'] = Group.objects.filter(id=i).values('id')[0]['id']
        list_groups.append(context)
    context_dictionary = RequestContext(request, {'list_groups':list_groups})
    return HttpResponse(template.render(context_dictionary))


def group(request, id_group):
    template = loader.get_template('group.html')
    list_students = []
    this_group = Group.objects.get(id = id_group)
    students = Student.objects.filter(group=this_group)
    for i in range(len(students)):
        context = {}
        context['student_name'] = students[i]
        context['foto'] = Student.objects.filter(student_name=students[i]).values('foto')[0]['foto']
        list_students.append(context)
    paginator = Paginator(list_students, 1)
    page = request.GET.get('page')
    try:
        list_students = paginator.page(page)
    except PageNotAnInteger:
        list_students = paginator.page(1)
    except EmptyPage:
        list_students = paginator.page(paginator.num_pages)
    context_dictionary = RequestContext(request, {'list_students':list_students})
    return HttpResponse(template.render(context_dictionary))


# def students(request):
#     template = loader.get_template('students.html')
#     list_students=[]
#     students = Student.objects.all()
#     for i in range(1,len(students)+1):
#         context={}
#         context['student_name'] = Student.objects.get(id=i)
#         context['foto'] = Student.objects.filter(id=i).values('foto')[0]['foto']
#         list_students.append(context)
#     paginator = Paginator(list_students, 2)
#     page = request.GET.get('page')
#     try:
#         list_students = paginator.page(page)
#     except PageNotAnInteger:
#         list_students = paginator.page(1)
#     except EmptyPage:
#         list_students = paginator.page(paginator.num_pages)
#     context_dictionary = RequestContext(request, {'list_students':list_students})
#     return HttpResponse(template.render(context_dictionary))


def redaction(request):
    pass


def list_view(request, *args, **kwargs):
    """
    List of all views by url
    """
    return render(request, 'base.html')
    # return render(request, 'console.html', {}) #**second method for getting list_of_possible_command

