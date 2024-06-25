from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import soundcard as sc
import soundfile as sf
import speech_recognition as sr

# Audio recording settings
OUTPUT_FILE_NAME = "out.wav"
SAMPLE_RATE = 48000
RECORD_SEC = 20

# Path to chromedriver executable
chromedriver_path = 'F:\\Google meet automation\\chromedriver-win64\\chromedriver.exe'

# Function to log into Google account
def Glogin(mail_address, password):
    # Login Page
    driver.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

    # input Gmail
    driver.find_element(By.ID, "identifierId").send_keys(mail_address)
    driver.find_element(By.ID, "identifierNext").click()
    driver.implicitly_wait(10)

    # input Password
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    driver.implicitly_wait(10)
    driver.find_element(By.ID, "passwordNext").click()
    driver.implicitly_wait(10)

    # go to google home page
    driver.get('https://google.com/')
    driver.implicitly_wait(100)

# Function to turn off microphone and camera
def turnOffMicCam():
    # turn off Microphone
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div[26]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[7]/div[1]/div/div/div[1]').click()
    driver.implicitly_wait(3000)

    # turn off camera
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div[26]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[7]/div[2]/div/div[1]').click()
    driver.implicitly_wait(3000)

# Function to join Google Meet
def joinNow():
    # Join meet
    print("Successfully joined!")
    time.sleep(5)
    driver.implicitly_wait(1000)
    driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.jEvJdc.QJgqC').click()
    print(1)

# Assign email id and password
mail_address = 'neerajminproject'
password = 'neerajminproject@1'

# Create Chrome instance
opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=opt)

try:
    # Login to Google account
    Glogin(mail_address, password)

    # Go to Google Meet
    driver.get('https://meet.google.com/ird-uqzy-opx')
    
    # Turn off mic and camera
    turnOffMicCam()

    # Join Google Meet
    joinNow()

    # Start audio recording
    default_speaker = sc.default_speaker()
    with sc.get_microphone(id=str(default_speaker.name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        print("Recording audio from the default speaker...")
        
        # Record audio data from the default speaker
        data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)
        
        # If multiple channels are present and you only want one, use data[:, 0]
        sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)
        print(f"Finished recording. Audio saved to {OUTPUT_FILE_NAME}")

    # Wait for a while to stay in the meeting
    time.sleep(RECORD_SEC + 10)  # Ensure the script stays in the meeting for the duration of the recording plus some buffer time
finally:
    driver.quit()

# Convert recorded audio to text
recognizer = sr.Recognizer()

def convert_audio_to_text(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Converted Text:", text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

convert_audio_to_text(OUTPUT_FILE_NAME)
