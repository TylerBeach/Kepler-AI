import speech_recognition as sr
import pyttsx3 as t

print("starting up..")

r = sr.Recognizer()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
               
                audio2 = r.listen(source2)
                
                MyText = r.recognize_google(audio2)
               
                return MyText
            
            
        except sr.RequestError as e:
            print("Error processing")
            
        except sr.UnknownValueError as e:
            print("Unknown error occured")
        
        
    
def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return


while(1):
    text = record_text()
    if text == 'exit':
        print("Exiting...")
        break
    output_text(text)
    print(text)

    

    