from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

handler404 = handler404
urlpatterns = [
    path('',PeliculaList.as_view(), name="inicio"), #Esta es nuestra primer vista
    path('detalle/<pk>', PeliculaDetalle.as_view(), name='detalle'),
    path('nuevo/',PeliculaCreate.as_view(),name="nuevo"), 
    path('editar/<pk>',PeliculaUpdate.as_view(),name="editar"),
    path('eliminar/<pk>',PeliculaDelete.as_view(),name="eliminar"),
    path('login/', login_request, name='login'),
    path('registro/',register,name="registro"),
    path('logout/',LogoutView.as_view(template_name="AppBlog/logout.html"),name="logout"),
    path('editar-perfil/',editar_perfil,name="editar-perfil"),
    path('agregar-avatar/',agregar_avatar,name='agregar-avatar'),
    #PATH RELACIONADOS A COMENTARIOS
    path('comentario/<int:pelicula_id>/', ComentarioCreate.as_view(), name='comentario'),
    path('comentario-eliminar/<pk>',ComentarioDelete.as_view(),name="comentario-eliminar"),
    #Acerca de mi
    path('acerca-de-mi/', acerca_de_mi, name='acerca-de-mi'),
    #Buscar pelicula
    path('buscar-peliculas/',buscar_peliculas,name='buscar_peliculas'),
    
]