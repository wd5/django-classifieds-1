from django.db import models
from django.conf import settings

import uuid

from smart_selects.db_fields import ChainedForeignKey

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust, SmartResize, ResizeToFit

from common.models import CommonCategory, CommonPost, CommonPostImage
from location.models import Country, City

# Create your models here.

#META_CHOICE = (
#    ( 'email', 'email' ),
#    ( 'phone', 'phone' ),
#    ( 'skype', 'skype' ),
#    ( 'facebook', 'facebook' ),
#
# )

def image_upload_to( instance, filename ):
    ext = filename.split( '.' )[-1]
    filename = "%s.%s" % ( uuid.uuid4(), ext.lower() )
    id = str( instance.post.id )
    return 'classifieds/%s/%s/%s' % ( id[:1], id, filename )

class ClassifiedsCategory( CommonCategory ):
    pass

class ClassifiedsPost( CommonPost ):
    category = models.ManyToManyField( 
        ClassifiedsCategory,
        related_name = "%(app_label)s_%(class)s_related",
    )
    country = models.ForeignKey( 
        Country,
        null = True,
        related_name = "%(app_label)s_%(class)s_related",
    )
    city = ChainedForeignKey( 
        City,
        chained_field = "country",
        chained_model_field = "country",
        show_all = False,
        auto_choose = False,
        related_name = "%(app_label)s_%(class)s_related",
    )
    site = models.URLField( 
        blank = True,
        verbose_name = u'Site URL',
        help_text = u'your web site full URL',
    )
    is_featured = models.BooleanField( default = 0 )
    featured_untill = models.DateTimeField( blank = True )
    email = models.EmailField( blank = True )
    phone = models.CharField( max_length = 30, blank = True )
    skype = models.CharField( max_length = 30, blank = True )
    address = models.TextField( blank = True )
    twitter = models.URLField( 
        blank = True,
        help_text = u'full URL to your account with http://',
    )
    facebook = models.URLField( 
        blank = True,
        help_text = u'full URL to your account with http://',
    )
    google_plus = models.URLField( 
        blank = True,
        help_text = u'full URL to your account with http://',
    )


#class ClassifiedsPostMeta( models.Model ):
#    post = models.ForeignKey( ClassifiedsPost, blank = True, null = True, )
#    key = models.CharField( max_length = 25, choices = META_CHOICE )
#    value = models.TextField()

class ClassifiedsPostImages( CommonPostImage ):
    post = models.ForeignKey( 
        ClassifiedsPost,
        default = '',
        blank = True,
        null = True,
        related_name = "%(app_label)s_%(class)s_related",
    )
    image = models.ImageField( upload_to = image_upload_to )
