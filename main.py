from pynput.keyboard import Key, Listener 
import datetime
import threading
import time
import ffmpeg
import os

#Mutex
lock_capture = threading.Lock() 

#Função responsável por upar o vídeo no drive
def upload_drive_video(source): 
    print("Upload!")

#Função responsável por editar o vídeo após baixar
def edit_video():
    print("Editing Video")
    try:
       stream = ffmpeg.input(
           url,
           rtsp_transport='tcp',
           listen_timeout=-1,
           t=15 
       )
       stream = ffmpeg.output(stream, 
                              source + start_time + '.mp4',
                              map='0:v',
                              acodec='copy',
                              vcodec='copy')
       ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
       print('stdout:', e.stdout.decode('utf8'))
       print('stderr:', e.stderr.decode('utf8'))

#Função responsável por capturar o vídeo do sistema das cameras
def capture_video(cameras, ido):
    #print("Quero Conquistar", ido) #Teste de Mutex
    agora = datetime.datetime.now()
    #Retirar os 10 minutos atrás na prática
    futuro = agora + datetime.timedelta(seconds = 2) - datetime.timedelta(minutes=10)
    passado = agora - datetime.timedelta(seconds = 19) - datetime.timedelta(minutes=10)
    #adicionar um sleep de 5 minutos
    #time.sleep(300) #300s = 5 minutos
    lock_capture.acquire()
    #print("Conquistei!", ido)  #Teste de Mutex
    start_time = str(passado.year) + str(passado.month).zfill(2) + str(passado.day).zfill(2) + "T" + str(passado.hour).zfill(2) + str(passado.minute).zfill(2) + str(passado.second).zfill(2)
    end_time = str(futuro.year) + str(futuro.month).zfill(2) + str(futuro.day).zfill(2) + "T" + str(futuro.hour).zfill(2) + str(futuro.minute).zfill(2) + str(futuro.second).zfill(2)
    server_ip = "192.168.2.108:554"
    username = "admin"
    password = "fred8808"
    url = "rtsp:/" + username + ":" + password + "@" + server_ip + "/ISAPI/streaming/tracks/" + str(cameras) + "?starttime=" + start_time + "Z&endtime=" + end_time + "Z"
    source = "tempfiles/" + start_time + "/" + str(cameras) + "/"
    if not os.path.exists(source):
       os.makedirs(source) 
    try:
       stream = ffmpeg.input(
           url,
           rtsp_transport='tcp',
           listen_timeout=-1,
           t=15 
       )
       stream = ffmpeg.output(stream, 
                              source + start_time + '.mp4',
                              map='0:v',
                              acodec='copy',
                              vcodec='copy')
       ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
       print('stdout:', e.stdout.decode('utf8'))
       print('stderr:', e.stderr.decode('utf8'))
    #print('Video salvo!', ido)  #Teste de Mutex
    lock_capture.release()
    #print('Mutex liberado!', ido)  #Teste de Mutex

#Função resposável por realizar a captura de vídeo da quadra society
def thread_capture_soccer(name):

    print("Thread Capture Soccer", name, " start")
    time.sleep(2)
    print("Thread ", name, " wakeup")

global ilo
def on_press(key):
        global ilo
        print('\nYou Entered {0}'.format( key))
        if key == Key.f7: 
            print("\n\nF7\n\n")
            x = threading.Thread(target=capture_video, args=(701,ilo))
            ilo+=1
            x.start()
        if key == Key.f8: 
            print("\n\nF7\n\n")
            #x = threading.Thread(target=thread_test, args=(2,))
            #x.start()

def on_release(key):
     if key == Key.esc:
         # Stop listener
         return False

# Collect events until released
ilo = 1
with Listener(on_press = on_press, on_release=on_release) as listener: 
    listener.join() 
# agora = datetime.datetime.now()
# futuro = agora + datetime.timedelta(seconds = 2)
# passado = agora - datetime.timedelta(seconds = 19)
# print("Passado: ", passado)
# print("Agora: ", agora)
# print("Futuro: ", futuro)
# start_time = str(passado.year) + str(passado.month).zfill(2) + str(passado.day).zfill(2) + "T" + str(passado.hour).zfill(2) + str(passado.minute).zfill(2) + str(passado.second).zfill(2)
# end_time = str(futuro.year) + str(futuro.month).zfill(2) + str(futuro.day).zfill(2) + "T" + str(futuro.hour).zfill(2) + str(futuro.minute).zfill(2) + str(futuro.second).zfill(2)
# print(start_time)
# print(end_time)