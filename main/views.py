from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf

from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm

from models_project.models import Group


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


    # form = UserCreationForm()
    #
    # if request.method == 'POST':
    #     data = request.POST.copy()
    #     errors = form.get_validation_errors(data)
    #     if not errors:
    #         new_user = form.save(data)
    #         return HttpResponseRedirect("/auth/register/")
    # else:
    #     data, errors = {}, {}
    #
    # return render_to_response("/register.html", {
    #     'form' : forms.FormWrapper(form, data, errors)
    # })

def groups(request):
    group = Group.objects.all()
    return render_to_response('base.html',{'group': group, 'username': auth.get_user(request).username})

    # template = loader.get_template('base.html')
    # list_groups=[{'group_name':'a', 'number':34, 'praepostor':'vasya'}, {'group_name':'b', 'number':14, 'praepostor':'gen'}]
    # context_dictionary = RequestContext(request, {'list_groups':list_groups})
    # return HttpResponse(template.render(context_dictionary))



def students(request):
    context={}
    context['username']=auth.get_user(request).username
    return render_to_response('base.html',context)


def redaction(request):
    pass


def list_view(request, *args, **kwargs):
    """
    List of all views by url
    """
    return render(request, 'base.html')
    # return render(request, 'console.html', {}) #**second method for getting list_of_possible_command

