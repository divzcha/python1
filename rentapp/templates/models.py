# Импортируем необходимые модули и классы из Django и других библиотек
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Модель автомобиля
# max_length - максимальная длина поля (символы); verbose_name - отображаемое имя; defaults - предопределённое значение (записывается, если при заполнении поле оставили пустым)
# max_digits - для полей типа "Decimal" (символы до запятой); decimal_places - символы после запятой.
class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Бренд", default="Неизвестный бренд")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год")
    price_per_minute = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Цена за минуту")
    location = models.CharField(max_length=100, verbose_name="Локация")
    available = models.BooleanField(default=True, verbose_name="Доступность")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

# Модель бронирования автомобиля
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Внешний ключ к предопределённой таблице Django с каскадным удалением (при удалении связанной записи из таблицы пользователя удалится и эта запись)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Метод для расчета общей стоимости бронирования
    def calculate_total_price(self):
        duration = Decimal((self.end_time - self.start_time).total_seconds() / 60)
        self.total_price = duration * self.car.price_per_minute
        return self.total_price

    # Переопределение метода save для автоматического расчета общей стоимости при сохранении
    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Аренда машины - {self.car} клиентом: {self.user.username}"