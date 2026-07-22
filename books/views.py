from django.shortcuts import *
from books.forms import Create_book_form, Update_book_form, Payment_form
from author.models import Authors_profile
from books.models import All_books, Rented_books
import razorpay
from django.conf import settings

def create_books(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if request.method == "POST":
        form = Create_book_form(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            author_pro, created = Authors_profile.objects.get_or_create(author=request.user)
            book.author = author_pro
            book.save()
            return redirect('author_profile')
        else:
            print(form.errors)
            return render(request, 'create_book.html', {'form': form})
    else:
        form = Create_book_form()
    return render(request, 'create_book.html', {'form': form})


def read_books(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    books = get_object_or_404(All_books, pk=id)

    # ── Author check ──
    is_author = False
    try:
        author_pro = Authors_profile.objects.get(author=request.user)
        is_author = (books.author == author_pro)
    except Authors_profile.DoesNotExist:
        is_author = False

    # ── Rent check — kya student ne yeh book rent ki hai? ──
    has_rented = Rented_books.objects.filter(
        book=books,
        user=request.user
    ).exists()

    # ── Preview: sirf pehle 100 words ──
    full_content    = books.book_content or ''
    words           = full_content.split()
    preview_content = ' '.join(words[:100]) + (' ...' if len(words) > 100 else '')

    # Author ko hamesha full, student ko rent karne ke baad full
    show_full = is_author or has_rented

    return render(request, 'read_books.html', {
        'books'          : books,
        'is_author'      : is_author,
        'has_rented'     : has_rented,
        'show_full'      : show_full,
        'preview_content': preview_content,
    })


def update_books(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    books = get_object_or_404(All_books, pk=id)

    # ── Only the book's author can update ──
    try:
        author_pro = Authors_profile.objects.get(author=request.user)
        if books.author != author_pro:
            return render(request, '403.html', status=403)
    except Authors_profile.DoesNotExist:
        return render(request, '403.html', status=403)

    if request.method == "POST":
        form = Update_book_form(request.POST, instance=books)
        if form.is_valid():
            form.save()
            return redirect('author_profile')
        else:
            print(form.errors)
            return render(request, 'update_books.html', {'form': form, 'books': books})
    else:
        form = Update_book_form(instance=books)

    return render(request, 'update_books.html', {'form': form, 'books': books})


def all_books(request):
    books = All_books.objects.all()
    return render(request, 'total_books.html', {'books': books})


def delete_books(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    books = get_object_or_404(All_books, pk=id)

    # ── Only the book's author can delete ──
    try:
        author_pro = Authors_profile.objects.get(author=request.user)
        if books.author != author_pro:
            return render(request, '403.html', status=403)
    except Authors_profile.DoesNotExist:
        return render(request, '403.html', status=403)

    books.delete()
    return redirect('author_profile')


def rent_book(request, id):
    book = get_object_or_404(All_books, pk=id)

    if not book.is_available:
        return render(request, 'book_unavailable.html', {'book': book})

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    if request.method == "POST":
        # ── Payment verification ──
        payment_id  = request.POST.get('razorpay_payment_id')
        order_id    = request.POST.get('razorpay_order_id')
        signature   = request.POST.get('razorpay_signature')
        return_date = request.POST.get('return_date')
        amount      = request.POST.get('amount')

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id'   : order_id,
                'razorpay_payment_id' : payment_id,
                'razorpay_signature'  : signature,
            })
            # Payment verified ✅
            book.is_available = False
            book.save()
            Rented_books.objects.create(
                book=book,
                user=request.user,
                return_at=return_date,
                amount_paid=amount,
            )
            return redirect('student_profile')

        except Exception:
            return render(request, 'payment_page.html', {
                'book': book,
                'error': 'Payment verification failed. Try again.'
            })

    else:
        # ── Create Razorpay order ──
        amount_paise = int(book.book_price * 100)  # Razorpay paisa mein leta hai
        order = client.order.create({
        'amount'  : amount_paise,
        'currency': 'INR',
        'payment_capture': '1',  # string mein do
        })
        return render(request, 'payment_page.html', {
            'book'       : book,
            'order'      : order,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount_paise': amount_paise,
        })