from django.contrib import admin

from .models import Cancer, Snp, Gene

admin.site.register(Cancer)
admin.site.register(Snp)
admin.site.register(Gene)
