from django.urls import path, include
from LittlelemonAPI import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('', views.home),
    # path('menu-item/' , views.MenuItemsView.as_view()),
    # path('menu-item/<int:pk>' , views.SingleMenuItemView.as_view()),
    # path('menu-category/' , views.MenuCategoryView.as_view()),
    # path('menu-category/<int:pk>' , views.MenuCategoryView.as_view())
    path('menu-item/' , views.menuitems),
    path('secret/' , views.secret),
    path('obtain-token-auth/' , obtain_auth_token),
    path('manager-view/' , views.managerview),
    path("throttle/" , views.throttle),
    path('logged/' , views.loggedusers)
    # path('menu-item/<int:pk>', views.singleItem)
]
