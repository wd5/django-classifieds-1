from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from zokiguide.decorators import render_to_json

from . models import ClassifiedsPost, ClassifiedsPostImages
from . forms import ImageUploadForm

@login_required
@render_to_json
def image_upload( request ):

    id = int( request.POST['post'] )

#    import logging
#    # Get an instance of a logger
#    logger = logging.getLogger()
#    logger.debug( request.POST['post'] )
#    logger.debug( id )



    try:
        post = ClassifiedsPost.objects.get( pk = id )
    except ClassifiedsPost.DoesNotExist:
        raise Http404

#    logger.debug( post )

    if request.method == "POST":
        form = ImageUploadForm( request.POST, request.FILES )
        if form.is_valid:
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
