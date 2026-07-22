from django.shortcuts import *
from author.forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from author.models import Authors_profile
from books.models import All_books


def author_reg(request):
    if request.method == 'POST':
        form = Author_reg_form(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='author')
            user.groups.add(group)
            # Auto-create profile on registration
            Authors_profile.objects.get_or_create(author=user)
            return redirect("user_login")
        else:
            print(form.errors)
    else:
        form = Author_reg_form()
    return render(request, 'author_reg.html', {'form': form})


def author_profile(request):
    if request.user.is_authenticated:
        # get_or_create — never 404 crash
        author_pro, created = Authors_profile.objects.get_or_create(author=request.user)
        books = All_books.objects.filter(author=author_pro)
        context = {'author_pro': author_pro, 'books': books}
        return render(request, 'author_profile.html', context)
    else:
        return redirect('users')


def author_logout(request):
    logout(request)
    return redirect('all_books')


def author_profile_update(request):
    if request.user.is_authenticated:
        # get_or_create — safe even if profile row missing
        author_pro, created = Authors_profile.objects.get_or_create(author=request.user)

        if request.method == "POST":
            form = Author_update_form(request.POST, request.FILES, instance=author_pro)
            if form.is_valid():
                form.save()
                return redirect('author_profile')
            else:
                # ── FIX: re-render form with errors instead of HttpResponse ──
                print(form.errors)
                return render(request, 'author_profile_update.html', {'form': form})
        else:
            form = Author_update_form(instance=author_pro)

        return render(request, 'author_profile_update.html', {'form': form})
    else:
        return redirect('user_login')


def all_author(request):
    data = Authors_profile.objects.all()
    return render(request, 'all_author.html', {'data': data})