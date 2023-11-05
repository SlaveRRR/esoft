from django.shortcuts import render, redirect
from .forms import ClientRegistrationForm, RealtorRegistrationForm
from mainapp.models import User
from django.contrib.auth.hashers import make_password

def client_registration(request):
    if request.method == 'POST':
        newUser = User()
        newUser.nickname = request.POST.get('nicknamesignup')
        newUser.first_name = request.POST.get('firstnamesignup')
        newUser.last_name = request.POST.get('lastnamesignup')
        newUser.middle_name = request.POST.get('middlenamesignup')
        newUser.email = request.POST.get('emailsignup')
        newUser.phone_number = request.POST.get('phonesignup')
        newUser.password = make_password(request.POST.get('passwordsignup'))
        newUser.password_confirmation = request.POST.get('passwordsignup_confirm')
        newUser.is_realtor = False
        newUser.save()

    else:
        return render(request, 'client_registration.html')
    return render(request, 'client_registration.html')


def realtor_registration(request):
    if request.method == 'POST':
        newUser = User()
        newUser.nickname = request.POST.get('nicknamesignup')
        newUser.first_name = request.POST.get('firstnamesignup')
        newUser.last_name = request.POST.get('lastnamesignup')
        newUser.middle_name = request.POST.get('middlenamesignup')
        newUser.commission = request.POST.get('commissionsignup')
        newUser.password = make_password(request.POST.get('passwordsignup'))
        newUser.password_confirmation = request.POST.get('passwordsignup_confirm')
        newUser.is_realtor = True
        newUser.save()
    else:
        return render(request, 'realtor_registration.html')
    return render(request, 'realtor_registration.html')


def levenshtein_distance(s1, s2): # передаем текущее из User all() и искомое имя/фам/отч
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1) 
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)

    for i, c1 in enumerate(s1): #перебираем индекс/символ s1
        current_row = [i + 1] #это число соответствует количеству операций

        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2) #подмена символа
            current_row.append(min(insertions, deletions, substitutions)) #добавл мин значение из трех операций
        previous_row = current_row

    return previous_row[-1] #минимальное количество операций


def search_fio(last_name, first_name, middle_name, target_last_name, target_first_name, target_middle_name):
    distance_last_name = levenshtein_distance(last_name, target_last_name)
    distance_first_name = levenshtein_distance(first_name, target_first_name)
    distance_middle_name = levenshtein_distance(middle_name, target_middle_name)

    if (
        distance_last_name <= 3
        and distance_first_name <= 3
        and distance_middle_name <= 3
    ):
        return True # пользователя на котором True -> заносим в итоговый вывод
    else:
        return False
    

def home(request):
    target_last_name = '' #из POST приходят
    target_first_name = ''
    target_middle_name = ''

    if request.method == 'POST':
        fio = request.POST.get('query') # получаем фио из формы
        fio_parts = fio.split(' ') # ['Иванов', 'Петр', 'Сергеевич']
        
        target_last_name = fio_parts[0] #иванов
        target_first_name = fio_parts[1] #петр
        target_middle_name = fio_parts[2] #сергеевич

        users = User.objects.all()
    
        usersFinal = []

        for user in users:
            if search_fio(user.last_name, user.first_name, user.middle_name, target_last_name, target_first_name, target_middle_name):
                usersFinal.append(f"Найден клиент: {user.last_name} {user.first_name} {user.middle_name}")
        
        context = {'users':usersFinal}

        return render(request, 'home.html', context)
    
    return render(request, 'home.html')