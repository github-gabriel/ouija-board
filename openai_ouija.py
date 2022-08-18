import threading
import time

import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from PIL import ImageTk, Image

user = "Person:"
ai = "Geist:"
openai.api_key = "YOUR_OPENAI_API_KEY" 
prompt_text = "YOUR_GHOST_PROMPT_TEXT"

# Key: Character (char), Value: Position (Tuple)

characters = {'A': (142, 386),
              'Ä': (142, 386),
              'B': (230, 339),
              'C': (313, 310),
              'D': (394, 285),
              'E': (475, 269),
              'F': (558, 260),
              'G': (630, 257),
              'H': (721, 258),
              'I': (795, 269),
              'J': (855, 277),
              'K': (941, 304),
              'L': (1031, 334),
              'M': (1112, 371),
              'N': (163, 545),
              'O': (231, 495),
              'Ö': (231, 495),
              'P': (303, 452),
              'Q': (376, 423),
              'R': (460, 401),
              'S': (543, 382),
              'T': (621, 377),
              'U': (706, 379),
              'Ü': (706, 379),
              'V': (792, 384),
              'W': (884, 416),
              'X': (977, 453),
              'Y': (1050, 491),
              'Z': (1120, 539),
              '1': (291, 611),
              '2': (350, 614),
              '3': (428, 614),
              '4': (506, 614),
              '5': (588, 616),
              '6': (668, 614),
              '7': (747, 615),
              '8': (824, 616),
              '9': (905, 615),
              '0': (985, 610)}

x = 0
y = +35


class Ouija_Board:

    def __init__(self):

        self.temporary_pointer = None

        # Create Window

        self.root = tk.Tk()

        self.root.geometry("1280x720")
        self.root.title("Ouija Board")

        self.root.update()

        # Create a canvas
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # Images
        self.background_image = ImageTk.PhotoImage(file="ouija_board.png")  # scale image to fit canvas
        self.zeiger_image = ImageTk.PhotoImage(Image.open("ouija_board_zeiger.png").resize((320, 400)).rotate(180))

        # Set images in canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)
        self.zeiger = self.canvas.create_image(0, 0, image=self.zeiger_image, anchor=tk.NW)

        # Exit on close
        self.root.protocol("WM_DELETE_WINDOW", exit)

        # Resizable false
        self.root.resizable(False, False)

        # self.characters['A'][0] -> x-Koordinate von A

    def move_pointer(self, text):
        self.canvas.delete(self.zeiger)
        for char in text:
            char = char.upper()
            if char in characters.keys():
                self.temporary_pointer = self.canvas.create_image(characters[char][0] + x,
                                                                  characters[char][1] + y,
                                                                  image=self.zeiger_image)
                # print("Char: " + char + " X: " + str(self.characters[char][0]) + " Y: " + str(self.characters[char][1])) Prints out info about the current character
                time.sleep(1)
                self.canvas.delete(self.temporary_pointer)
        self.zeiger = self.canvas.create_image(0, 0, image=self.zeiger_image, anchor=tk.NW)

    def listening_status(self, x, y, w, h, color):
        self.canvas.create_oval(x, y, w, h, fill=color)

    def close(self):
        self.root.quit()
        exit(0)


def speak(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def ask(question):
    text = f"{prompt_text}\n{user} {question}"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=text,
        temperature=0.5,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = response['choices'][0]['text'].replace("\n", "")
    return str(response)


class MicrophoneListener(threading.Thread):

    def __init__(self, ouija_board: Ouija_Board):
        super(MicrophoneListener, self).__init__(daemon=True)
        self.ouija_board: Ouija_Board = ouija_board

    def run(self) -> None:
        r = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as microphone:
                    r.adjust_for_ambient_noise(microphone, duration=0.1)

                    ouija_board.listening_status(0, 0, 50, 50, "green")

                    audio = r.listen(microphone)
                    question = r.recognize_google(audio, language='de-DE')

                    ouija_board.listening_status(0, 0, 50, 50, "red")

                    raw_question = question
                    question = user + question.lower() + '\n'

                    print(question)

                    if raw_question.lower() == "goodbye":
                        ouija_board.close()
                    else:
                        answer = ask(question)
                        print(answer)

                        self.ouija_board.move_pointer(answer.replace(ai, "").replace(" ", ""))
                        self.ouija_board.root.update()
            except:
                r = sr.Recognizer()
                continue


if __name__ == '__main__':
    ouija_board = Ouija_Board()

    thread = MicrophoneListener(ouija_board)
    thread.start()

    ouija_board.root.mainloop()
