from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Module, ModuleInstances, Professors, Rating


# Create your views here.

@csrf_exempt
def HandleLogin(request):
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username = un, password = pw)
        if user is not None:
            if user.is_active:
                login(request, user)
                if (user.is_authenticated):
                    request.session['user'] = un
                    return JsonResponse({
                        'status': 'Success',
                        'result': un + ' is logged in'
                    })
            else:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'Disabled account'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'result': 'That username and/or password are not correct or have not been registered'
            })

@csrf_exempt
def HandleRegistration(request):
    if (request.method == 'POST'):
        un = request.POST['username']
        pw = request.POST['password']
        mail = request.POST['email']
        user = authenticate(request, username = un, password = pw)
        if user is None or not user.is_active:
            try:
                user = User.objects.create_user(username = un, email = mail, password = pw)
                login(request, user)
                request.session['user'] = un
                return JsonResponse({
                    'status': 'Success',
                    'result': 'User has been registered and is now logged in'
                })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'User could not be registered'
                })

@csrf_exempt
def HandleLogout(request):
    if request.method == 'POST':
        if 'user' not in request.session:
            return JsonResponse({
                'status': 'Failed',
                'result': 'You must login before logging out'
            })
        else:
            try:
                un = request.session['user']
                logout(request)
                return JsonResponse({
                    'status': 'Success',
                    'result': un + ' has been logged out'
                })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'Logout attempt failed'
                })

@csrf_exempt
def HandleList(request):
    if request.method == 'GET':
        if 'user' not in request.session:
            return JsonResponse({
                'status': 'Failed',
                'result': 'You must login or register before accessing the data'
            })
        else:
            mods = ModuleInstances.objects.all()
            if not mods:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'No modules in the database'
                })
            all_modules = []
            for mod in mods:
                professors = mod.professors.all()
                all_profs = dict()
                for prof in professors:
                    all_profs[prof.name] = prof.professor_id
                all_modules.append({'code': mod.module.module_code, 'name': mod.module.name, 'year': mod.year, 'sem': mod.semester, \
                    'names': all_profs})
            return JsonResponse({
                'status': 'Success',
                'result': all_modules
            })

@csrf_exempt
def HandleRate(request):
    if request.method == 'POST':
        if 'user' not in request.session:
            return JsonResponse({
                'status': 'Failed',
                'result': 'You must login or register before accessing the data'
            })
        else:
            rate = int(request.POST['rating'])
            if rate < 1 or rate > 5:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'Rating must be between 1 and 5'
                })
            try:
                mod = Module.objects.get(module_code = request.POST['module_code'])
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That module code does not correspond to any modules'
                })
            p_id = request.POST['professor_id']
            yr = int(request.POST['year'])
            if yr < 0:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'Year value cannot be negative'
                })
            sem = int(request.POST['semester'])
            if sem != 1 and sem != 2:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'Semester value must be 1 or 2'
                })
            try:
                pro = Professors.objects.get(professor_id = p_id)
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That professor does not exist'
                })
            try:
                mod = ModuleInstances.objects.get(module = mod, year = yr, semester = sem, professors = pro)
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That module instance does not exist'
                })
            new_rate = Rating(rating = rate, module = mod, professor = pro)
            new_rate.save()
            return JsonResponse({
                'status': 'Success',
                'result': 'Your rating has been added to the database'
            })

@csrf_exempt
def HandleAverage(request):
    if request.method == 'GET':
        if 'user' not in request.session:
            return JsonResponse({
                'status': 'Failed',
                'result': 'You must login or register before accessing the data'
            })
        else:
            p_id = request.GET.get('professor_id', '')
            m_code = request.GET.get('module_code', '')
            try:
                prof = Professors.objects.get(professor_id = p_id)
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That professor does not exist'
                })
            try:
                module_obj = Module.objects.get(module_code = m_code)
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That module code does not correspond to any modules'
                })
            mods = ModuleInstances.objects.filter(module = module_obj, professors = prof)
            if not mods:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'That module does not exist or the professor given does not teach it'
                })
            total = 0
            num_ratings = 0
            average = 0
            for mod in mods:
                all_ratings = Rating.objects.filter(module = mod, professor = prof)
                for rate in all_ratings:
                    total += rate.rating
                    num_ratings += 1
            if num_ratings == 0:
                    return JsonResponse({
                        'status': 'Failed',
                        'result': 'There are no ratings for this professor in this module'
                    })
            average = total / num_ratings
            return JsonResponse({
                'status': 'Success',
                'result': average,
                'prof': prof.name,
                'module': mod.module.name
            })

@csrf_exempt
def HandleView(request):
    if request.method == 'GET':
        if 'user' not in request.session:
            return JsonResponse({
                'status': 'Failed',
                'result': 'You must login or register before accessing the data'
            })
        else:
            all_ratings = []
            for prof in Professors.objects.all():
                total = 0
                num = 0
                for rate in Rating.objects.filter(professor = prof):
                    total += rate.rating
                    num += 1
                average = 0
                if num != 0:
                    average = total / num
                rating = {"name": prof.name, "id": prof.professor_id, "rating": average}
                all_ratings.append(rating)
            if not all_ratings:
                return JsonResponse({
                    'status': 'Failed',
                    'result': 'No professors in the database yet'
                })
            return JsonResponse({
                'status': 'Success',
                'result': all_ratings
            })