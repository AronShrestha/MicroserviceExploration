from django.urls import path

from .views import ProductViewSet, UserAPIView

urlpatterns = [
     path('products', ProductViewSet.as_view({
         'get':'get_list',
         'post' :'create'
     })),
     path('products/<str:pk>', ProductViewSet.as_view(
         {
             'get':'retrive',
             'put':'update',
             'delete':'destroy'
         }
     )),
     path('user', UserAPIView.as_view())
]
