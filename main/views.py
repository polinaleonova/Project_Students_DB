from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from models_project.models import Group, Student
from sorl.thumbnail import get_thumbnail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login(request):
    arg = {}
    arg.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session.user = user
            return redirect('/groups/')
        else:
            arg['login_error'] = "User not found"
            return render_to_response('login.html', arg)
    else:
        return render_to_response('login.html', arg)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(
                username=newuser_form.cleaned_data['username'],
                password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)


def groups(request):
    template = loader.get_template('groups.html')
    list_groups = []
    groups = Group.objects.all()
    for group_ in groups:
        context = dict({
            'name_group': group_.name_group,
            'count': group_.student_set.count(),
            'id_group': group_.id,
            'praepostor': group_.praepostor.student_name
            if group_.praepostor else '-'
        })
        list_groups.append(context)
    context_dictionary = RequestContext(request,
                                        {'list_groups': list_groups,
                                         'object_for_changing': 'groups'})
    return HttpResponse(template.render(context_dictionary))


def group(request, id_group):
    template = loader.get_template('group.html')
    list_students = []
    this_group = Group.objects.get(id=id_group)
    students = Student.objects.filter(group=this_group)
    for student in students:
        context = dict({
            'student_name': student.student_name,
            'foto': str(student.foto)
        })
        list_students.append(context)
    paginator = Paginator(list_students, 5)
    page = request.GET.get('page')
    try:
        list_students = paginator.page(page)
    except PageNotAnInteger:
        list_students = paginator.page(1)
    except EmptyPage:
        list_students = paginator.page(paginator.num_pages)
    context_dictionary = RequestContext(request,
                                        {'list_students': list_students,
                                         'name_group': this_group.name_group,
                                         'group_id': this_group.id,
                                         'object_for_changing': 'group'})
    return HttpResponse(template.render(context_dictionary))


def submition(request, entity, id):
    if entity == 'group':
        group_ = Group.objects.get(id=id)
        if request.method == "POST":
            group_.name_group = request.POST.get('name_group')
            group_.praepostor_id = request.POST.get('praepostor_id')
            group_.save()
            return redirect('/changing/groups')
    else:
        student = Student.objects.get(id=id)
        group_with_this_st = student.group
        id_group_with_this_st = str(Group.objects.get(
            name_group=group_with_this_st).id)
        if request.method == "POST":
            student.student_name = request.POST.get('student_name')
            student.ticket_number = request.POST.get('student_ticket_number')
            student.date_birthday = request.POST.get('dob')
            foto = request.FILES.get('foto')
            if foto:
                student.foto = foto
            if student.student_name != '':
                student.save()
                return redirect('/changing_data/groups/edition/' +
                                id_group_with_this_st + '/')


def changing_data(request, entity, action, id=None):
    command = '{}/{}'.format(entity, action)

    def groups_delete(id):
        gr_to_delete = Group.objects.get(id=id)
        gr_to_delete.delete()
        return redirect('/changing/groups')

    def groups_creation(*args):
        if request.method == "POST":
            name_group = request.POST.get('name_group')
            if name_group != '':
                Group.objects.create(name_group=name_group)
        return redirect('/changing/groups/')

    def groups_edition(id):
        template = loader.get_template('form _edit_group.html')
        this_group = Group.objects.get(id=id)
        students = this_group.student_set.all()
        list_students = []
        for student in students:
            context = dict({
                'student_name': student.student_name,
                'student_ticket_number': student.ticket_number,
                'dob': student.date_birthday,
                'foto': str(student.foto),
                'id_student': student.id
            })
            list_students.append(context)

        context_dictionary = RequestContext(request, {
            'list_students': list_students,
            'praepostor_id': this_group.praepostor_id,
            'name_group': this_group.name_group,
            'object_for_changing': 'group',
            'id_group': id,
            'student': 'student'})
        return HttpResponse(template.render(context_dictionary))

    def student_edition(id_student):
        student = Student.objects.get(id=id_student)
        context = dict({
            'student': student,
            'foto': str(student.foto),
            'object_for_changing': 'student'
        })
        return render_to_response('form _edit_student.html', context)

    def student_delete(id):
        student = Student.objects.get(id=id)
        group_with_this_st = student.group
        id_group_with_this_st = str(group_with_this_st.id)
        student.delete()
        return redirect('/changing_data/groups/edition/' +
                        id_group_with_this_st + '/')

    def student_creation(id_group):
        if request.method == "POST":
            group_for_new_student = Group.objects.get(id=id_group)
            student_name = request.POST.get('student_name')
            ticket_number = request.POST.get('student_ticket_number')
            date_birthday = request.POST.get('dob')
            foto = request.FILES.get('foto')
            if student_name != '':
                st_to_create = Student.objects.create(
                    student_name=student_name,
                    date_birthday=date_birthday,
                    ticket_number=ticket_number,
                    foto=foto,
                    group_id=group_for_new_student.id)
                st_to_create.save()
        return redirect(
            '/changing_data/groups/edition/'+id_group+'/')

    dict_ = {
        'groups/delete': groups_delete,
        'groups/creation': groups_creation,
        'groups/edition': groups_edition,
        'student/delete': student_delete,
        'student/creation': student_creation,
        'student/edition': student_edition
    }
    return dict_[command](id)


def changing(request, entity):
    template_groups = loader.get_template('changing_groups.html')
    list_groups = []
    groups = Group.objects.all()
    for group_ in groups:
        context = dict({
            'name_group': group_.name_group,
            'count': group_.student_set.count(),
            'id_group': group_.id,
            'praepostor': group_.praepostor.student_name
            if group_.praepostor else '-'
        })
        list_groups.append(context)
    context_dictionary = RequestContext(request,
                                        {'list_groups': list_groups,
                                         'object_for_changing': 'groups'})
    return HttpResponse(template_groups.render(context_dictionary))


def list_view(request, *args, **kwargs):
    return render(request, 'base.html')
