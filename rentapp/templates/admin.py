# Импортируем модуль администратора из Django и наши модели Car и Booking
from django.contrib import admin
from .models import Car, Booking


# Определяем класс CarAdmin для настройки отображения модели Car в админке
class CarAdmin(admin.ModelAdmin):
    # list_display указывает, какие поля модели будут отображаться в списке объектов
    list_display = ('brand', 'model', 'year', 'price_per_minute', 'location', 'available')

    # list_filter добавляет возможность фильтрации объектов по указанным полям
    list_filter = ('brand', 'available', 'year')

    # search_fields позволяет осуществлять поиск по указанным полям модели
    search_fields = ('brand', 'model', 'location')


# Определяем класс BookingAdmin для настройки отображения модели Booking в админке
class BookingAdmin(admin.ModelAdmin):
    # list_display указывает, какие поля модели будут отображаться в списке объектов
    list_display = ('user', 'car', 'start_time', 'end_time', 'total_price')

    # readonly_fields делает указанные поля только для чтения, их нельзя редактировать в админке
    readonly_fields = ('total_price',)

    # list_filter добавляет возможность фильтрации объектов по указанным полям
    list_filter = ('car', 'start_time', 'end_time')

    # search_fields позволяет осуществлять поиск по указанным полям модели
    search_fields = ('user__username', 'car__brand', 'car__model')

    # Переопределяем метод save_model для автоматического пересчета общей стоимости бронирования при сохранении
    def save_model(self, request, obj, form, change):
        # Вызываем метод для расчета общей стоимости
        obj.calculate_total_price()
        # Сохраняем объект, используя родительский метод save_model
        super().save_model(request, obj, form, change)


# Регистрируем модели Car и Booking в админке с указанными настройками
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
