from django.contrib import admin
from .models import profiledatadb,postdb,Collab_Information_tabledb,Member_Information,syncAudios_table

admin.site.register(profiledatadb)
admin.site.register(postdb)
admin.site.register(Collab_Information_tabledb)
admin.site.register(Member_Information)
admin.site.register(syncAudios_table)

# Register your models here.
