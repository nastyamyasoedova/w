import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Путь к файлу данных
DATA_FILE = "quotes_data.json"

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x550")

        # Исходные данные
        self.quotes = [
            {"text": "Жизнь — это то, что случается с тобой, пока ты оживлённо строишь другие планы.", "author": "Джон Леннон", "topic": "Жизнь"},
            {"text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.", "author": "Альберт Эйнштейн", "topic": "Наука"},
            {"text": "Успех — это идти от ошибки к ошибке, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"},
            {"text": "Великие умы обсуждают идеи; средние умы обсуждают события; мелкие умы обсуждают людей.", "author": "Элеонора Рузвельт", "topic": "Мудрость"},
            {"text": "Единственный способ делать великие дела — любить то, что вы делаете.", "author": "Стив Джобс", "topic": "Работа"}
        ]
        
        self.history = []
        self.load_data()
        self.create_widgets()

    def load_data(self):
        """Загрузка истории и списка цитат из JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get("history", [])
                    # Если в файле есть новые цитаты, объединяем их с базовыми
                    saved_quotes = data.get("quotes", [])
                    if saved_quotes:
                        self.quotes = saved_quotes
            except Exception as e:
                print(f"Ошибка загрузки: {e}")

    def save_data(self):
        """Сохранение данных в JSON"""
        data = {
            "quotes": self.quotes,
            "history": self.history
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # --- Секция генерации ---
        frame_gen = tk.LabelFrame(self.root, text="Генератор", padx=10, pady=10)
        frame_gen.pack(fill="x", padx=10, pady=5)

        self.lbl_quote = tk.Label(frame_gen, text="Нажмите кнопку, чтобы получить цитату", 
                                  wraplength=500, font=("Arial", 11, "italic"))
        self.lbl_quote.pack(pady=10)

        self.lbl_author = tk.Label(frame_gen, text="", font=("Arial", 10, "bold"))
        self.lbl_author.pack()

        # Фильтры
        filter_frame = tk.Frame(frame_gen)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=0)
        self.cb_topic = ttk.Combobox(filter_frame, values=["Все"] + list(set(q['topic'] for q in self.quotes)))
        self.cb_topic.set("Все")
        self.cb_topic.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=2)
        self.cb_author = ttk.Combobox(filter_frame, values=["Все"] + list(set(q['author'] for q in self.quotes)))
        self.cb_author.set("Все")
        self.cb_author.grid(row=0, column=3, padx=5)

        btn_gen = tk.Button(frame_gen, text="Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50", fg="white")
        btn_gen.pack(pady=10)

        # --- Секция истории ---
        tk.Label(self.root, text="История цитат:").pack()
        self.history_list = tk.Listbox(self.root, height=8)
        self.history_list.pack(fill="both", padx=10, pady=5)
        self.update_history_display()

        # --- Секция добавления (для проверки ввода) ---
        frame_add = tk.LabelFrame(self.root, text="Добавить новую цитату", padx=10, pady=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_add, text="Текст:").grid(row=0, column=0)
        self.ent_text = tk.Entry(frame_add, width=40)
        self.ent_text.grid(row=0, column=1, padx=5)

        tk.Label(frame_add, text="Автор:").grid(row=1, column=0)
        self.ent_author = tk.Entry(frame_add)
        self.ent_author.grid(row=1, column=1, sticky="w", padx=5)

        btn_add = tk.Button(frame_add, text="Добавить", command=self.add_custom_quote)
        btn_add.grid(row=1, column=1, sticky="e")

    def generate_quote(self):
        topic_f = self.cb_topic.get()
        author_f = self.cb_author.get()

        filtered = self.quotes
        if topic_f != "Все":
            filtered = [q for q in filtered if q['topic'] == topic_f]
        if author_f != "Все":
            filtered = [q for q in filtered if q['author'] == author_f]

        if not filtered:
            messagebox.showwarning("Внимание", "Цитат с такими фильтрами не найдено!")
            return

        selected = random.choice(filtered)
        self.lbl_quote.config(text=f"«{selected['text']}»")
        self.lbl_author.config(text=f"— {selected['author']} ({selected['topic']})")
        
        # Добавляем в историю
        hist_entry = f"{selected['author']}: {selected['text'][:40]}..."
        self.history.append(hist_entry)
        self.update_history_display()
        self.save_data()

    def update_history_display(self):
        self.history_list.delete(0, tk.END)
        for item in reversed(self.history):
            self.history_list.insert(tk.END, item)

    def add_custom_quote(self):
        text = self.ent_text.get().strip()
        author = self.ent_author.get().strip()
        
        # Проверка корректности ввода (пустые строки)
        if not text or not author:
            messagebox.showerror("Ошибка", "Текст и автор не могут быть пустыми!")
            return

        new_q = {"text": text, "author": author, "topic": "Разное"}
        self.quotes.append(new_q)
        
        # Обновляем списки в комбобоксах
        self.cb_author['values'] = ["Все"] + list(set(q['author'] for q in self.quotes))
        
        self.ent_text.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.save_data()
        messagebox.showinfo("Успех", "Цитата добавлена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
