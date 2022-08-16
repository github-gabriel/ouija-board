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
prompt_text = "EXAMPLE PROMPT FOR A GHOST"


class Ouija_Board:

    def __init__(self):

        self.temporary_pointer = None

        self.x = 0
        self.y = +35

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

        # Key: Character (char), Value: Position (Tuple)

        self.characters = {'A': (142+self.x, 386+self.y),
                           'Ä': (142 + self.x, 386 + self.y),
                           'B': (230+self.x, 339+self.y),
                           'C': (313+self.x, 310+self.y),
                           'D': (394+self.x, 285+self.y),
                           'E': (475+self.x, 269+self.y),
                           'F': (558+self.x, 260+self.y),
                           'G': (630+self.x, 257+self.y),
                           'H': (721+self.x, 258+self.y),
                           'I': (795+self.x, 269+self.y),
                           'J': (855+self.x, 277+self.y),
                           'K': (941+self.x, 304+self.y),
                           'L': (1031+self.x, 334+self.y),
                           'M': (1112+self.x, 371+self.y),
                           'N': (163+self.x, 545+self.y),
                           'O': (231+self.x, 495+self.y),
                           'Ö': (231 + self.x, 495 + self.y),
                           'P': (303+self.x, 452+self.y),
                           'Q': (376+self.x, 423+self.y),
                           'R': (460+self.x, 401+self.y),
                           'S': (543+self.x, 382+self.y),
                           'T': (621+self.x, 377+self.y),
                           'U': (706+self.x, 379+self.y),
                           'Ü': (706+self.x, 379+self.y),
                           'V': (792+self.x, 384+self.y),
                           'W': (884+self.x, 416+self.y),
                           'X': (977+self.x, 453+self.y),
                           'Y': (1050+self.x, 491+self.y),
                           'Z': (1120+self.x, 539+self.y),
                           '1': (291+self.x, 611+self.y),
                           '2': (350+self.x, 614+self.y),
                           '3': (428+self.x, 614+self.y),
                           '4': (506+self.x, 614+self.y),
                           '5': (588+self.x, 616+self.y),
                           '6': (668+self.x, 614+self.y),
                           '7': (747+self.x, 615+self.y),
                           '8': (824+self.x, 616+self.y),
                           '9': (905+self.x, 615+self.y),
                           '0': (985+self.x, 610+self.y)}

        # self.characters['A'][0] -> x-Koordinate von A

    def move_pointer(self, text):
        self.canvas.delete(self.zeiger)
        for char in text:
            char = char.upper()
            if char in self.characters.keys():
                self.temporary_pointer = self.canvas.create_image(self.characters[char][0], self.characters[char][1], image=self.zeiger_image)
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
