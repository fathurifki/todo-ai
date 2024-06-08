from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Todo
from django.db import connection
from django.http import QueryDict
from .forms import TodoForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    """
    View function for home page of site.
    """
    # Generate a simple context to pass to the template rendering engine.
    context = {
        'title': 'Home Page',
        'heading': 'Welcome to the Todo Application',
    }
    
    return render(request, 'list/index.html', context=context)

@login_required
def create_todo(request):
    user_id = request.user.user_id
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO todo (title, description, user_id, accomplished) VALUES (%s, %s, %s, %s)", [title, description, user_id, False])
        return render_todo_list(request)


@login_required
def todo_list(request):
    user_id = request.user.user_id
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT todo_id, title, description, accomplished FROM todo WHERE user_id = %s", [user_id])
            todos = cursor.fetchall()
            todos_list = [{'id': todo[0], 'title': todo[1], 'description': todo[2], 'accomplished': todo[3]} for todo in todos]
            return render(request, 'list/index.html', {'todos': todos_list})
    else:    
        return render(request, 'list/index.html')

@login_required
def get_detail_todo(request, todo_id):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT todo_id, title, description, accomplished FROM todo WHERE todo_id = %s", [todo_id])
            todo = cursor.fetchone()
            todo_detail = {'id': todo[0], 'title': todo[1], 'description': todo[2], 'accomplished': todo[3]}
    return render(request, 'list/partials/edit_todo.html', {'todo': todo_detail})

@login_required
def edit_todo(request, todo_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE todo SET title = %s, description = %s WHERE todo_id = %s", [title, description, todo_id])
        return render_todo_list(request)
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT todo_id, title, description, accomplished FROM todo WHERE todo_id = %s", [todo_id])
            todo = cursor.fetchone()
            todo_detail = {'id': todo[0], 'title': todo[1], 'description': todo[2], 'accomplished': todo[3]}
            return render(request, 'list/partials/edit_todo.html', {'todo': todo_detail})

@login_required    
def delete_todo(request, todo_id):
    if request.method == 'DELETE':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM todo WHERE todo_id = %s", [todo_id])
        return render_todo_list(request)
    return HttpResponse(status=405)

@login_required
def render_todo_list(request):
    user_id = request.user.user_id
    with connection.cursor() as cursor:
        cursor.execute("SELECT todo_id, title, description, accomplished FROM todo WHERE user_id = %s", [user_id])
        todos = cursor.fetchall()
        todos_list = [{'id': todo[0], 'title': todo[1], 'description': todo[2], 'accomplished': todo[3]} for todo in todos]
    return render(request, 'list/partials/list_todo.html', {'todos': todos_list})

@login_required
def accomplished_task(request, todo_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("UPDATE todo SET accomplished = %s WHERE todo_id = %s", [True, todo_id])
        return render_todo_list(request)
    return HttpResponse(status=405)
