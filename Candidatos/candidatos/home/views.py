from django.shortcuts import render
from home.models import Candidato, Noticia, Video, GaleriaImagenes, Compromiso
import urllib
import json

##### Inicio Terminado #######
def inicio(request):
	alcaldes = Candidato.objects.all().filter(tipo_candidato = 1)
	d_locales = Candidato.objects.all().filter(tipo_candidato = 2)
	d_federales = Candidato.objects.all().filter(tipo_candidato = 3)
	return render(request, 'index.html', { "alcaldes" : alcaldes, "d_locales" : d_locales, "d_federales" : d_federales })

#### Iniocio 2 Terminado ######
def inicio2(request):
	candidatos = Candidato.objects.all()
	return render(request, 'index0.html', { "candidatos" : candidatos })

#### candidato Terminado ######
def candidato(request, n_candidato):
	candidato = Candidato.objects.get(slug = n_candidato)

	try:
		noticia_destacada = Noticia.objects.get(candidato = candidato, destacada = True)
	except:
		noticia_destacada = Noticia.objects.all()[0]

	noticias = Noticia.objects.all().filter(candidato = candidato, destacada = False)[0:2]

	try:
		video = Video.objects.get(candidato = candidato, destacado = True)
		video = embed_video(video.url)
		galeria = None
	except:
		try:
			video = None
			galeria = GaleriaImagenes.objects.get(candidato = candidato, destacada = True)
		except:
			galeria = None

	return render(request, 'micrositio/home.html', { "candidato" : candidato, "noticia_destacada":noticia_destacada, "noticias":noticias, "video":video, "galeria":galeria })

#### perfil Terminado ##############
def perfil(request, n_candidato):
	candidato = Candidato.objects.get(slug = n_candidato)
	return render(request, 'micrositio/conoceme.html', {"candidato":candidato})

####### perfil Compromisos #################
def compromisos(request, n_candidato):
	candidato = Candidato.objects.get(slug = n_candidato)
	compromisos = Compromiso.objects.all().filter(candidato = candidato)
	return render(request, 'micrositio/compromisos.html', {"candidato":candidato, "compromisos":compromisos })

def galerias(request):
	return render(request, 'galerias.html')

def galeria(request):
	return render(request, 'galeria01.html')

###### noticias Terminado ##############
def noticias(request, n_candidato):
	candidato = Candidato.objects.get(slug = n_candidato)
	noticias = Noticia.objects.all().filter(candidato = candidato)
	return render(request, 'micrositio/noticias.html', { "candidato" : candidato, "noticias" : noticias })

def noticia(request, n_candidato, t_noticia):
	candidato = Candidato.objects.get(slug = n_candidato)
	noticia = Noticia.objects.get(slug = t_noticia, candidato = candidato)
	return render(request, 'micrositio/noti01.html', { "candidato":candidato, "noticia":noticia })

def videos(request):
	return render(request, 'videos.html')

def video(request):
	return render(request, 'video01.html')

################### HERRAMIENTAS #################3
def embed_video(url):	
	embed = 'http://www.youtube.com/oembed?url={0}&format=json'.format(url)
	sock = urllib.urlopen(embed)
	video = json.loads(sock.read())['html']	.replace('480', '390').replace('270', '275')
	sock.close()
	return video
