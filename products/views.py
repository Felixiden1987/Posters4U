from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def wishlist_view(request):
    """
    Display the user's wishlist.

    This view retrieves all products in the
    logged-in user's wishlist and
    displays them on the wishlist page.
    Each product in the wishlist is
    shown with its name, price,
    and image (if available).

    Arguments:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered template
        showing the user's wishlist.
    """
    wishlist_items = (
        Wishlist.objects.filter(user=request.user).
        select_related('product'))
    for item in wishlist_items:
        print(
            f"Product in wishlist: {item.product.name}, "
            f"Price: {item.product.price}, "
            f"Image URL:"
            f"{item.product.image.url if item.product.image else 'No Image'}"
        )
        print("wishlist_view items", wishlist_items)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'products/wishlist.html', context)


@login_required
def add_to_wishlist_view(request, product_id):
    """
    Add product to wishlist
    This view adds the specified product to the
    logged-in user's wishlist.
    If the product is already in the wishlist,
    an informational message is displayed.

    Arguments:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to
        add to the wishlist.

    Returns:
        HttpResponse: A redirect to the wishlist page
        after adding the product.
    """
    
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item, created = (
        Wishlist.objects.get_or_create(user=request.user, product=product)
    )
    print(wishlist_item)

    if created:
        messages.success(
            request,
            f"{product.name} has been added to your wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    # Redirect to the wishlist page
    return redirect(reverse('wishlist'))   # Redirect to the wishlist page


@login_required
def remove_from_wishlist_view(request, product_id):
    """Remove product from wishlist

    This view removes the specified product
    from the logged-in user's wishlist.
    If the product is not found in the wishlist,
    an informational message is shown.

    Arguments:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product to remove.
    Returns:
        HttpResponse: A redirect to the wishlist
        page after the removal action.
    """
    
    #  Get the product object (if it exists)
    product = get_object_or_404(Product, pk=product_id)

    #  Try to find the wishlist item for the
    #  logged-in user and the specific product
    wishlist_item = (
        Wishlist.objects.filter
        (user=request.user, product=product).first()
    )
    if wishlist_item:
        wishlist_item.delete()  # Remove the item from the wishlist
        messages.success(
            request,
            f"{product.name} has been removed from your wishlist.")
    else:
        messages.info(request, f"{product.name} is not in your wishlist.")

    # Redirect to the wishlist page after removing the item
    return redirect(reverse('wishlist'))