from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from common.decorators import json_response

from . models import ClassifiedsPost, ClassifiedsPostImages
from . forms import ImageUploadForm

@login_required
@json_response
def image_upload( request ):

    id = int( request.POST['post'] )

    try:
        post = ClassifiedsPost.objects.get( pk = id )
    except ClassifiedsPost.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = ImageUploadForm( request.POST, request.FILES )
        if form.is_valid():
            image = form.save()

    data = {
        'post':{
            'id':post.id,
        },
        'image':{
            'id':image.id,
            'x100':image.x100.url,
            'x150':image.x150.url,
            'x450':image.x450.url,
        },
    }

    return data
