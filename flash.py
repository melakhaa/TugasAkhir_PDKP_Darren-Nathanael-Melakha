import tkinter as tk
from tkinter import messagebox
from collections import deque
import random

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
        self.master.geometry("600x700")
        self.master.config(bg='#f7f7f7')

        self.flashcards = [
            Flashcard("Siapa presiden Indonesia yang pertama?", "Soekarno"),
            Flashcard("Tahun berapa Indonesia merdeka?", "1945"),
            Flashcard("Siapa presiden Indonesia yang kedua?", "Soeharto"),
            Flashcard("Apa nama perjanjian yang mengakhiri Konfrontasi Indonesia-Malaysia?", "Perjanjian Bangkok"),
            Flashcard("Siapa pahlawan wanita dari Aceh yang berperang melawan Belanda?", "Cut Nyak Dien"),
            Flashcard("Apa nama kerajaan Hindu pertama di Indonesia?", "Kerajaan Kutai"),
            Flashcard("Siapa yang mendirikan organisasi Budi Utomo?", "Dr. Soetomo"),
            Flashcard("Apa nama pertempuran besar di Surabaya pada tahun 1945?", "Pertempuran Surabaya"),
            Flashcard("Siapa tokoh utama di balik Proklamasi Kemerdekaan Indonesia?", "Soekarno dan Mohammad Hatta"),
            Flashcard("Kapan Sumpah Pemuda dideklarasikan?", "28 Oktober 1928"),
            Flashcard("Apa nama gerakan yang menuntut reformasi politik di Indonesia pada tahun 1998?", "Reformasi"),
            Flashcard("Siapa yang dikenal sebagai pahlawan dari Blitar?", "Soekarno"),
            Flashcard("Apa nama perjanjian yang mengakui kedaulatan Indonesia oleh Belanda?", "Perjanjian Linggarjati"),
            Flashcard("Siapa pahlawan dari Minangkabau yang dikenal dengan Perang Paderi?", "Tuanku Imam Bonjol"),
            Flashcard("Apa nama organisasi yang didirikan pada tahun 1908 sebagai awal kebangkitan nasional?", "Budi Utomo"),
            Flashcard("Siapa Gubernur Jenderal VOC yang mendirikan Batavia?", "Jan Pieterszoon Coen"),
            Flashcard("Kapan Indonesia menjadi anggota PBB?", "28 September 1950"),
            Flashcard("Apa nama peristiwa di mana tujuh jenderal Indonesia dibunuh pada tahun 1965?", "G30S/PKI"),
            Flashcard("Siapa tokoh utama dalam Serangan Umum 1 Maret 1949?", "Sultan Hamengkubuwono IX"),
            Flashcard("Apa nama ibu kota kerajaan Majapahit?", "Trowulan"),
            Flashcard("Siapa yang mengucapkan 'Proklamasi Kemerdekaan Indonesia'?", "Soekarno"),
            Flashcard("Apa nama perjanjian yang menyatukan Nusantara di bawah Gajah Mada?", "Sumpah Palapa")
            # Tambah pertanyaan lain di sini
        ]

        self.stack = []  # Stack to shuffle flashcards
        self.forward_stack = deque()  # Stack to manage forward flashcards
        self.backward_stack = deque()  # Stack to manage backward flashcards
        self.shuffle_flashcards()

        self.correct_answers = 0
        self.total_answers = 0
        self.answer_checked = False

        self.setup_ui()
        self.show_next_card()
        master.bind('<Return>', self.on_enter_key)

    def setup_ui(self):
        self.top_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.top_frame.pack(pady=20)

        self.middle_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.middle_frame.pack(pady=20)

        self.question_label = tk.Label(self.top_frame, text="", font=('Arial', 16), bg='#f7f7f7', wraplength=350)
        self.question_label.pack()

        self.user_input = tk.Entry(self.middle_frame, font=('Arial', 14), width=30, bd=2)
        self.user_input.pack(pady=10)

        self.answer_label = tk.Label(self.middle_frame, text="", font=('Arial', 14), bg='#f7f7f7', wraplength=350)
        self.answer_label.pack(pady=10)

        self.bottom_frame = tk.Frame(self.master, bg='#f7f7f7')
        self.bottom_frame.pack(pady=20, side=tk.BOTTOM, fill=tk.X)

        self.button_frame = tk.Frame(self.bottom_frame, bg='#f7f7f7')
        self.button_frame.pack()

        self.hint_button = tk.Button(self.button_frame, text="Hint", command=self.show_hint, font=('Arial', 12), bg='#d1d1d1', width=10)
        self.hint_button.grid(row=0, column=0, padx=5)

        self.check_answer_button = tk.Button(self.button_frame, text="Check Answer", command=self.check_answer, font=('Arial', 12), bg='#d1d1d1', width=15)
        self.check_answer_button.grid(row=0, column=1, padx=5)

        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.previous_card, font=('Arial', 12), bg='#d1d1d1', width=10)
        self.prev_button.grid(row=0, column=2, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_card, font=('Arial', 12), bg='#d1d1d1', width=10)
        self.next_button.grid(row=0, column=3, padx=5)

    def shuffle_flashcards(self):
        # Shuffle the flashcards using the stack
        indices = list(range(len(self.flashcards)))
        random.shuffle(indices)
        for index in indices:
            self.stack.append(self.flashcards[index])

        while self.stack:
            self.forward_stack.append(self.stack.pop())

    def show_next_card(self):
        if self.forward_stack:
            card = self.forward_stack[0]
            self.question_label.config(text=card.get_question())
            self.answer_label.config(text="")
            self.user_input.delete(0, tk.END)
            self.answer_checked = False
        else:
            self.show_score()

    def show_hint(self):
        card = self.forward_stack[0]
        hint = card.get_answer()[:3] + "..."
        self.answer_label.config(text=hint)

    def check_answer(self):
        card = self.forward_stack[0]
        user_answer = self.user_input.get().strip()
        self.total_answers += 1
        if user_answer.lower() == card.get_answer().lower():
            self.correct_answers += 1
            self.answer_label.config(text=f"✔️ Benar! Jawabannya adalah: {card.get_answer()}", fg='green')
        else:
            self.answer_label.config(text=f"❌ Salah. Jawabannya adalah: {card.get_answer()}", fg='red')
        
        self.next_button.config(state=tk.NORMAL)
        self.answer_checked = True

    def next_card(self):
        if self.forward_stack:
            card = self.forward_stack.popleft()
            self.backward_stack.appendleft(card)
            self.show_next_card()


    def previous_card(self):
        if self.backward_stack:
            card = self.backward_stack.popleft()
            self.forward_stack.appendleft(card)
            self.show_previous_card()

    def show_previous_card(self):
        if self.forward_stack:
            card = self.forward_stack[0]
            self.question_label.config(text=card.get_question())
            self.answer_label.config(text="")
            self.user_input.delete(0, tk.END)
            self.answer_checked = False

    def show_score(self):
        if self.total_answers == 0:
            messagebox.showinfo("Peringatan", "Anda telah sampai di flashcard terakhir.")
        else:
            score_percentage = (self.correct_answers / self.total_answers) * 100
            self.show_scoreboard(score_percentage)

    def reset_game(self):
        self.correct_answers = 0
        self.total_answers = 0
        self.forward_stack.clear()
        self.backward_stack.clear()
        self.shuffle_flashcards()
        self.show_next_card()

    def on_enter_key(self, event):
        if self.answer_checked:
            self.next_card()
        elif self.forward_stack:
            self.check_answer()
        else:
            messagebox.showinfo("Peringatan", "Tidak ada pertanyaan yang tersedia.")
            self.user_input.focus_set()  # Set focus to the answer entry


    def show_scoreboard(self, score_percentage):
        scoreboard_window = tk.Toplevel(self.master)
        scoreboard_window.title("Scoreboard")
        scoreboard_window.geometry("300x200")

        tk.Label(scoreboard_window, text="Selesai!", font=('Arial', 16)).pack(pady=10)
        tk.Label(scoreboard_window, text=f"Nilaimu: {self.correct_answers}/{self.total_answers}", font=('Arial', 14)).pack()

        score_canvas = tk.Canvas(scoreboard_window, width=250, height=100, bg='#f7f7f7')
        score_canvas.pack()

        green_bar_length = score_percentage * 2

        bar_left = (250 - green_bar_length) / 2
        bar_right = bar_left + green_bar_length

        score_canvas.create_rectangle(bar_left, 50, bar_right, 80, fill='green')

        text_x = (bar_left + bar_right) / 2
        text_y = 65

        score_canvas.create_text(text_x, text_y, text=f"{score_percentage:.2f}%", font=('Arial', 12))

def main():
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
