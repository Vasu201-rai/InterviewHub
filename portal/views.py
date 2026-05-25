from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Bookmark
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html')

def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            
            messages.error(request,'Username already exists!')
            
            return redirect('/signup/')

    

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/login/')

    return render(request, 'signup.html')

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print(user)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Question


@login_required
def add_question(request):

    # 🔒 Only Admin Can Access
    if not request.user.is_superuser:
        return HttpResponseForbidden("403 Forbidden")

    if request.method == "POST":

        title = request.POST.get('title')
        answer = request.POST.get('answer')
        category = request.POST.get('category')

        # Save Question
        Question.objects.create(
            
            title=title,
            answer=answer,
            category=category
        )

        messages.success(request, "Question Added Successfully ✅")

        return redirect('/dashboard/')

    return render(request, 'add_question.html')

def logout_view(request):

    logout(request)

    return redirect('/login/')

from django.core.paginator import Paginator

@login_required
def dashboard(request):

    search = request.GET.get('search')
    category = request.GET.get('category')
    
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).values_list('question_id', flat=True)

    questions = Question.objects.all()

    if search:
        questions = questions.filter(title__icontains=search)

    if category:
        questions = questions.filter(category=category)

    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'questions': questions,
        'total': Question.objects.count(),
        'python_count': Question.objects.filter(category="Python").count(),
        'sql_count': Question.objects.filter(category="SQL").count(),
        'django_count': Question.objects.filter(category="Django").count(),
        'web_count': Question.objects.filter(category="Web").count(),
        'bookmarks': bookmarks
    })

       
@login_required
def edit_question(request, id):

    question = Question.objects.get(
    id=id,
    user=request.user
)

    if request.method == 'POST':

        question.category = request.POST.get('category')

        question.title = request.POST.get('title')

        question.answer = request.POST.get('answer')

        question.save()
        
        messages.success(request,'Question updated successfully!')

        return redirect('/dashboard/')

    return render(request, 'edit_question.html', {
        'question': question
    })
    
@login_required
def delete_question(request, id):

    question = Question.objects.get(
    id=id,
    user=request.user
)

    question.delete()
    
    messages.success(request,'Question deleted successfully!')

    return redirect('/dashboard/')


@login_required
def toggle_bookmark(request, id):

    question = Question.objects.get(id=id)

    bookmark = Bookmark.objects.filter(
        user=request.user,
        question=question
    )

    if bookmark.exists():

        bookmark.delete()

    else:

        Bookmark.objects.create(
            user=request.user,
            question=question
        )

    return redirect('/dashboard/')

@login_required
def bookmarked_questions(request):

    bookmarks = Bookmark.objects.filter(
        user=request.user
    )

    return render(request, 'bookmarks.html', {
        'bookmarks': bookmarks
    })
    
@login_required
def question_detail(request, id):

    question = Question.objects.get(id=id)

    return render(request, 'question_detail.html', {
        'question': question
    })