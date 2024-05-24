from django.shortcuts import render

def index(request):
    """
    View function for home page of site.
    """
    # Generate a simple context to pass to the template rendering engine.
    context = {
        'title': 'Home Page',
        'heading': 'Welcome to the Todo Application',
    }
    
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'list/index.html', context=context)
