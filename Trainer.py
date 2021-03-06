import random
import tkinter as tk
import winsound
import os

# Constants to be used
NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
LARGE_FONT = ("Verdana", 40)
SMALL_FONT = ("Verdana", 16)

# Create directory string
sound_dir = os.getcwd() + '\Sounds'

# The Trainer class that creates the GUI and 
class Trainer(tk.Frame):

    # Initialise class
    def __init__(self):
        tk.Frame.__init__(self)
        self.has_been_called = False
        self.create_frames()
        self.create_buttons()  
        self.answers = []

            
    def create_frames(self):
        
        # Create frames to contain widgets
        self.topFrame = tk.Frame(self)
        self.bottomFrame = tk.Frame(self)
        self.middleFrame = tk.Frame(self)

        # Set their positions
        self.topFrame.grid(sticky="n")
        self.bottomFrame.grid(sticky="s")
        self.middleFrame.grid(sticky="ns")

        # Create text output windows
        self.mainwindow = tk.Label(self.topFrame, text="Ear Trainer", font=LARGE_FONT)
        self.mainwindow.grid(sticky="n")
        self.outputwindow = tk.Label(self.topFrame, text="Welcome. Click Begin to start")
        self.outputwindow.grid(sticky="s")

        # Create container for buttons
        self.buttons = tk.Frame(self.bottomFrame, bg="white")
        self.buttons.grid(row=0)
        

    def create_buttons(self):       
        # Iterate through NOTES and create a button, then assign a unique function to each via lambda
        for i in range(len(NOTES)):
            r = 0
            if i >= 6:
                r = 1
                self.button = tk.Button(self.buttons, text=f"{NOTES[i]}", font=SMALL_FONT,  command=lambda i=i:self.validate_guess(NOTES[i]))
                self.button.grid(row=r, column=i-6)
                self.button.config(height=3, width=4)

            else:
                self.button = tk.Button(self.buttons, text=f"{NOTES[i]}",font=SMALL_FONT, command=lambda i=i:self.validate_guess(NOTES[i]))
                self.button.grid(row=r, column=i)
                self.button.config(height=3, width=4)

        # Create the begin and end buttons            
        self.begin = tk.Button(self.topFrame, text="Begin", command=self.play_note, font=SMALL_FONT)
        self.begin.grid(sticky="s")
        self.end = tk.Button(self.middleFrame, text="End", command=self.print_answers)
        self.end.grid(sticky="n")


    # Begin the game and play a random note
    def play_note(self):   
        self.has_been_called = True
        self.mainwindow.config(text="PLAYING NOTE")
        self.outputwindow.config(text="Take your guess!")
        print("Playing sound...")

        # Assign note variable from random choice
        self.note = random.choice(NOTES)
        note_dir = f"{sound_dir}\{self.note}"
        winsound.PlaySound(f"{note_dir}.wav", winsound.SND_ASYNC)
        print("Take your guess!")

    # Determine whether the player's guess was correct, then update the output windows
    def validate_guess(self, value):    
        self.value = value
        if self.has_been_called == True:
            self.calculate_steps()
            if value == self.note:
                self.mainwindow.config(text="Correct!")
                self.outputwindow.config(text=f"Good job!, the note was {self.note}. Click Begin to play again")
                print(f"Good job!, the note was {self.note}")
                self.answers.append(1)
            else:
                self.mainwindow.config(text="Incorrect")

                self.outputwindow.config(text=f"Wrong! The note was {self.note}, you chose {value}. You were {self.distance} half-steps away. Click Begin to play again")
                print(f"Wrong! The note was {self.note}, you chose {value}. You were {self.distance} half-steps away")
                self.answers.append(0)
        else:
            self.outputwindow.config(text="Error: No note played! Please Click Begin")            
            print("Error: Note not played! Please press Begin")

      
    # Calculate amount of half-steps between player's choice and correct note
    def calculate_steps(self):
        self.distance = abs(NOTES.index(self.value) - NOTES.index(self.note))

    # Called when the game ends. Outputs score and accuracy rating. 
    def print_answers(self):
        ans = sum(self.answers)
        acc_percentage = round((ans/len(self.answers))*100, 3)

        if ans > 0:
            self.mainwindow.config(text="WELL DONE")
            self.outputwindow.config(text=f"Well done! Your score was {ans} out of {len(self.answers)} tries.\nThat's a {acc_percentage}% accuracy rate!\n ")            
            print(f"Congrats, your score was {ans}\n ")
        else:
            self.mainwindow.config(text="TRY AGAIN")
            self.outputwindow.config(text=f"Your score was {ans}... Maybe try again...")            
            print(f"Your score was {ans}... Maybe try again...")
        print(f"You tried {len(self.answers)} times.")
        print(f"That's a {(ans/len(self.answers))*100}% accuracy rate!")

        
if __name__ == "__main__":
    root = Trainer()
    root.pack()
    root.mainloop()
