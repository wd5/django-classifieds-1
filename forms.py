from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
#from django.forms.models import inlineformset_factory

from common.forms import CommonPostEditForm
from . models import ClassifiedsPost, ClassifiedsCategory, ClassifiedsPostImages

class ClassifiedsEditForm( CommonPostEditForm ):
    category = forms.ModelMultipleChoiceField( 
        queryset = ClassifiedsCategory.objects.all(),
        required = False,
        widget = FilteredSelectMultiple( 
            'categories',
            False,
        )
    )

    class Meta( CommonPostEditForm.Meta ):
        fields = ( 
            'title',
            'content',
            'category',
            'country',
            'city',
            'site',
            'email',
            'phone',
            'address',
            'skype',
            'google_plus',
            'facebook',
            'twitter',
            'tags',
        )
        model = ClassifiedsPost


class ImageUploadForm( forms.ModelForm ):
    post = forms.ModelChoiceField( 
        queryset = ClassifiedsPost.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = ClassifiedsPostImages
