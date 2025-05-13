from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Count, Avg, F, Q
from .models import Category, Product, Comment, Reply, Rating, ProductView
from .forms import CommentForm, ReplyForm, RatingForm
from django.db.models.functions import Coalesce


def home(request):
    categories = Category.objects.all()
    filter_type = request.GET.get('filter', 'recent')
    products = Product.objects.filter(available=True)

    try:
        if filter_type == 'most_liked':
            products = products.annotate(like_count=Count('likes')).order_by('-like_count', '-created')[:8]
        elif filter_type == 'most_commented':
            products = products.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created')[:8]
        elif filter_type == 'highest_rated':
            products = products.annotate(avg_rating=Coalesce(Avg('ratings__rating'), 0.0)).order_by('-avg_rating', '-created')[:8]
        elif filter_type == 'most_viewed':
            products = products.order_by('-view_count', '-created')[:8]
        else:  # recent
            products = products.order_by('-created')[:8]
    except Exception as e:
        # Log the error for debugging (use logging in production)
        print(f"Error in filtering: {e}")
        products = products.order_by('-created')[:8]  # Fallback to recent

    context = {
        'products': products,
        'categories': categories,
        'current_filter': filter_type,
    }
    
    return render(request, 'shop/home.html', context)

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'products': products,
        'categories': categories
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    comments = product.comments.all()
    liked = False
    is_owner = False
    user_rating = None
    
    # Track unique views
    viewed = False
    
    if request.user.is_authenticated:
        # Check if authenticated user has viewed this product
        viewed = ProductView.objects.filter(product=product, user=request.user).exists()
        if not viewed:
            # Create new view record and increment counter
            ProductView.objects.create(product=product, user=request.user)
            product.view_count += 1
            product.save()
    else:
        # For anonymous users, use session key
        if not request.session.session_key:
            request.session.save()
        
        session_key = request.session.session_key
        viewed = ProductView.objects.filter(product=product, session_key=session_key).exists()
        
        if not viewed:
            # Create new view record and increment counter
            ProductView.objects.create(product=product, session_key=session_key)
            product.view_count += 1
            product.save()
    
    if request.user.is_authenticated:
        liked = product.likes.filter(id=request.user.id).exists()
        is_owner = product.owner == request.user
        # Check if user has already rated this product
        try:
            user_rating = Rating.objects.get(product=product, user=request.user)
        except Rating.DoesNotExist:
            user_rating = None
    
    # Handle comment form submission
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Izohingiz saqlandi')
            return redirect('product_detail', slug=product.slug)
    else:
        comment_form = CommentForm()
    
    # Handle rating form submission
    if request.user.is_authenticated and request.method == 'POST' and 'rating_submit' in request.POST:
        rating_value = request.POST.get('rating')
        if rating_value:
            # Create or update the rating
            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating_value}
            )
            messages.success(request, 'Baxoyingiz saqlandi')
            return redirect('product_detail', slug=product.slug)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
        'liked': liked,
        'is_owner': is_owner,
        'reply_form': ReplyForm(),
        'user_rating': user_rating,
        'categories': Category.objects.all(),
    })

@login_required
def like_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            liked = False
        else:
            product.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'total_likes': product.total_likes()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    product = comment.product
    
    # Only the product owner can reply to comments
    if request.user != product.owner:
        return HttpResponseForbidden("You don't have permission to reply to this comment.")
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            messages.success(request, 'Qayta javobingiz saqlandi')
    
    return redirect('product_detail', slug=product.slug)

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query, available=True) if query else []
    return render(request, 'shop/search_results.html', {'products': products, 'query': query})
