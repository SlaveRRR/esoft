from django.shortcuts import render, redirect
from .forms import ClientRegistrationForm, RealtorRegistrationForm
from mainapp.models import User, RealEstate, User_Real_estate, Offers, Demand, Deal
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout


def registration(request):
    return render(request, 'registration.html')

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


def logout_user(request):
    logout(request)
    return redirect('login')


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

def search_real_estates(city, street, house, apartment, target_city, target_street, target_house, target_apartment):

    distance_city = levenshtein_distance(city, target_city)
    distance_street = levenshtein_distance(street, target_street)
    distance_house = levenshtein_distance(house, target_house)
    distance_apartment = levenshtein_distance(apartment, target_apartment)

    if (
        distance_city <=3
        and distance_street <=3
        and distance_house <=1
        and distance_apartment <=1
    ):
        return True
    else: 
        return False
    

def home(request):
    context = {}

    target_last_name = '' #из POST приходят
    target_first_name = ''
    target_middle_name = ''

    target_city = ''
    target_street = ''

    selected_type = request.GET.get('type')
    selected_city = request.GET.get('city')
    
    all_real_estates = RealEstate.objects.all()

    if selected_type and selected_type != '0':
        all_real_estates = all_real_estates.filter(type=selected_type)

    if selected_city and selected_city != '0':
        all_real_estates = all_real_estates.filter(city=selected_city)


    context['all_real_estates'] = all_real_estates


    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'search_fio':
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
            
            context ['users'] = usersFinal

            return render(request, 'home.html', context)
        
        if action == 'search_real_estate':
            address = request.POST.get('search_real_state') 
            address_parts = address.split(' ') # ['Город', 'Улица', 'Дом', 'Квартира']

            if (len(address_parts) == 4):
                target_city = address_parts[0] 
                target_street = address_parts[1] 
                target_house = address_parts[2] 
                target_apartment = address_parts[3] 

                real_estates = RealEstate.objects.all()

                real_estates_final = []

                for real_estate in real_estates:
                    city = real_estate.city
                    street = real_estate.street
                    house_number = real_estate.house_number
                    apartment_number = real_estate.apartment_number

                    if not real_estate.city:
                        city = ''
                    if not real_estate.street:
                        street = ''
                    if not real_estate.house_number:
                        house_number = ''
                    if not real_estate.apartment_number:
                        apartment_number = ''

                    if search_real_estates(city, street, house_number, apartment_number, target_city, target_street, target_house, target_apartment):
                        real_estates_final.append(f"Найдена недвижимость: {real_estate.heading}, город: {real_estate.city}, улица: {real_estate.street}, дома {real_estate.house_number}, квартира {real_estate.apartment_number}\n")
                
                context['real_estates'] = real_estates_final

                return render(request, 'home.html', context)
            
            else:
                context['alert'] = 'Убедитесь, что вы ввели все поля (город улица дом квартира)'
    
    return render(request, 'home.html', context)


