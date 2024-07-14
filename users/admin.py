from django.contrib import admin
from .models import AddCredit


class AddCreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')

admin.site.register(AddCredit, AddCreditAdmin)
# Register your models here.
