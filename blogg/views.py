from django.shortcuts import render,redirect
from blogg.models import Blog
from django.contrib import messages

# Create your views here.

def home_page(request):
    try:
        search = request.GET.get('search')
        if search:
            query_blog= Blog.objects.filter(title= search)

        else:
            query_blog = Blog.objects.all()


        context={
            "query": query_blog,
        }
        return render(request, 'index.html', context=context)
    except Exception as e:
        messages.warning(request, f'{e}')
        return redirect('home')


def create_blog(request):
    try:
        if request.method =="POST":
            title= request.POST.get('title')
            description = request.POST.get('desc')
            image = request.FILES.get('image')
            
            Blog.objects.create(author=request.user, title=title, description= description, image= image)
            messages.success(request, f'Successfully post')
            return redirect('home')
    except Exception as e:
        messages.warning(request, f'{e}')

    return render(request, "create_blog.html")

def update_blog(request, id):
    try:
        blog= Blog.objects.get(id = id)
        if request.method =="POST":
            title= request.POST.get('title')
            description = request.POST.get('desc')
            image = request.FILES.get('image')
            if request.user == blog.author:
                blog.author = request.user
                blog.title= title
                blog.description = description
                if image:
                    blog.image = image
                
                blog.save()
                messages.success(request, f'Successfully Updated')
                return redirect('home')
            else:
                messages.warning(request, f'You didnt have access')
    except Exception as e:
        messages.warning(request, f'{e}')
    context ={

        "blogs": blog
    }
    return render(request, "update_blog.html", context=context)


def delete_blog(request, id):
    try:
        blog= Blog.objects.get(id = id)
        if request.user == blog.author:
            blog.delete()
            messages.success(request, f'Successfully Deleted ')
            return redirect('home')
        else:
            messages.warning(request, f'You didnt have access')
            return redirect('home')

    except Exception as e:
        messages.warning(request, f'{e}')
    
