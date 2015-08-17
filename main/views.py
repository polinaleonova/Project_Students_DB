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
    for i in groups:
        context={}
        context['name_group'] = i
        context['count'] = Student.objects.filter(group = i).count()
        context['id_group'] = Group.objects.get(name_group=i).id
        if bool(Student.objects.filter(praepostor_of_group__name_group=i)):
            context['praepostor'] = Student.objects.filter(praepostor_of_group__name_group=i)[0]
        else:
            context['praepostor']='-'
        list_groups.append(context)
    context_dictionary = RequestContext(request, {'list_groups':list_groups,'object_for_changing':'groups'})
    return HttpResponse(template.render(context_dictionary))


def group(request, id_group):
    template = loader.get_template('group.html')
    list_students = []
    id =id_group
    this_group = Group.objects.get(id = id)
    students = Student.objects.filter(group=this_group)
    for i in students:
        context = {}
        context['student_name'] = i
        context['foto'] = str(Student.objects.get(student_name=i).foto)
        list_students.append(context)
    paginator = Paginator(list_students, 1)
    page = request.GET.get('page')
    try:
        list_students = paginator.page(page)
    except PageNotAnInteger:
        list_students = paginator.page(1)
    except EmptyPage:
        list_students = paginator.page(paginator.num_pages)
    context_dictionary = RequestContext(request, {'list_students':list_students,'object_for_changing':'group'})
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

def submition(request, entity, id):
    if entity == 'group':
        group = Group.objects.get(id=id)
        if request.method == "POST":
            group.name_group = request.POST.get('name_group')
            group.save()
            return redirect('/changing/groups')
    if entity == 'student':
        student = Student.objects.get(id=id)
        group_with_this_st = student.group
        id_group_with_this_st = str(Group.objects.get(name_group=group_with_this_st).id)
        if request.method == "POST":
            student.student_name = request.POST.get('student_name')
            student.ticket_number = request.POST.get('student_ticket_number')
            student.date_birthday = request.POST.get('dob')
            student.foto = request.POST.get('foto')
            if student.student_name != '':
                student.save()
                return redirect('/changing_data/groups/edition/'+id_group_with_this_st+'/')
    return redirect('/changing_data/groups/edition/'+id_group_with_this_st+'/')


def changing_data(request, entity, action, id = None):
    command = entity+action

    def groups_delete(id):
        gr_to_delete = Group.objects.get(id=id)
        gr_to_delete.delete()
        return redirect('/changing/groups')

    def groups_creation(*args):
        if request.method == "POST":
            name_group = request.POST.get('name_group')
            if name_group != '':
                gr_to_create = Group.objects.create(name_group=name_group)
                gr_to_create.save()
                return redirect('/changing/groups')
            else:
                return redirect('/changing/groups')
        else:
            return redirect('/changing/groups/')

    def groups_edition(id):
        template = loader.get_template('form _edit_group.html')
        this_group = Group.objects.get(id=id)
        students = Student.objects.filter(group=this_group)
        list_students=[]
        for i in students:
            context={}
            context['student_name'] = i
            context['student_ticket_number'] =  Student.objects.get(student_name=i).ticket_number
            context['dob'] =  Student.objects.get(student_name=i).date_birthday
            context['foto'] = str(Student.objects.get(student_name=i).foto)
            context['id_student'] = Student.objects.get(student_name=i).id
            list_students.append(context)

        context_dictionary = RequestContext(request, {'list_students': list_students, 'name_group': this_group,'object_for_changing': 'group','id_group':id,'student':'student'})
        return HttpResponse(template.render(context_dictionary))

    def student_edition(id_student):
        student=Student.objects.get(id=id_student)
        context={}
        context['student_name'] = student
        context['student_ticket_number'] = student.ticket_number
        context['dob'] =  student.date_birthday
        context['foto'] = str(student.foto)
        context['id_student'] = student.id
        context['object_for_changing'] = 'student'
        # if request.method == "POST":
        #     student_name=request.POST.get('student_name')
        #     ticket_number =request.POST.get('student_ticket_number')
        #     date_birthday=request.POST.get('dob')
        #     foto = request.POST.get('foto')
        #     if student_name != '':
        #         st_to_edit = Student.objects.get(id=id_student)
        #         st_to_edit.update(student_name=student_name,date_birthday=date_birthday,ticket_number=ticket_number,group=group_for_new_student)
        #         st_to_edit.save()
        #         return redirect('/changing/groups')
        return render_to_response('form _edit_student.html', context)


    # def ololo(id_group):
    #     if request.method == "POST":
    #         name_group = request.POST.get('name_group')
    #         # students=Student.objects.filter(group=name_group)
    #         this_group=Group.objects.get(id=id_group)
    #         this_group.update(name_group=name_group)
    #         this_group.save()
    #         student_name = request.POST.get('name_student')
    #         ticket_number = request.POST.get('student_ticket_number')
    #         date_birthday = request.POST.get('dob')
    #         foto = request.POST.get('foto')
    #         st_to_update = Student.objects.create(student_name=student_name, date_birthday=date_birthday,ticket_number=ticket_number,group=group_for_new_student)
    #         st_to_update.save()
    #         return redirect('/changing/groups')


    def student_delete(id):
        group_with_this_st = Student.objects.get(id=id).group
        id_group_with_this_st = str(Group.objects.get(name_group=group_with_this_st).id)
        st_to_delete = Student.objects.get(id=id)
        st_to_delete.delete()
        return redirect('/changing_data/groups/edition/'+id_group_with_this_st+'/')



    def student_creation(id_group):
            if request.method == "POST":
                group_for_new_student = Group.objects.get(id=id_group)
                student_name = request.POST.get('student_name')
                ticket_number = request.POST.get('student_ticket_number')
                date_birthday = request.POST.get('dob')
                foto = request.POST.get('foto')
                if student_name != '':
                    st_to_create = Student.objects.create(student_name=student_name, date_birthday=date_birthday, ticket_number=ticket_number, group_id=group_for_new_student.id)
                    st_to_create.save()
                    return redirect('/changing_data/groups/edition/'+id_group+'/')
                else:
                    return redirect('/changing_data/groups/edition/'+id_group+'/')
            else:
                return redirect('/changing_data/groups/edition/'+id_group+'/')


    dict = {'groups/delete': groups_delete,
            'groups/creation': groups_creation,
            'groups/edition': groups_edition,
            'student/delete': student_delete,
            'student/creation': student_creation,
            'student/edition': student_edition
    }
    return dict[command](id)


def changing(request, entity):
    if entity == 'group':
        template_group = loader.get_template('changing_group.html')
        context_dictionary = RequestContext(request, {'object_for_changing':entity, 'id':'ololo'})
        return HttpResponse(template_group.render(context_dictionary))
    else:
        template_groups = loader.get_template('changing_groups.html')
        list_groups=[]
        groups = Group.objects.all()
        for i in groups:
            context={}
            context['name_group'] = i
            context['count'] = Student.objects.filter(group = i).count()
            context['id_group'] = Group.objects.get(name_group=i).id
            if bool(Student.objects.filter(praepostor_of_group__name_group=i)):
                context['praepostor'] = Student.objects.filter(praepostor_of_group__name_group=i)[0]
            else:
                context['praepostor']='-'
            list_groups.append(context)
        context_dictionary = RequestContext(request, {'list_groups':list_groups,
                                                          'object_for_changing':'groups'})
        return HttpResponse(template_groups.render(context_dictionary))


def list_view(request, *args, **kwargs):
    """
    List of all views by url
    """
    return render(request, 'base.html')
    # return render(request, 'console.html', {}) #**second method for getting list_of_possible_command

