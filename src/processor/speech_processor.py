"""
This module handles speech recognition functionality for the ISLify application.
"""

import speech_recognition as sr
from .image_processor import display_isl_gif, display_alphabet_images
from utils import load_supported_phrases

class SpeechRecognizer:
    """
    A class to handle speech recognition and processing.
    """

    def __init__(self):
        """
        Initialize the SpeechRecognizer with a recognizer object and supported phrases.
        """
        self.recognizer = sr.Recognizer()
        self.supported_phrases = load_supported_phrases()

    def process_speech(self, source):
        """
        Process speech input and convert it to ISL gestures or alphabet images.

        Args:
            source: The audio source (typically a microphone) to listen from.
        """
        self.calibrate_microphone(source)
        print("Microphone calibrated. Start speaking.")

        while True:
            try:
                audio = self.recognizer.listen(source)
                rec_audio = self.recognizer.recognize_google(audio).lower()
                print("You Said: " + rec_audio)

                if rec_audio in ["goodbye", "good bye", "bye"]:
                    print("Goodbye, see you next time!")
                    break
                elif rec_audio in self.supported_phrases:
                    display_isl_gif(rec_audio)
                else:
                    display_alphabet_images(rec_audio)
            except sr.UnknownValueError:
                print("Google Recognition could not understand audio. Please repeat.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Recognition service; {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def calibrate_microphone(self, source):
        """
        Calibrate the microphone for ambient noise.

        Args:
            source: The audio source (microphone) to calibrate.
        """
        print("Please wait. Calibrating microphone...")
        self.recognizer.adjust_for_ambient_noise(source, duration=5)
