from django.contrib import admin

# Register your models here.
from .models import User, category, auction, bid, komen

admin.site.register(User)
admin.site.register(category)
admin.site.register(auction)
admin.site.register(bid)
admin.site.register(komen)