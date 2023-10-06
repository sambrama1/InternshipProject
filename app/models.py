from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator




# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    confirmpassword = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class SignIn(models.Model):
    phonenumber = models.IntegerField(null=True)
    password = models.CharField(max_length=255)

class Dishes(models.Model):
    CATEGORY_CHOICES = (
        ('Baverages', 'Baverages'),
        ('South Indians', 'South Indians'),
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='Baverages')
    description = models.CharField(max_length=255)

    


    def __str__(self):
        return self.name
    
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'Table {self.table_number}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return f'table no {self.table.table_number} -- {self.dishes.name}'


class Orderplaced(models.Model):
    STATUS_CHOICES = (
    ('accepted','Accepted'),
    ('served','Served'),
    ('delivered','Delivered'),
    )    

    User = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, models.CASCADE)
    dishes = models.ForeignKey(Dishes,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.IntegerField(null=True)
    Ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dishes.name}--- quantity({self.quantity})----  TotalAmount({self.amount}))"


     