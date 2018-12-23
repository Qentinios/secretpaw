from django.contrib import admin

from secretpawapp.models import Tag, Profile, CharacterNSFWTypes, Character, Gift, Setting

admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(CharacterNSFWTypes)
admin.site.register(Character)
admin.site.register(Gift)
admin.site.register(Setting)

