from django.contrib import admin


from common.admin import CommonPostAdmin, CommonCategoryAdmin
from . models import ClassifiedsCategory, ClassifiedsPost

class ClassifiedsCategoryAdmin( CommonCategoryAdmin ):
    pass

class ClassifiedsPostAdmin( CommonPostAdmin ):
    list_display = ( 'title', 'author', 'date_edit', 'date_add', 'status', 'country', 'city', )

admin.site.register( ClassifiedsCategory, ClassifiedsCategoryAdmin )
admin.site.register( ClassifiedsPost, ClassifiedsPostAdmin )
