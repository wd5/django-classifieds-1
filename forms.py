from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
#from django.forms.models import inlineformset_factory

from common.forms import CommonPostEditForm
from . models import ClassifiedsPost, ClassifiedsCategory, ClassifiedsPostImages

class ClassifiedsEditForm( CommonPostEditForm ):
    category = forms.ModelMultipleChoiceField( 
        queryset = ClassifiedsCategory.objects.all(),
        required = True,
        widget = FilteredSelectMultiple( 
            'categories',
            False,
        )
    )

    class Meta( CommonPostEditForm.Meta ):
        model = ClassifiedsPost
        fields = ( 
            'title',
            'content',
            'category',
            'in_stock',
            'site',
            'email',
            'phone',
            'skype',
            'google_plus',
            'facebook',
            'twitter',
            'tags',
        )



class ImageUploadForm( forms.ModelForm ):
    post = forms.ModelChoiceField( 
        queryset = ClassifiedsPost.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = ClassifiedsPostImages
