from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from blog.models import Post, Comment
from blog.forms import AuthForm, PostForm, CommentForm

from django.utils import timezone

from .model.nlp_model import is_offensive

'''
 The following functions are named views in Django.
 A view is executed when a client hits a certain URL pattern (specified in the urls.py file).
 A view can accept different HTTP request methods, but the ones used here are GET and POST.
'''

# GET '/'
def indexView(request):
    # get the posts in descending order based on publication date
    post_list = Post.objects.order_by('-pub_date')
    
    is_logged_in = request.user.is_authenticated
    context = {
        'post_list': post_list,
        'is_logged_in': is_logged_in
    }

    if is_logged_in:
        context['user'] = request.user

    return render(request, 'blog/index.html', context)


# POSTS

# GET, POST '/post/'
@login_required
def createPost(request):
    if request.method == 'POST':
        # get the results from the form
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            if is_offensive(request.POST['content']):
                context = {
                    'form': form,
                    'is_logged_in': request.user.is_authenticated,
                    'error': 'Offensive language is prohibited !'
                }

                return render(request, 'blog/create.html', context)

            # to save the post to the db it is needed to add extra fields
            # in order to do so, we're saving the current data in post
            post = form.save(commit=False)
            
            post.author = request.user
            post.pub_date = timezone.now()

            post.save()

            # after saving the post, go to it's page
            return postDetailView(request, post.id)      
    else: # method == 'GET'
        # create the form to be displayied to the user
        form = PostForm()

    context = {
        'form': form,
        'is_logged_in': request.user.is_authenticated
    }

    return render(request, 'blog/create.html', context)

# GET '/post/[id]/'
def postDetailView(request, post_id, error=None, comment_form=None):
    # get the desired post from the db
    post = Post.objects.get(pk=post_id)

    # get the post's comments
    comments = Comment.objects.filter(post=post_id)

    context = {
        'post': post,
        'comments': comments,
        'is_logged_in': request.user.is_authenticated,
        'post_id': post_id
    }

    # if an error appeared, add it to the context to be able to display it
    if error:
        context['error'] = error

    # create a form for adding comments
    form = CommentForm()

    # if a comment form was submitted (coming from the createComment view) then take it to the context
    if comment_form:
        form = comment_form

    context['comment_form'] = form
    
    return render(request, 'blog/detail.html', context)

# POST '/post/[post_id]/delete'
@login_required
def deletePostView(request, post_id):
    if request.method == 'POST':
        # get the post from the db
        post = Post.objects.get(pk=post_id)

        # if the client is not the author of the post display an error on the post's page
        if post.author != request.user:
            return postDetailView(request=request, post_id=post_id, error='This is not your post. You cannot delete it !')

        post.delete()

        # redirect to the home page
        return redirect('/')
    else:
        return postDetailView(request=request, post_id=post_id, error=f'Incorrect method ! (cannot GET at post/{post_id}/delete')


# COMMENTS

# POST '/comment/'
@login_required
def createCommentView(request):
    # get the id of the post
    post_id = request.POST['post_id']

    if request.method == 'POST':
        # create a form and populate it with the request body
        form = CommentForm(request.POST)

        # if form.is_valid() and not is_offensive(request.POST['content']):
        if form.is_valid():
            if is_offensive(request.POST['content']):
                return postDetailView(request=request, post_id=post_id, error='Offensive language is prohibited !')

            # create an instance of the comment with the data form the form
            comment = form.save(commit=False)

            # add new attributes to it
            comment.author = request.user
            comment.post = Post.objects.get(pk=post_id)
            comment.pub_date = timezone.now()
            
            # save the comment
            comment.save()

            # redirect to the post's page
            return redirect(f'/post/{post_id}')
        else:
            # if the form is not valid call the postDetailView to display the form's errors
            return postDetailView(request=request, post_id=post_id, comment_form=form)
    else:
        # if received a request other than POST, display an error at the post's page
        return postDetailView(request=request, post_id=post_id, error='Incorrect method ! (cannot GET at \'/comment/)\'')

# POST '/comment/delete'
@login_required
def deleteCommentView(request):
    # get the id of the post
    post_id = request.POST['post_id']

    if request.method == 'POST':
        # find the comment to be deleted in the db
        comment = Comment.objects.get(pk=request.POST['comment_id'])

        # if the client is the author of the comment then delete it and redirect to the post's page
        if comment.author == request.user:
            comment.delete()

            return redirect(f'/post/{post_id}')
        else:
            # if the client attempted to delete a comment not of his own, then display an error at the post's page
            return postDetailView(request=request, post_id=post_id, error='This is not you comment. You cannot delete it !')
    else:
        # if the received request is other than a POST, display an error at the post's page
        return postDetailView(request=request, post_id=post_id, error='Incorrect method ! (cannot GET at \'/comment/delete/\'')


# PROFILE

# GET '/profile/[user_id]/'
@login_required
def profileView(request, user_id):
    if request.method == 'GET':
        # get the user id from the session
        user = request.user

        # check if the user id from the URL is the same as the one from the session and redirect to home page if these don't match
        if user.id != user_id:
            return redirect('/')
        
        # get the user's posts
        posts = Post.objects.filter(author=user)

        is_logged_in = request.user.is_authenticated

        # display the profile page
        return render(request, 'blog/profile.html', {
            'username': user.username,
            'posts': posts,
            'date_joined': user.date_joined,
            'id': user_id,
            'is_logged_in': is_logged_in
        })
    else:
        # if the method is not GET redirect to the home page
        return redirect('/')

# POST '/profile/[user_id]/delete'
@login_required
def profileDeleteView(request, user_id):
    if request.method == 'POST':
        # get the user id from the session
        user = request.user

        # check if the user id from the URL is the same as the one from the session and delete the user if so
        if user.id == user_id:
            # delete the user
            User.objects.get(pk=user_id).delete()

    return redirect('/')


# AUTH

# POST '/signup/', GET '/signup/'
def signupView(request):
    if request.method == 'POST':
        # create a form for authenticating and populate it with the request body
        form = AuthForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            # if a user with this username already exists then display an error
            if User.objects.filter(username=username).exists():
                return render(request, 'blog/auth.html', {
                    'error': 'A user with this username already exists',
                    'form': form,
                    'auth_type': 'signup' # a variable to indicate auth.html to display the signup page instead of the login page
                })
            
            # add the user to the db
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # log in the user
            login(request, user)

            # redirect to the home page
            return redirect('/')
    else:
        # for a GET request display an authentication form
        form = AuthForm()

    return render(request, 'blog/auth.html', {
        'form': form,
        'auth_type': 'signup' # a variable to indicate auth.html to display the signup page instead of the login page
    })

# POST '/login/'
def loginView(request):
    if request.method == 'POST':
        # create a form for logging in and populate it with the request body
        form = AuthForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            # authenticate the user
            user = authenticate(username=username, password=password)

            # if authentication is succesfull, then log in the user and redirect to the home page
            # otherwise display an error at the login page
            if user is not None:
                login(request, user)

                return redirect('/')
            else:
                return render(request, 'blog/auth.html', {
                    'error': 'Incorrect username or password',
                    'form': form,
                    'auth_type': 'login' # a variable to indicate auth.html to display the login page instead of the signup page
                })
    else:
        # for a GET request display an authentication form
        form = AuthForm()

    return render(request, 'blog/auth.html', {
            'form': form,
            'auth_type': 'login' # a variable to indicate auth.html to display the login page instead of the signup page
        })

# GET '/logout/'
@login_required
def logoutView(request):
    logout(request)

    return redirect('/')
