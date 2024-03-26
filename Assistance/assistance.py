# Trợ lý ảo
# Yêu cầu ban đầu với trợ lý là có thể nghe và trả lời bằng giọng nói
# Thêm lib
import pyttsx3
import speech_recognition as sr

# 1. Nghe là chuyển lời nói sang text để xử lý
# Quá trình nghe là quá trình thu lời nói vào Microphone sau đó recognizer âm thanh thu được thành text

# Khởi tạo recognizer(nhận-dạng)
r = sr.Recognizer()

# Bắt đầu nghe từ microphone
with sr.Microphone() as source:
    print("Đang lắng nghe: ")
    audio = r.listen(source)
    
# Sử dụng Google Speech Recognition để chuyển audio thành text
try:
    text = r.recognize_google(audio, language="vi-VN")
    print("Bạn đã nói: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition không hiểu được audio")
except sr.RequestError as e:
    print("Không thể yêu cầu kết quả từ Google Speech Recognition service; {0}".format(e))
    
# Sử dụng pyttsx3 để đọc văn bản
engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()


# 2. Nói là chuyển text thành lời nói trả lời.