# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.views.decorators.cache import cache_page

#from . import settings
from . models import ClassifiedsPost, ClassifiedsCategory, ClassifiedsPostImages
from . forms import ClassifiedsEditForm, ImageUploadForm
from common.utils import log


def get_categories():
    return ClassifiedsCategory.objects.get_query_set()

def get_posts( category = None, page = None ):
    posts = ClassifiedsPost.objects.filter( status = 'active' )

    if category:
        posts = posts.filter( category = category )

    paginator = Paginator( posts, 7 )

    try:
        posts = paginator.page( page )
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page( 1 )
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page( paginator.num_pages )

    return posts

def home( request, page = None, ):

    categories = get_categories()
    posts = get_posts( page = page )

    data = {
        'categories' : categories,
        'posts' : posts,
    }
    return render( request, 'classifieds/home.html', data )


def category( request, id, slug = None, page = None ):

    id = int( id )

    try:
        category = ClassifiedsCategory.objects.get( pk = id )
    except ClassifiedsCategory.DoesNotExist:
        raise Http404

    if category.slug() != slug:
        return redirect( 'classifieds-category', id = id, slug = category.slug(), permanent = True )

    categories = get_categories()
    posts = get_posts( category = category, page = page )

    data = {
        'category':category,
        'posts':posts,
        'categories':categories,
    }

    return render( request, 'classifieds/home.html', data )

@login_required
def add( request ):
    if request.session.get( 'classifieds-draft-id', '' ) and int( request.session['classifieds-draft-id'] ) > 0:
        return redirect( 'classifieds-edit', id = request.session['classifieds-draft-id'] )
    else:
        post = ClassifiedsPost( status = 'draft', author = User.objects.get( pk = request.user.id ) )
        post.save()
        request.session['classifieds-draft-id'] = post.id
        return redirect( 'classifieds-edit', id = post.id )

def post( request, id, slug = None ):
    id = int( id )

    try:
        post = ClassifiedsPost.objects.get( pk = id )
    except ClassifiedsPost.DoesNotExist:
        raise Http404

    if post.slug() != slug:
        return redirect( 'classifieds-post', id = id, slug = post.slug(), permanent = True )

    data = {
        'post':post,
        'categories':ClassifiedsCategory.objects.all(),
    }

    return render( request, 'classifieds/post.html', data )

@login_required
def edit( request, id ):

    id = int( id )

    try:
        post = ClassifiedsPost.objects.get( pk = id )
    except ClassifiedsPost.DoesNotExist:
        raise Http404

    images = ClassifiedsPostImages.objects.filter( post = post )

    form = ClassifiedsEditForm( instance = post )

    if request.method == "POST":
        form = ClassifiedsEditForm( request.POST, instance = post )
        if form.is_valid():
            form.save()
            post.status = 'active'
            post.save()

            del request.session['classifieds-draft-id']

            return redirect( 'classifieds-post', id = id )

    data = {
        'post':post,
        'form':form,
        'image_upload_form':ImageUploadForm( initial = {'post':post} ),
        'images':images,
    }
    return render( request, 'classifieds/edit.html', data )
