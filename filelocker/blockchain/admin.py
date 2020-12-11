from django.contrib import admin
from .models import BlockChain

# Register your models here.
@admin.register(BlockChain)
class BlockChainAdmin(admin.ModelAdmin):
    list_display = ['data','hash','previous_hash']
