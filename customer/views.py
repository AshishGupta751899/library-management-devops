from django.shortcuts import *
from customer.forms import Student_reg_form, Student_login_form, Student_update_form
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from customer.models import students_profile
from books.models import Rented_books


def student_reg(request):
    if request.method == 'POST':
        form = Student_reg_form(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='student')
            user.groups.add(group)
            # Auto-create profile on registration
            students_profile.objects.get_or_create(student=user)
            return redirect("user_login")
        else:
            print(form.errors)
            # ── FIX: re-render with errors ──
            return render(request, 'student_reg.html', {'form': form})
    else:
        form = Student_reg_form()
    return render(request, 'student_reg.html', {'form': form})


def student_profile(request):
    if request.user.is_authenticated:
        # get_or_create — never 404 crash
        student_pro, created = students_profile.objects.get_or_create(student=request.user)
        rented_books = Rented_books.objects.filter(user=request.user)
        context = {
            'student_pro': student_pro,
            'rented_books': rented_books,
        }
        return render(request, 'student_profile.html', context)
    else:
        return redirect('user_login')


def student_logout(request):
    logout(request)
    return redirect('all_books')


def student_profile_update(request):
    if request.user.is_authenticated:
        # get_or_create — safe even if profile row missing
        student_pro, created = students_profile.objects.get_or_create(student=request.user)

        if request.method == "POST":
            form = Student_update_form(request.POST, request.FILES, instance=student_pro)
            if form.is_valid():
                form.save()
                return redirect('student_profile')
            else:
                print(form.errors)
                # ── FIX: re-render with errors instead of HttpResponse ──
                return render(request, 'student_profile_update.html', {'form': form})
        else:
            form = Student_update_form(instance=student_pro)

        return render(request, 'student_profile_update.html', {'form': form})
    else:
        return redirect('user_login')


def all_students(request):
    student_group = Group.objects.get(name='student')
    students = User.objects.filter(groups=student_group)
    return render(request, 'all_students.html', {'students': students})