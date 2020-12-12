from django.contrib import admin
from .models import BlockChain,File
from django.contrib import messages

# Register your models here.
@admin.register(BlockChain)
class BlockChainAdmin(admin.ModelAdmin):
    list_display = ['user','hash','previous_hash']

admin.site.register(File)
