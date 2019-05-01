from django.http import JsonResponse
from django.shortcuts import render, redirect
from authentication.models import Customer, Admin
from authentication.user import User
from shop_app.models import Cart, Category, Product, ProductImages, CartItem
from django.contrib import messages


# Create your views here.

def home(request):
    categories = Category.objects.get_queryset().filter(mptt_level=0)
    products = Product.objects.all()
    return render(request, 'shop_app/page_home.html',
                  {'user_role': user_role(request), 'categories': categories, 'products': products})


def user_role(request):
    if (request.user.is_anonymous):
        return 'anonymous'
    else:
        try:
            Admin.objects.get(email=request.user.email)
            return 'admin'
        except User.DoesNotExist:
            return 'customer'


def page_not_found(request):
    return render(request, 'error/error404.html')


def user_profile(request):
    return render(request, 'shop_app/page_user_profile.html', {'user_role': user_role(request)})


def user_profile_edit(request):
    user_input = request.POST
    response_data = {}
    user = User.objects.get(email=request.user.email)
    user.first_name = user_input['first_name']
    user.last_name = user_input['last_name']
    user.phone = user_input['phone']
    user.save()
    response_data = {'response': 'success'}
    return JsonResponse(response_data)


def user_new_password(request):
    return render(request, 'shop_app/page_user_new_password.html', {'user_role': user_role(request)})


def user_change_password(request):
    user_input = request.POST
    user = User.objects.get(email=request.user.email)
    response_data = {}
    if (user.check_password(user_input['current_password'])):
        user.set_password(user_input['new_password'])
        user.save()
        response_data = {'response': 'success'}
    else:
        response_data = {'response': 'current_pass_inc'}
    return JsonResponse(response_data)


def user_cart(request):
    user = User.objects.get(email=request.user.email)
    Cart.objects.get_or_create(user=user)
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'shop_app/page_user_cart.html', {'user_role': user_role(request), 'cart_items': cart_items})


def new_category(request):
    role = user_role(request)
    if (role == 'admin'):
        categories = Category.objects.get_queryset()
        return render(request, 'shop_app/page_new_category.html',
                      {'user_role': role, 'categories': categories})
    else:
        return redirect(page_not_found)


def create_category(request):
    admin_input = request.POST
    category = Category.objects.get_queryset().filter(name=admin_input['category'])
    if (category.exists()):
        messages.error(request, 'This category already exists')
    else:
        if (admin_input['parent_category'] == 'not_parent'):
            Category.objects.create(name=admin_input['category'])
        else:
            parent = Category.objects.get(name=admin_input['parent_category'])
            Category.objects.create(name=admin_input['category'], parent=parent)
        messages.success(request, 'Category successfully created')
    return redirect(new_category)


def page_delete_category(request):
    role = user_role(request)
    if (role == 'admin'):
        categories = Category.objects.get_queryset()
        return render(request, 'shop_app/page_delete_category.html',
                      {'user_role': role, 'categories': categories})
    else:
        return redirect(page_not_found)


def delete_category(request):
    admin_input = request.POST
    category = Category.objects.get(name=admin_input['category'])
    category.delete()
    messages.success(request, 'Category successfully deleted')
    return redirect(new_category)


def new_product(request):
    role = user_role(request)
    if (role == 'admin'):
        categories = Category.objects.get_queryset()
        return render(request, 'shop_app/page_new_product.html', {'user_role': role, 'categories': categories})
    else:
        return redirect(page_not_found)


def create_product(request):
    admin_input = request.POST
    admin_files = request.FILES
    category = Category.objects.get(name=admin_input['category'])
    product = Product.objects.create(name=admin_input['product_name'], main_image=admin_files['title_image'],
                                     short_description=admin_input['product_short_description'],
                                     description=admin_input['product_description'], price=admin_input['product_price'],
                                     stock=admin_input['product_stock'], category=category)
    ProductImages.objects.create(product=product, image=request.FILES['detail_image_one'])
    ProductImages.objects.create(product=product, image=request.FILES['detail_image_two'])
    if ('detail_image_three' in admin_files):
        ProductImages.objects.create(product=product, image=request.FILES['detail_image_three'])
    if ('detail_image_four' in admin_files):
        ProductImages.objects.create(product=product, image=request.FILES['detail_image_four'])
    messages.success(request, 'Product successfully added')
    return redirect(new_product)


