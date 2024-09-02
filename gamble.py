import tkinter as tk
import random
import pygame
import webbrowser

class SlotMachineGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        self.root.geometry("800x600")
        self.root.attributes('-fullscreen', True)  #Vollbildmodus

        #Symbole mit Wahrscheinlichkeiten und dazugehörigen bits
        self.symbols = ['🍒', '🍋', '🍊', '🍉', '🍇', '🍓']
        self.symbol_colors = ['red', 'yellow', 'orange', 'green', 'purple', 'pink']
        self.symbol_probabilities = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1]  #Wahrscheinlichkeiten für die Symbole
        self.symbol_rewards = [20, 30, 40, 50, 60, 70]  #Gewinne für die Symbole

        #Guthaben
        self.balance = 0

        #Gewinn- und Verlustzähler
        self.consecutive_wins = 0

        #Erstelle GUI-zeug
        self.create_widgets()

    def create_widgets(self):
        #Rahmen für den Titel
        self.title_frame = tk.Frame(self.root, bg="#4CAF50")
        self.title_frame.pack(fill=tk.X, pady=10)

        #Titel-Label
        self.title_label = tk.Label(self.title_frame, text="Slot Machine Game", font=("Helvetica", 28, "bold"), bg="#4CAF50", fg="white")
        self.title_label.pack(pady=10)

        #Guthaben-Anzeige
        self.balance_label = tk.Label(self.root, text="Guthaben: 0 Bits", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        #Rahmen für die Symbole
        self.symbol_display_frame = tk.Frame(self.root)
        self.symbol_display_frame.pack(pady=30)

        #Labels für die Symbole
        self.symbol_labels = [[tk.Label(self.symbol_display_frame, text='', font=("Helvetica", 32), width=2, height=1, borderwidth=2, relief="groove") for _ in range(3)] for _ in range(3)]
        for row in self.symbol_labels:
            row_frame = tk.Frame(self.symbol_display_frame)
            row_frame.pack()
            for label in row:
                label.pack(side=tk.LEFT, padx=20)

        #Eingabefeld für die Einzahlung
        self.deposit_label = tk.Label(self.root, text="Bits einzahlen:", font=("Helvetica", 14))
        self.deposit_label.pack(pady=10)

        self.deposit_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.deposit_entry.pack(pady=5)

        #Einzahlungs-Button
        self.deposit_button = tk.Button(self.root, text="Einzahlen", command=self.deposit, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief=tk.RAISED, bd=5)
        self.deposit_button.pack(pady=10)

        #Spin-Button
        self.spin_button = tk.Button(self.root, text="Spin (10 Bits)", command=self.spin, font=("Helvetica", 18), bg="#2196F3", fg="white", relief=tk.RAISED, bd=5)
        self.spin_button.pack(pady=20)
        self.spin_button.config(state=tk.DISABLED)  #Anfangs deaktiviert

        #Ergebnis-Label
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 22), bg="white")
        self.result_label.pack(pady=10)

        #Schließen-Button
        self.close_button = tk.Button(self.root, text="Schließen", command=self.close, font=("Helvetica", 14), bg="#F44336", fg="white", relief=tk.RAISED, bd=5)
        self.close_button.pack(pady=20)
        
        
    
        github_button = tk.Button(self.root, text="Github", command=self.open_github, font=("Helvetica", 14), bg="black", fg="white", relief=tk.RAISED, bd=5)
        github_button.pack(pady=20)

        #Update der Guthaben-Anzeige
        self.update_balance_display()

    def deposit(self):
        try:
            deposit_amount = int(self.deposit_entry.get())
            if deposit_amount <= 0:
                raise ValueError("Betrag muss positiv sein.")
            self.balance += deposit_amount
            self.deposit_entry.delete(0, tk.END)
            self.update_balance_display()
            self.check_spin_button_state()
        except ValueError:
            self.result_label.config(text="Bitte geben Sie eine gültige Zahl ein.", fg="red")

    def spin(self):
        if self.balance >= 10:
            self.balance -= 10
            self.update_balance_display()
            self.animate_spin()
        else:
            self.result_label.config(text="Nicht genügend Guthaben für einen Spin.", fg="red")

    def animate_spin(self):
        self.result_label.config(text="Spinning...", fg="blue")
        self.animation_step = 0
        self.animate_step()

    def animate_step(self):
        if self.animation_step < 20:  #Anzahl der Animation-Schritte
            self.animation_step += 1
            self.update_symbols()
            self.root.after(100, self.animate_step)  #Wiederhole alle 100 Millisekunden
        else:
            self.perform_spin()

    def update_symbols(self):
        for i in range(3):
            for j in range(3):
                #Zufälliges Symbol für die Animation
                symbol = random.choices(self.symbols, self.symbol_probabilities)[0]
                self.symbol_labels[i][j].config(text=symbol, fg=self.get_symbol_color(symbol))

    def perform_spin(self):
        #Generiere zufällige Symbole basierend auf den Wahrscheinlichkeiten
        results = [[random.choices(self.symbols, self.symbol_probabilities)[0] for _ in range(3)] for _ in range(3)]

        #Update der Symbole in der GUI
        for i in range(3):
            for j in range(3):
                symbol = results[i][j]
                self.symbol_labels[i][j].config(text=symbol, fg=self.get_symbol_color(symbol))

        #Überprüfe auf Gewinne
        self.check_wins(results)

        if self.spin_sound:
            pygame.mixer.stop()

    def check_wins(self, results):
        won = False
        win_amount = 0

        #Hintergrundfarbe zurücksetzen
        for i in range(3):
            for j in range(3):
                self.symbol_labels[i][j].config(bg="white")

        #Checke horizontale und vertikale Gewinne
        for i in range(3):
            if results[i][0] == results[i][1] == results[i][2]:
                won = True
                win_amount += self.get_symbol_reward(results[i][0])
                for label in self.symbol_labels[i]:
                    label.config(bg="green")
            if results[0][i] == results[1][i] == results[2][i]:
                won = True
                win_amount += self.get_symbol_reward(results[0][i])
                for j in range(3):
                    self.symbol_labels[j][i].config(bg="green")

        #Checke diagonale Gewinne
        if results[0][0] == results[1][1] == results[2][2]:
            won = True
            win_amount += self.get_symbol_reward(results[0][0])
            for i, j in zip(range(3), range(3)):
                self.symbol_labels[i][j].config(bg="green")

        if results[0][2] == results[1][1] == results[2][0]:
            won = True
            win_amount += self.get_symbol_reward(results[0][2])
            for i, j in zip(range(3), range(2, -1, -1)):
                self.symbol_labels[i][j].config(bg="green")

        if won:
            self.balance += win_amount
            self.result_label.config(text=f"Herzlichen Glückwunsch! Sie gewinnen {win_amount} Bits!", fg="green")
            if self.win_sound:
                pygame.mixer.stop()
                self.win_sound.play()
            self.consecutive_wins += 1
        else:
            self.result_label.config(text="Versuchen Sie es noch einmal!", fg="red")
            if self.lose_sound:
                pygame.mixer.stop()
                self.lose_sound.play()
            self.consecutive_wins = 0

        if self.consecutive_wins >= 3:
            self.adjust_probabilities(True)
        else:
            self.adjust_probabilities(False)

        self.update_balance_display()
        self.check_spin_button_state()

    def get_symbol_reward(self, symbol):
        index = self.symbols.index(symbol)
        return self.symbol_rewards[index]

    def get_symbol_color(self, symbol):
        index = self.symbols.index(symbol)
        return self.symbol_colors[index]

    def adjust_probabilities(self, decrease):
        if decrease:
            #Wahrscheinlichkeiten erhöhen (mehr gleiche Symbole)
            self.symbol_probabilities = [0.3, 0.3, 0.2, 0.1, 0.05, 0.05]
        else:
            #Wahrscheinlichkeiten normalisieren
            self.symbol_probabilities = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1]

    def update_balance_display(self):
        self.balance_label.config(text=f"Guthaben: {self.balance} Bits")

    def check_spin_button_state(self):
        if self.balance >= 10:
            self.spin_button.config(state=tk.NORMAL)
        else:
            self.spin_button.config(state=tk.DISABLED)

    def close(self):
        pygame.mixer.quit()
        self.root.destroy()
    def open_github(self):
            webbrowser.open("https://github.fh-zwickau.de/hes23n6v/slot_maschine")

#Erstelle das Hauptfenster
root = tk.Tk()
game = SlotMachineGame(root)
root.mainloop()
