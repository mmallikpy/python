from netmiko import ConnectHandler
import speech_recognition as sr

# get audio from the microphone
listener = sr.Recognizer()

def voice_command():
    with sr.Microphone() as source:
        print('Give the cisco command : ')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        #print(command)
while True:

    try:
        with sr.Microphone() as source:
            print('Listening......')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if 'router' in command:
                print('SSH is starting........')
                '''
                cisco_devices = {
                    'device_type': 'cisco_ios',
                    'host': '172.16.201.12',
                    'username': 'mithun',
                    'password': '',
                    'port': 22,  # SSH port if you have custom port you can use it
                    'secret': '',  # Enable password
                }
                ssh = ConnectHandler(**cisco_devices)
                '''
                cisco_command = input('Give the command ', voice_command())
                print(cisco_command)
                #print(ssh.send_command('show ip int bri'))
            else:
                print('Command not found')

    except:
        pass
