from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Pelicula(models.Model):
    nombre = models.CharField(max_length=255)
    sinopsis = models.TextField()
    foto = models.ImageField(upload_to='peliculas')
    comentarios = models.ManyToManyField('Comentario', through='PeliculaComentario', related_name='pelicula_comentarios')

    def __str__(self): 
        return self.nombre


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='comentarios_pelis')
    cuerpo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username}: {self.cuerpo}'

    class Meta:
        ordering = ['-fecha_creacion']


class Puntuacion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='puntuaciones')
    puntuacion = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.pelicula.nombre}: {self.puntuacion}'


class PeliculaComentario(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)

class Avatar(models.Model):
    #vinculo con el perfil del usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #subcarpeta avatares
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True, default='blank.png')

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Avatares"