def product_detail(request, category_name, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.get_queryset().filter(mptt_level=0)
    all_categoriest = Category.objects.get_queryset()
    product_images = ProductImages.objects.filter(product=product)
    return render(request, 'shop_app/page_product_detail.html',
                  {'categories': categories, 'product': product, 'product_images': product_images,
                   'user_role': user_role(request), 'all_categoriest': all_categoriest})


def edit_product(request, id):
    role = user_role(request)
    if (role == 'admin'):
        product = Product.objects.get(id=id)
        categories = Category.objects.get_queryset()
        return render(request, 'shop_app/page_edit_product.html',
                      {'user_role': role, 'categories': categories, 'product': product})
    else:
        return redirect(page_not_found)


def update_product(request, id):
    user_input = request.POST
    files = request.FILES
    product = Product.objects.get(id=id)
    product.name = user_input['product_name']
    product.short_description = user_input['product_short_description']
    product.description = user_input['product_description']
    product.price = user_input['product_price']
    product.stock = user_input['product_stock']
    product.category = Category.objects.get(name=user_input['category'])
    if ('title_image' in files):
        product.main_image = request.FILES['title_image']
    product.save()
    messages.success(request, 'Product successfully updated')
    return redirect(edit_product, id)


def delete_product(request, id):
    role = user_role(request)
    if (role == 'admin'):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect(home)
    else:
        return redirect(page_not_found)


def edit_product_images(request, id):
    role = user_role(request)
    if (role == 'admin'):
        product = Product.objects.get(id=id)
        product_images = ProductImages.objects.filter(product=product)
        return render(request, 'shop_app/page_edit_product_images.html',
                      {'user_role': role, 'product': product,
                       'product_images': product_images})
    else:
        return redirect(page_not_found)


def update_product_images(request, image_id):
    product_image = ProductImages.objects.get(id=image_id)
    if ('image' in request.FILES):
        product_image.image = request.FILES['image']
        product_image.save()
        messages.success(request, 'Product image successfully updated')
    return redirect(edit_product_images, product_image.product.id)


def delete_product_images(request, image_id):
    product_image = ProductImages.objects.get(id=image_id)
    product_image.delete()
    messages.success(request, 'Product image successfully deleted')
    return redirect(edit_product_images, product_image.product.id)


def add_new_product_image(request, id):
    role = user_role(request)
    if (role == 'admin'):
        return render(request, 'shop_app/page_add_new_product_image.html', {'id': id})
    else:
        return redirect(page_not_found)


def create_new_product_image(request, id):
    product = Product.objects.get(id=id)
    if (ProductImages.objects.filter(product=product).count() == 5):
        messages.error(request, 'Sorry, but you have created the maximum number of images. Maximum: 5.')
    else:
        ProductImages.objects.create(image=request.FILES['image'], product=product)
        messages.success(request, 'New image successfully updated')
    return redirect(add_new_product_image, id)


def add_product_to_cart(request, id):
    response_data = {}
    user = User.objects.get(email=request.user.email)
    user.phone = request.POST['phone']
    user.save()
    Cart.objects.get_or_create(user=user)
    cart = Cart.objects.get(user=user)
    print(cart)
    product = Product.objects.get(id=id)
    quantity = float(request.POST['quantity'])
    CartItem.objects.create(cart=cart, product=product, quantity=float(quantity))
    cart.count += 1
    cart.save()
    response_data = {'response': 'success'}
    return JsonResponse(response_data)


def delete_product_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    messages.success(request, 'Product successfully deleted from cart')
    return redirect(user_cart)
