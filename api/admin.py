from django.contrib import admin
from .models import Employee, Store, Visit


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    list_per_page = 25


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'employee')
    search_fields = ('name',)
    list_filter = ('employee',)
    ordering = ('name',)
    list_per_page = 25


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'employee', 'date_time', 'latitude', 'longitude')
    search_fields = ('employee__name', 'store__name')
    list_filter = ('employee', 'store')
    ordering = ('-date_time',)
    list_per_page = 25
