import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance
import webbrowser
import datetime
import wikipedia

# Opciones de vaz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id4 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0'

# escuchar nuestro microfono y devolver el audio como texto
def trasformarAudioEnTexto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    #configurar el miscrofono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio

        audio = r.listen(origen)

    try:
        # Buscarr en google
        pedido = r.recognize_google(audio, language='es-DO')

        # Pruebba de que pudo ingresar
        print("Dijiste: " + pedido)

        # Devolver pedido
        return pedido
    
    # En caso de que no comprenda el audio
    except sr.UnknownValueError:

        # Prueba de que no comprendio el audio
        print("ups, no entendi")

        # Devolver error
        return "Sigo esperando"
    
    # En caso de no resolver el pedido

    except sr.RequestError:

        # Prueba de que no comprendio el audio
        print("Ups, no hay servicio")

        # Devolver error
        return "Sigo esperando"
    
    # Error inesperado
    except:

        #prueba de que no comprendio el audio
        print("Ups, algo ha salido mal")

        # Devolver error
        return "Sigo esperando"
    
# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id3)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el dia de la semana
def pedirDia():

    # Crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de semana
    diaSemana = dia.weekday()
    print(diaSemana)

    # Diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miercoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sabado',
                  6: 'Domingo'}
    
    # Decir el dia de la semana
    hablar(f'Hoy es {calendario[diaSemana]}')

# Informar que hora es
def pedirHora():

    # Crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # Decir la hora
    hablar(hora)

# Funcion saludo inicial
def saludoInicial():
    
    # Crear variable condatos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen dia'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f"{momento}, soy Helena, tu asistente personal. Por favor, dime en que te puedo ayudar")

# Funcion central del asistente
def pedirCosas():

    #Activar saludo inicial
    saludoInicial()

    #Variable de corte
    comenzar = True

    #Loop central
    while comenzar:

        #Activar el micro y guardar el pedido en un string
        pedido = trasformarAudioEnTexto().lower()

        if 'abrir youtube' in pedido:
            hablar("Con gusto, estoy abrindo YouTube")
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'que día es hoy' in pedido:
            pedirDia()
            continue
        elif 'qué hora es' in pedido:
            pedirHora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace("Busca en wikipedia", '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice la siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yfinance.ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon pero no la he encontrado')
                continue
        elif 'adios' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break


pedirCosas()