# @login_required
def profile(request):

    context = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'change_user':
            user_id = request.POST.get('editId')
            user_id = int(user_id)
            user = User.objects.get(pk=user_id)
            user.nickname = request.POST.get('editNickname')
            user.last_name = request.POST.get('editLastName')
            user.first_name = request.POST.get('editFirstName')
            user.middle_name = request.POST.get('editMiddleName')
            user.email = request.POST.get('editEmail')
            user.phone_number = request.POST.get('editPhone')
            user.commission = request.POST.get('editCommission')
            user.save()

        if action == 'change_real_estate':
            id = request.POST.get('id')
            real_estate = RealEstate.objects.get(pk=id) #изменяемый объект
            real_estate.heading = request.POST.get('heading')
            real_estate.city = request.POST.get('city')
            real_estate.street = request.POST.get('street')
            real_estate.house_number = request.POST.get('house_number')
            real_estate.apartment_number = request.POST.get('apartment_number')
            real_estate.latitude = request.POST.get('latitude')
            real_estate.longitude = request.POST.get('longitude')
            real_estate.floor = request.POST.get('floor')
            real_estate.floor = request.POST.get('number_of_floors')
            real_estate.number_of_rooms = request.POST.get('number_of_rooms')
            real_estate.square = request.POST.get('square')
            real_estate.type = request.POST.get('type')
            real_estate.save()

        if action == 'change_offer':
            id = request.POST.get('id')
            offer = Offers.objects.get(pk=id) #изменяемый объект
            offer.price = request.POST.get('price')
            offer.real_estate_id = request.POST.get('select-real-estates') #селектом
            offer.rieltor_id = request.POST.get('select-realtor') #селектом
            offer.save()

        if action == 'change_demand':
            id = request.POST.get('id')
            demand = Demand.objects.get(pk=id) #изменяемый объект
            demand.type = request.POST.get('type')
            demand.address = request.POST.get('address')
            demand.min_price = request.POST.get('min_price')
            demand.max_price = request.POST.get('max_price')
            demand.min_square = request.POST.get('min_square')
            demand.max_square = request.POST.get('max_square')
            demand.min_number_of_rooms = request.POST.get('min_number_of_rooms')
            demand.max_number_of_rooms = request.POST.get('max_number_of_rooms')
            demand.min_floor = request.POST.get('min_floor')
            demand.max_floor = request.POST.get('max_floor')
            demand.min_number_of_floors = request.POST.get('min_number_of_floors')
            demand.max_number_of_floors = request.POST.get('max_number_of_floors')
            demand.save()

        if action == 'delete-acc':
            user = User.objects.get(pk=request.user.id)
            offers = Offers.objects.filter(client = request.user.id)
            demands = Demand.objects.filter(client = request.user.id)

            if offers or demands:
                user.delete_value == False
            else: 
                user.delete_value == True

            if (user.delete_value == True):
                logout(request)
                user.delete()
                return render(request, 'home.html')
            else:
                context['alert'] = 'невозможно удалить т к у вас есть предложение или потребность'

        if action == 'delete-real-estate': # если недвижка связана с предложением - то не удалять ее
            id = request.POST.get('id')
            offer = Offers.objects.filter(real_estate = id)
            if offer:
                context['alert'] = 'невозможно удалить т к недвижимость связана с предложением'
            else:
                real_estate = RealEstate.objects.get(pk=id)
                real_estate.delete()
                context['alert'] = 'недвижимость удалена'

        if action == 'delete-offer':
            id = request.POST.get('id')
            deal = Deal.objects.filter(offer=id)
            if deal:
                context['alert'] = 'невозможно удалить т к с предложением связана сделка'
            else:
                offer = Offers.objects.get(pk=id)
                offer.delete()
                context['alert'] = 'Предложение удалено'

        if action == 'delete-demand':
            id = request.POST.get('id')
            deal = Deal.objects.filter(demand=id)
            if deal:
                context['alert'] = 'невозможно удалить т к с потребностью связана сделка'
            else:
                demand = Demand.objects.get(pk=id)
                demand.delete()
                context['alert'] = 'Потребность удалена'
        
            
    user_real_estates = User_Real_estate.objects.filter(user_id=request.user.id) #объекты юзер_недвижимости конкретного юзера {id, user_id, real_estate_id}
    real_estates = []

    for index in user_real_estates: 
        new_real_estates = RealEstate.objects.get(pk=index.user_real_estate_id)
        real_estates.append(new_real_estates)


    #Список предложений конкретного пользователя
    offers = Offers.objects.filter(client_id=request.user.id)

    #Список потребностей конкретного пользователя
    demands = Demand.objects.filter(client_id=request.user.id)

    #Список риэлторов
    realtors = User.objects.filter(is_realtor=1)

    context['offers'] = offers #массив предложений
    context['real_estates'] = real_estates #массив (объектов) недвижек конкретного юзера
    context['demands'] = demands
    context['realtors'] = realtors

    return render(request, 'profile.html', context)


def real_estate(request):
    return render(request, 'real_estate.html')


def create_an_apartment(request):

    context = {}

    if request.method == 'POST':
        newApartment= RealEstate()
        newApartment.heading = request.POST.get('heading')
        newApartment.city = request.POST.get('city')
        newApartment.street = request.POST.get('street')
        newApartment.house_number = request.POST.get('house_number')
        newApartment.apartment_number = request.POST.get('apartment_number')
        newApartment.latitude = request.POST.get('latitude')
        newApartment.longitude = request.POST.get('longitude')
        newApartment.floor = request.POST.get('floor')
        newApartment.number_of_rooms = request.POST.get('number_of_rooms')
        newApartment.square = request.POST.get('square')
        newApartment.type = request.POST.get('type')
        newApartment.save()
        
        if newApartment:
            context = {'alert': 'Данные сохранены'}
        else:
            context = {'alert': 'Данные некорректны'}

        newuser_real_estate_object = User_Real_estate()
        user_id = User.objects.get(pk=request.user.id)
        newuser_real_estate_object.user_id = user_id
        newuser_real_estate_object.user_real_estate = newApartment
        newuser_real_estate_object.save()


    return render(request, 'create_an_apartment.html', context)


def create_a_house(request):

    context = {}

    if request.method == 'POST':
        newHouse= RealEstate()
        newHouse.heading = request.POST.get('heading')
        newHouse.city = request.POST.get('city')
        newHouse.street = request.POST.get('street')
        newHouse.house_number = request.POST.get('house_number')
        newHouse.apartment_number = request.POST.get('apartment_number')
        newHouse.latitude = request.POST.get('latitude')
        newHouse.longitude = request.POST.get('longitude')
        newHouse.number_of_floors = request.POST.get('floor')
        newHouse.number_of_rooms = request.POST.get('number_of_rooms')
        newHouse.square = request.POST.get('square')
        newHouse.type = request.POST.get('type')
        newHouse.save()

        if newHouse:
            context = {'alert': 'Данные сохранены'}
        else:
            context = {'alert': 'Данные некорректны'}

        newuser_real_estate_object = User_Real_estate()
        user_id = User.objects.get(pk=request.user.id)
        newuser_real_estate_object.user_id = user_id
        newuser_real_estate_object.user_real_estate = newHouse
        newuser_real_estate_object.save()

    return render(request, 'create_a_house.html', context)


