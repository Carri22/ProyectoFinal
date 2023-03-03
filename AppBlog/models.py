from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pelicula(models.Model):
    nombre = models.CharField(max_length=255)
    sinopsis = models.TextField()
    foto = models.ImageField(upload_to='peliculas')
    puntacion = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor} en {self.pelicula.nombre}'

class Avatar(models.Model):
    #vinculo con el perfil del usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #subcarpeta avatares
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True, default='blank.png')

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Avatares"