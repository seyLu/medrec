from django.contrib import admin

from .models import City, District, Province, Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin[Region]):
    list_display = ("name", "code")
    readonly_fields = [field.name for field in Region._meta.fields]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin[Province]):
    list_display = ("name", "code")
    readonly_fields = [field.name for field in Province._meta.fields]


@admin.register(City)
class CityAdmin(admin.ModelAdmin[City]):
    list_display = ("name", "code")
    readonly_fields = [field.name for field in City._meta.fields]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin[District]):
    list_display = ("name", "code")
    readonly_fields = [field.name for field in District._meta.fields]