def create_land(request):

    context = {}

    if request.method == 'POST':
        newLand = RealEstate()
        newLand.heading = request.POST.get('heading')
        newLand.city = request.POST.get('city')
        newLand.street = request.POST.get('street')
        newLand.house_number = request.POST.get('house_number')
        newLand.apartment_number = request.POST.get('apartment_number')
        newLand.latitude = request.POST.get('latitude')
        newLand.longitude = request.POST.get('longitude')
        newLand.square = request.POST.get('square')
        newLand.type = request.POST.get('type')
        newLand.save()

        if newLand:
            context = {'alert': 'Данные сохранены'}
        else:
            context = {'alert': 'Данные некорректны'}

        newuser_real_estate_object = User_Real_estate()
        user_id = User.objects.get(pk=request.user.id)
        newuser_real_estate_object.user_id = user_id
        newuser_real_estate_object.user_real_estate = newLand
        newuser_real_estate_object.save()

    return render(request, 'create_land.html', context)


def search_offers_demands(request):
    return render(request, 'search_offers_demands.html')


def create_offer(request):
    if request.method == 'POST':
        newOffer = Offers()
        newOffer.price = request.POST.get('price')
        newOffer.client_id = request.user.id
        newOffer.real_estate_id = request.POST.get('select-real-estates')
        newOffer.rieltor_id = request.POST.get('select-realtor')
        newOffer.save()
        user = User.objects.get(pk=request.user.id)
        user.delete_value = False

    #Список риэлторов
    realtors = User.objects.filter(is_realtor=1)

    #Список недвижек конкретного пользователя 
    user_real_estates = User_Real_estate.objects.filter(user_id=request.user.id) #объекты юзер_недвижимости конкретного юзера {id, user_id, real_estate_id}
    real_estates = []
    for index in user_real_estates: 
        new_real_estate = RealEstate.objects.get(pk=index.user_real_estate_id)
        real_estates.append(new_real_estate)


    context = {'realtors': realtors, 'real_estates': real_estates}
    return render(request, 'create_offer.html', context)

def create_demand(request):
    if request.method == 'POST':
        newDemand = Demand()
        newDemand.client_id = request.user.id
        newDemand.rieltor_id = request.POST.get('select-realtor')
        newDemand.type = request.POST.get('select-type')
        newDemand.address = request.POST.get('address')
        newDemand.min_price = request.POST.get('min-price')
        newDemand.max_price = request.POST.get('max-price')
        newDemand.min_square = request.POST.get('min-square')
        newDemand.max_square = request.POST.get('max-square')
        newDemand.min_number_of_rooms = request.POST.get('min-number-of-rooms')
        newDemand.max_number_of_rooms = request.POST.get('max-number-of-rooms')
        newDemand.min_floor = request.POST.get('min-floor')
        newDemand.max_floor = request.POST.get('max-floor')
        newDemand.min_number_of_floors = request.POST.get('min-number-of-floors')
        newDemand.max_number_of_floors = request.POST.get('max-number-of-floors')
        newDemand.save()
        
        user = User.objects.get(pk=request.user.id)
        user.delete_value = False

    #Список риэлторов
    realtors = User.objects.filter(is_realtor=1)

    context = {'realtors': realtors}
    return render(request, 'create_demand.html', context)


def deals(request):
    if request.method == 'POST':
        deal = Deal()
        deal.heading = request.POST.get('heading')
        deal.offer_id = request.POST.get('select-offer')
        deal.demand_id = request.POST.get('select-demand')
        deal.confirmed = 0
        deal.save()

    demands = Demand.objects.all()
    offers = Offers.objects.all()
    deals = Deal.objects.all()

    context = {'demands': demands, 'offers': offers, 'deals': deals}

    return render(request, 'deals.html', context)

def manage_clients(request):
    context = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'choose-client':
            client_id = request.POST.get('select-client')
            #потребности
            client_offers = Offers.objects.filter(client = client_id)
            #предложения
            client_demands = Demand.objects.filter(client = client_id)
            context['client_offers'] = client_offers
            context['client_demands'] = client_demands

        if action == 'choose-realtor':
            realtor_id = request.POST.get('select-realtor')
            #потребности
            realtor_offers = Offers.objects.filter(rieltor = realtor_id)
            #предложения
            realtor_demands = Demand.objects.filter(rieltor = realtor_id)
            context['realtor_offers'] = realtor_offers
            context['realtor_demands'] = realtor_demands

    realtors = User.objects.filter(is_realtor=1)
    clients = User.objects.filter(is_realtor=0)
    context['realtors'] = realtors
    context['clients'] = clients



    return render(request, 'manage_clients.html', context)
