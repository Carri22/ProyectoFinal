from django.shortcuts import render, redirect
#Importacion de modelos
from AppBlog.models import Pelicula,Comentario,Avatar
#Importacion de formularios
from .forms import MyUserCreationForm,UserEditForm,AvatarFormulario
#Importacion de vista lista
from django.views.generic import ListView
#Importacion de la vista detalles
from django.views.generic.detail import DetailView
#Importacion de las vistas, crear,editar y eliminar
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#Importacion para el login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from  django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
#Importaciones para el mixins
from django.contrib.auth.mixins import LoginRequiredMixin
#Importaciones para los decoradores 
from django.contrib.auth.decorators import login_required
#Importacion de reverse_lazy
from django.urls import  reverse_lazy

# Create your views here.
def inicio(request):
    return render(request,'AppCoder/inicio.html')

#CRUD DE PELICULA
class PeliculaList(LoginRequiredMixin,ListView):
    model = Pelicula
    template_name = 'AppBlog/peliculas-list.html'

class PeliculaDetalle(DetailView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-detalle.html'

class PeliculaCreate(LoginRequiredMixin, CreateView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-nueva.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','sinopsis','foto','puntacion']

class PeliculaUpdate(LoginRequiredMixin, UpdateView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-nueva.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','sinopsis','foto','puntacion']

class PeliculaDelete(LoginRequiredMixin,DeleteView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-eliminar.html'
    success_url = reverse_lazy('inicio')



#Vistas del login
def login_request(request):
    form = AuthenticationForm()

    if request.method == "POST":
        #Creacion del formulario con los datos resividos desde la vista
        form = AuthenticationForm(request, data=request.POST)

        #Validar si los datos del formulario sean validaos
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')

            user = authenticate(username = usuario, password=contraseña)

            if user is not None:
                login(request, user)
                contexto = {'mensaje': f'Bienvenido {usuario}'}
                return render(request, 'AppBlog/inicio.html', contexto)
            else:
                contexto = {'mensaje': f'El usuario no existe','form': form}
                return render(request, 'AppBlog/login.html', contexto)
            
        else:
            contexto = {'mensaje': f'Los datos del formulario son erroneos','form': form}
            return render(request, 'AppBlog/login.html', contexto)
        
    contexto = {'form':form}
    return render(request, 'AppBlog/login.html',contexto)

def register(request):
    
    if request.method == "POST":
        
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    else:
        form = MyUserCreationForm()
    return render(request, 'AppBlog/registro.html', {'form': form})


@login_required
def editar_perfil(request):
    usuario = User.objects.get(username=request.user)

    if request.method == 'POST':
        mi_formulario = UserEditForm(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data

            usuario.username = informacion["username"]
            usuario.email = informacion["email"]
            # usuario.password = informacion["password"]
            # usuario.password2 = informacion["password2"]
            usuario.last_name = informacion["last_name"]
            usuario.first_name = informacion["first_name"]

            usuario.save()
            return redirect('/')

    else:        
        mi_formulario = UserEditForm(initial={"username":usuario.username,
                                            "email":usuario.email,
                                            "last_name":usuario.last_name,
                                            "first_name":usuario.first_name})
        contexto = {'mi_formulario': mi_formulario}
        return render(request,'AppBlog/editar-perfil.html',contexto)

@login_required
def agregar_avatar(request):
    try:
        avatar = request.user.avatar
    except Avatar.DoesNotExist:
        avatar = None

    if request.method == 'POST':
        mi_formulario = AvatarFormulario(request.POST, request.FILES, instance=avatar)
        if mi_formulario.is_valid():
            nuevo_avatar = mi_formulario.save(commit=False)
            nuevo_avatar.user = request.user
            nuevo_avatar.save()
            return redirect('/')
    else:
        mi_formulario = AvatarFormulario(instance=avatar)
        return render(request, 'AppBlog/agregar-avatar.html',{'mi_formulario':mi_formulario})
