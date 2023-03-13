from django.shortcuts import render, redirect,get_object_or_404
#Importacion de modelos
from AppBlog.models import Pelicula,Comentario,Avatar, Puntuacion
#Importacion de formularios
from .forms import MyUserCreationForm,UserEditForm,AvatarFormulario, ComentarioForm
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
# Q es una clase de Django que se utiliza para construir consultas complejas a través de filtros lógicos.
from django.db.models import Q

# Create your views here.
def handler404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def acerca_de_mi(request):
    return render(request,'AppBlog/acerca-de-mi.html')

@login_required
def inicio(request):
    return render(request,'AppBlog/inicio.html')

#CRUD DE PELICULA
class PeliculaList(LoginRequiredMixin,ListView):
    model = Pelicula
    template_name = 'AppBlog/peliculas-list.html'

class PeliculaDetalle(DetailView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-detalle.html'


    #get_context_data() de la superclase para obtener el contexto predeterminado, 
    # y luego agregar la lista de comentarios a ese contexto. 
    # Para obtener los comentarios, primero obtiene la película actual (self.object) y 
    # luego utiliza el atributo de relación inversa relacionada con el modelo de Comentario (comentarios_pelis) 
    # para obtener los comentarios asociados con la película. Luego, agrega la lista de comentarios al contexto con la clave 'comentarios', 
    # que puedes usar en tu plantilla para mostrar los comentarios asociados a la película.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pelicula = self.object
        comentarios = pelicula.comentarios_pelis.all()
        puntuaciones = pelicula.puntuaciones.all()
        puntajes = [p.puntuacion for p in puntuaciones]
        puntacion_promedio = sum(puntajes) / len(puntajes) if puntajes else None
        context['cantidad_puntajes'] = len(puntajes)
        context['puntuacion_promedio'] = puntacion_promedio
        context['comentarios'] = comentarios
        return context
    
    def post(self, request, *args, **kwargs):
        #Optenemos la pelicula actual
        pelicula = self.get_object()
        #obtenemos la puntuación del formulario utilizando 
        puntuacion = request.POST.get('puntuacion')
        if puntuacion:
            #crear una nueva Puntuacion o actualizar una existente
            Puntuacion.objects.update_or_create(
                pelicula=pelicula,
                usuario=request.user,
                defaults={'puntuacion': puntuacion},
            )
        return redirect('detalle', pk=pelicula.pk)

class PeliculaCreate(LoginRequiredMixin, CreateView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-nueva.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','sinopsis','foto']

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PeliculaUpdate(LoginRequiredMixin, UpdateView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-nueva.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','sinopsis','foto']

class PeliculaDelete(LoginRequiredMixin,DeleteView):
    model = Pelicula
    template_name = 'AppBlog/pelicula-eliminar.html'
    success_url = reverse_lazy('inicio')
    


@login_required
def buscar_peliculas(request):
    consulta = request.GET.get('q', '') # Obtiene el término de búsqueda
    peliculas = Pelicula.objects.filter(Q(nombre__icontains=consulta)) # Realiza la búsqueda de películas
    return render(request, 'AppBlog/buscar-peliculas.html', {'peliculas': peliculas, 'consulta': consulta})


#Crud Comentario
class ComentarioCreate(CreateView):
    model = Comentario
    template_name = 'AppBlog/comentario-nuevo.html'
    form_class = ComentarioForm

    def form_valid(self, form):
        pelicula_id = self.kwargs['pelicula_id']
        pelicula = Pelicula.objects.get(id=pelicula_id)
        comentario = form.save(commit=False)
        comentario.pelicula = pelicula
        comentario.usuario = self.request.user
        comentario.save()
        return super().form_valid(form)
    
    #get_success_url, se encarga de devolver la URL de redirección después de eliminar el comentario.
    #La variable pelicula_id se define utilizando el atributo self.object, que representa el objeto de comentario que se está eliminando.
    #Luego, usamos reverse_lazy para construir la URL de redirección y le pasamos el parámetro pk con el valor de pelicula_id.
    def get_success_url(self):
        pelicula_id = self.kwargs['pelicula_id']
        return reverse_lazy('detalle', kwargs={'pk': pelicula_id})


class ComentarioDelete(LoginRequiredMixin, DeleteView):
    model = Comentario
    
    #get_success_url, se encarga de devolver la URL de redirección después de eliminar el comentario.
    #La variable pelicula_id se define utilizando el atributo self.object, que representa el objeto de comentario que se está eliminando.
    #Luego, usamos reverse_lazy para construir la URL de redirección y le pasamos el parámetro pk con el valor de pelicula_id.
    def get_success_url(self):
        pelicula_id = self.object.pelicula_id
        return reverse_lazy('detalle', kwargs={'pk': pelicula_id})

def comentario_pelicula(request, pelicula_id):
    #get_object_or_404 es una función de utilidad proporcionada por el framework Django 
    #para recuperar un objeto de la base de datos o devolver una página de error 404 si el objeto no se encuentra.
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    comentarios = pelicula.comentarios.all().prefetch_related('usuario')
    if request.method == 'POST':
        mi_formulario = ComentarioForm(request.POST)
        if mi_formulario.is_valid():
            comentario = mi_formulario.save(commit=False)
            comentario.pelicula = pelicula
            comentario.usuario = request.user
            comentario.save()
            return redirect('detalle', pk=pelicula_id)
    else:
        mi_formulario = ComentarioForm()
        print(mi_formulario)
    
    return render(request, 'AppBlog/pelicula-detalle.html', {'pelicula': pelicula, 'comentarios': comentarios, 'mi_formulario': mi_formulario})

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

#Registro
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

    else:
        mi_formulario = AvatarFormulario(instance=avatar)
        return render(request, 'AppBlog/agregar-avatar.html',{'mi_formulario':mi_formulario})
