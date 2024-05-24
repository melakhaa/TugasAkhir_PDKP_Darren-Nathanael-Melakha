import tkinter as tk
from tkinter import messagebox

class Flashcard:
    def __init__(self, question, answer):
        self._question = question
        self._answer = answer

    def get_question(self):
        return self._question

    def get_answer(self):
        return self._answer

    def set_question(self, question):
        self._question = question

    def set_answer(self, answer):
        self._answer = answer

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Indonesian History Flashcards")
        self.master.config(bg='#f7f7f7')

        self.flashcards = [
            Flashcard("Siapa presiden Indonesia yang pertama?", "Soekarno"),
            Flashcard("Tahun berapa Indonesia merdeka?", "1945"),
            # Tambah pertanyaan
        ]

        self.current_card_index = 0
        self.correct_answers = 0
        self.total_answers = 0
        self.answer_checked = False  # Tandai jika jawaban sudah dicek

        self.setup_ui()
        master.bind('<Return>', self.on_enter_key)  #bind enter

    def setup_ui(self):
        # Frame untuk layout
        self.top_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.top_frame.pack(pady=20)

        self.middle_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.middle_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.bottom_frame.pack(pady=20)

        # Top frame for question label
        self.question_label = tk.Label(self.top_frame, text="", font=('Arial', 18), bg='#f7f7f7', wraplength=400)
        self.question_label.pack()

        # Middle frame for user input and answer label
        self.user_input = tk.Entry(self.middle_frame, font=('Arial', 16), width=30, bd=2)
        self.user_input.pack(pady=10)

        self.answer_label = tk.Label(self.middle_frame, text="", font=('Arial', 16), bg='#f7f7f7', wraplength=400)
        self.answer_label.pack(pady=10)

        # Bottom frame for buttons
        self.hint_button = tk.Button(self.bottom_frame, text="Hint", command=self.show_hint, font=('Arial', 14), bg='#d1d1d1', width=10)
        self.hint_button.grid(row=0, column=0, padx=5)

        self.check_answer_button = tk.Button(self.bottom_frame, text="Check Answer", command=self.check_answer, font=('Arial', 14), bg='#d1d1d1', width=15)
        self.check_answer_button.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(self.bottom_frame, text="Next Card", command=self.next_card, font=('Arial', 14), bg='#d1d1d1', width=10, state=tk.DISABLED)
        self.next_button.grid(row=0, column=2, padx=5)

        self.show_next_card()

    def show_next_card(self):
        if self.current_card_index < len(self.flashcards):
            card = self.flashcards[self.current_card_index]
            self.question_label.config(text=card.get_question())
            self.answer_label.config(text="")
            self.user_input.delete(0, tk.END)
            self.next_button.config(state=tk.DISABLED)  # matikan tombol next kalo udah gaada pertanyaan
            self.answer_checked = False  #riset jawaban yang uda dicek
        else:
            self.show_score()

    def show_hint(self):
        card = self.flashcards[self.current_card_index]
        hint = card.get_answer()[:3] + "..."
        self.answer_label.config(text=hint)

    def check_answer(self):
        card = self.flashcards[self.current_card_index]
        user_answer = self.user_input.get().strip()
        self.total_answers += 1
        if user_answer.lower() == card.get_answer().lower():
            self.correct_answers += 1
            self.answer_label.config(text=f"✔️ Benar! Jawabannya adalah: {card.get_answer()}", fg='green')
        else:
            self.answer_label.config(text=f"❌ Salah. Jawabannya adalah: {card.get_answer()}", fg='red')
        
        self.next_button.config(state=tk.NORMAL)  # Next button jika jawaban sudah dicek
        self.answer_checked = True  # Set answer checked flag

    def next_card(self):
        self.current_card_index += 1
        self.show_next_card()

    def show_score(self):
        if self.total_answers == 0:
            messagebox.showinfo("Session Complete", "No answers were checked.")
        else:
            score_percentage = (self.correct_answers / self.total_answers) * 100
            self.show_scoreboard(score_percentage)

    def reset_game(self):
        self.correct_answers = 0
        self.total_answers = 0
        self.current_card_index = 0
        self.show_next_card()

        for card in self.flashcards:
            self.show_next_card()

    def on_enter_key(self, event):
        if not self.answer_checked:
            self.check_answer()
        else:
            self.next_card()

    def show_scoreboard(self, score_percentage):
        # new window for scoreboard
        scoreboard_window = tk.Toplevel(self.master)
        scoreboard_window.title("Scoreboard")
        scoreboard_window.geometry("300x200")

        tk.Label(scoreboard_window, text="Selesai!", font=('Arial', 16)).pack(pady=10)
        tk.Label(scoreboard_window, text=f"Nilaimu: {self.correct_answers}/{self.total_answers}", font=('Arial', 14)).pack()

        score_canvas = tk.Canvas(scoreboard_window, width=250, height=100, bg='#f7f7f7')
        score_canvas.pack()

        # Bar
        green_bar_length = score_percentage * 2

        # tengahin greenbar
        bar_left = (250 - green_bar_length) / 2
        bar_right = bar_left + green_bar_length

        # greenbar
        score_canvas.create_rectangle(bar_left, 50, bar_right, 80, fill='green')

        # teks label diatas bar
        text_x = (bar_left + bar_right) / 2
        text_y = 65

        # teks diatas bar
        score_canvas.create_text(text_x, text_y, text=f"{score_percentage:.2f}%", font=('Arial', 12))

def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()  