from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=255, blank=True, unique=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    commission = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_realtor = models.BooleanField(null=True)
    email = models.EmailField(blank=True, null=True)
    Active = models.SmallIntegerField(null=True, default=1)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []

class RealEstate(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(max_length=255, default=1)
    type = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=255, null=True)
    apartment_number = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    floor = models.CharField(max_length=255, null=True)
    number_of_floors = models.CharField(max_length=255, null=True)
    number_of_rooms = models.CharField(max_length=255, null=True)
    square = models.CharField(max_length=255, null=True)

class User_Real_estate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE)

class Offers(models.Model):
    heading = models.CharField(max_length=255, default=1)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    rieltor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rieltor")
    real_estate = models.ForeignKey(RealEstate, on_delete=models.CASCADE) #уже существ недвижка
    price = models.CharField(max_length=255)

class Demand(models.Model):
    heading = models.CharField(max_length=255, default=1)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clientindemand")
    rieltor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rieltorindemand")
    type = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    min_price = models.CharField(max_length=255)
    max_price = models.CharField(max_length=255)
    min_square = models.CharField(max_length=255)
    max_square = models.CharField(max_length=255)
    min_number_of_rooms = models.CharField(max_length=255, null=True)
    max_number_of_rooms = models.CharField(max_length=255, null=True)
    min_floor = models.CharField(max_length=255, null=True)
    max_floor = models.CharField(max_length=255, null=True)
    min_number_of_floors = models.CharField(max_length=255, null=True)
    max_number_of_floors = models.CharField(max_length=255, null=True)

class Deal(models.Model):        
    heading = models.CharField(max_length=255, default=1)
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name="offerDeal")
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name="demandDeal")
    confirmed = models.CharField(max_length=2)

    def calculate_commission(self):
        commission_seller = 45
        commission_buyer = 45
        #отчисления компаниии
        costBuyer_company = 0
        cost_seller_apartment_company = 0
        cost_seller_house_company = 0
        cost_seller_land_company = 0

        # риэлтор продавца
        if (self.offer.rieltor.commission):
            commission_seller = int(self.offer.rieltor.commission)
        # риэлтор покупателя
        if(self.demand.rieltor.commission):
            commission_buyer = int(self.demand.rieltor.commission)

        #просто стоимость недвижимости
        cost_offer = int(self.offer.price)
        
        # общая стоимость (компания + риэлтор) от покупателя
        costBuyer = int((cost_offer * 3)/100) #
        cost_realtor_buyer = int((costBuyer * commission_buyer)/100 ) #  
        type = self.offer.real_estate.type
 
        costBuyer_company = int(costBuyer - cost_realtor_buyer) # 

        if (type == 'apartment'):
            # общая стоимость (компания + риэлтор) от продавца
            costApartment = int(36000 + (cost_offer*1)/100)
            cost_realtor_seller_apartment = int((costApartment * commission_seller)/100)
            cost_seller_apartment_company = int(costApartment - cost_realtor_seller_apartment)
            cont = {'cost_seller_apartment_company': cost_seller_apartment_company, 'costBuyer_company': costBuyer_company, 'cost_realtor_seller_apartment': cost_realtor_seller_apartment, 'cost_realtor_buyer': cost_realtor_buyer }

        if (type == 'house'):
            costHouse = int(30000 + (cost_offer/100)*2)
            cost_realtor_seller_house = int((costHouse * commission_seller)/100)
            cost_seller_house_company = int(costHouse - cost_realtor_seller_house)
            cont = {'cost_seller_house_company': cost_seller_house_company, 'costBuyer_company': costBuyer_company, 'cost_realtor_seller_house': cost_realtor_seller_house, 'cost_realtor_buyer': cost_realtor_buyer }

        if (type == 'land'):
            costLand = int(30000 + (cost_offer/100)*1) 
            cost_realtor_seller_land = int((costLand * commission_seller)/100)
            cost_seller_land_company = int(costLand - cost_realtor_seller_land)
            cont = {'cost_seller_land_company': cost_seller_land_company, 'costBuyer_company': costBuyer_company, 'cost_realtor_seller_land': cost_realtor_seller_land, 'cost_realtor_buyer': cost_realtor_buyer }

        return cont
