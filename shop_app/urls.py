from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    url('^$', views.home, name='home'),
    path('page_not_found/', views.page_not_found, name='page_not_found'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('new_category/', views.new_category, name='new_category'),
    path('create_category/', views.create_category, name='create_category'),
    path('page_delete_category/', views.page_delete_category, name='page_delete_category'),
    path('delete_category/', views.delete_category, name='delete_category'),
    path('new_product/', views.new_product, name='new_product'),
    path('create_product/', views.create_product, name='create_product'),
    path('Products/<str:category_name>/<int:product_id>/', views.product_detail, name='product_detail'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile_edit/', views.user_profile_edit, name='user_profile_edit'),
    path('user_new_password/', views.user_new_password, name='user_new_password'),
    path('user_change_password/', views.user_change_password, name='user_change_password'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('edit_product_images/<int:id>/', views.edit_product_images, name='edit_product_images'),
    path('delete_product_images/<int:image_id>/', views.delete_product_images, name='delete_product_images'),
    path('update_product_images/<int:image_id>/', views.update_product_images, name='update_product_images'),
    path('add_new_product_image/<int:id>/', views.add_new_product_image, name='add_new_product_image'),
    path('create_new_product_image/<int:id>/', views.create_new_product_image, name='create_new_product_image'),
    path('add_product_to_cart/<int:id>/', views.add_product_to_cart, name='add_product_to_cart'),
    path('delete_product_from_cart/<int:id>/', views.delete_product_from_cart, name='delete_product_from_cart'),



    # path(r'^categories/(?P<category_url>[\w\d_/-]+)/$', 'categories.views.show_page'),
]
