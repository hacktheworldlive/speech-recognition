import speech_recognition as sr
import os
import time

# Initialize the recognizer
recognizer = sr.Recognizer()

def recognize_speech_from_mic(recognizer, microphone):
    """
    Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether the API request was successful,
    "error": `None` if no error occurred, or a string containing
             an error message if the API could not be reached or
             speech was unrecognizable,
    "transcription": `None` if speech could not be transcribed,
                     or a string containing the transcribed text.
    """
    # Check if recognizer and microphone arguments are of correct type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # Adjust the recognizer sensitivity to ambient noise and record audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    # Initialize the response dictionary
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        # Recognize speech using Google Speech Recognition
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # Speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def perform_action_based_on_keyword(transcription):
    """
    Perform actions based on specific keywords in the transcription.
    """
    if "hello" in transcription.lower():
        print("Hello! How can I assist you today?")
    elif "open notepad" in transcription.lower():
        print("Opening Notepad...")
        os.system("notepad")
    elif "what is your name" in transcription.lower():
        print("I'm your speech detection assistant.")
    elif "time" in transcription.lower():
        print("The current time is: " + time.strftime("%I:%M %p"))
    else:
        print("No specific action assigned for: ", transcription)

if __name__ == "__main__":
    # Create a microphone instance
    microphone = sr.Microphone()

    while True:
        # Call the recognize_speech_from_mic function and pass the recognizer and microphone
        result = recognize_speech_from_mic(recognizer, microphone)

        # Print the recognized speech
        if result["success"]:
            print("You said: {}".format(result["transcription"]))
            perform_action_based_on_keyword(result["transcription"])
        else:
            print("I didn't catch that. What did you say?\nError: {}".format(result["error"]))

        print("Listening again...\n")
