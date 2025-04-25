import tkinter as tk
from tkinter import messagebox
import os
import json
# 删除 PIL 相关导入
# from PIL import Image, ImageTk  

class WordGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Two-Player Word Game")
        self.master.configure(bg="#F8EDE3")  

        self.current_letter = tk.StringVar()
        self.boards = []
        self.row_score_labels = []
        self.col_score_labels = []
        self.current_player = 0
        self.remaining_spaces = 25
        self.waiting_for_player2 = False
        self.both_players_placed = False
        self.players_boards = [[[' ' for _ in range(5)] for _ in range(5)] for _ in range(2)]
        self.total_score_labels = []
        self.confirm_buttons = []  # 新增：存储确认按钮
        self.temp_placement = [None, None]  # 新增：存储临时放置的位置

        self.control_frame = tk.Frame(master, bg="#F8EDE3")
        self.control_frame.grid(row=0, column=0, columnspan=4, pady=20)

        self.turn_label = tk.Label(self.control_frame, text="Player 1, please enter a letter", font=('Comic Sans MS', 14), bg="#F8EDE3", fg="#D2B4DE")
        self.turn_label.grid(row=0, column=0, columnspan=2)

        self.letter_entry = tk.Entry(self.control_frame, textvariable=self.current_letter, width=5, font=('Comic Sans MS', 18), bg="#D2B4DE", fg="#F8EDE3")
        self.letter_entry.grid(row=1, column=0)

        self.confirm_button = tk.Button(self.control_frame, text="Confirm", command=self.confirm_letter, bg="#D2B4DE", fg="#F8EDE3", font=('Comic Sans MS', 14))
        self.confirm_button.grid(row=1, column=1)

        for player in range(2):
            outer_frame = tk.Frame(master, bg="#F8EDE3", borderwidth=5, relief="sunken")
            outer_frame.grid(row=1, column=player * 2, padx=10, pady=20)

            frame = tk.Frame(outer_frame, bg="#F8EDE3")
            frame.pack(padx=10, pady=10)

            board_labels = []
            row_scores = []
            col_scores = []

            for i in range(5):
                row_labels = []
                for j in range(5):
                    label = tk.Label(frame, text=' ', width=4, height=2, borderwidth=2, relief="raised", font=('Comic Sans MS', 18), bg="#D2B4DE", fg="#F8EDE3", highlightthickness=2, highlightbackground="#F8EDE3", highlightcolor="#F8EDE3", padx=5, pady=5)
                    label.grid(row=i, column=j, padx=3, pady=3)
                    label.bind("<Button-1>", lambda e, x=i, y=j, p=player: self.place_letter(p, x, y))
                    row_labels.append(label)
                board_labels.append(row_labels)

                score_label = tk.Label(frame, text="0", width=4, height=2, bg="#D2B4DE", fg="#F8EDE3", font=('Comic Sans MS', 14))
                score_label.grid(row=i, column=5, padx=3, pady=3)
                row_scores.append(score_label)

            for j in range(5):
                score_label = tk.Label(frame, text="0", width=4, height=2, bg="#D2B4DE", fg="#F8EDE3", font=('Comic Sans MS', 14))
                score_label.grid(row=5, column=j, padx=3, pady=3)
                col_scores.append(score_label)

            # 新增：确认按钮
            confirm_btn = tk.Button(frame, text="Confirm Placement", command=lambda p=player: self.confirm_placement(p), bg="#D2B4DE", fg="#F8EDE3", font=('Comic Sans MS', 14), state='disabled')
            confirm_btn.grid(row=6, column=0, columnspan=6, pady=5)
            self.confirm_buttons.append(confirm_btn)

            total_score_label = tk.Label(frame, text=f"Player {player + 1} Total Score: 0", font=('Comic Sans MS', 14), bg="#F8EDE3", fg="#D2B4DE")
            total_score_label.grid(row=7, column=0, columnspan=6, pady=10)
            self.total_score_labels.append(total_score_label)

            self.boards.append(board_labels)
            self.row_score_labels.append(row_scores)
            self.col_score_labels.append(col_scores)

        self.valid_words = set()
        json_files = ["3-letter-words.json", "4-letter-words.json", "5-letter-words.json"]
        for file_name in json_files:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        self.valid_words.add(item["word"].upper())
            except FileNotFoundError:
                print(f"File {file_name} not found. Please check if the file exists.")

        self.update_board_colors()

    def confirm_letter(self):
        letter = self.current_letter.get().strip().upper()
        if len(letter) == 1 and letter.isalpha():
            self.current_letter.set(letter)
            self.letter_entry.config(state='disabled')
            self.turn_label.config(text=f"Player {self.current_player + 1}, please place the letter: {letter}")
            self.waiting_for_player2 = False
            self.both_players_placed = False
            self.update_board_colors()
            # 启用当前玩家的确认按钮
            self.confirm_buttons[self.current_player].config(state='normal')
        else:
            messagebox.showerror("Error", "Please enter a single letter")

    def is_valid_word(self, word):
        return word.upper() in self.valid_words

    def update_board_colors(self):
        prompt_text = self.turn_label.cget("text")
        light_brown_color = "#E9DCC9"  # 浅黄棕色
        darker_brown_color = "#DBC9B0"  # 略深的浅黄色
        original_color = "#D2B4DE"  # 原粉紫配色
        original_text_color = "#8B4513"  # 原字母颜色
        disabled_text_color = "white"  # 棕黄配色时的字母颜色

        for player in range(2):
            board = self.players_boards[player]
            if "please enter a letter" in prompt_text:
                base_color = light_brown_color
                text_color = disabled_text_color
            elif "Player 1, please place the letter" in prompt_text:
                if player == 0:
                    base_color = original_color
                    text_color = original_text_color
                else:
                    base_color = light_brown_color
                    text_color = disabled_text_color
            elif "Player 2, please place the letter" in prompt_text:
                if player == 1:
                    base_color = original_color
                    text_color = original_text_color
                else:
                    base_color = light_brown_color
                    text_color = disabled_text_color

            # 重置所有字母颜色和背景色
            for row in range(5):
                for col in range(5):
                    self.boards[player][row][col].config(fg=text_color, bg=base_color)

            # 重置分数标签
            for row in range(5):
                self.row_score_labels[player][row].config(text="0")
            for col in range(5):
                self.col_score_labels[player][col].config(text="0")

            # 检查行单词
            for row_index, row in enumerate(board):
                word_str = ''.join(row).strip()
                used_indices = set()
                # 找出所有有效单词并按长度排序
                valid_words = []
                start = 0
                while start < len(row):
                    for end in range(start + 3, len(row) + 1):
                        sub_word = ''.join(row[start:end]).strip()
                        if self.is_valid_word(sub_word):
                            valid_words.append((sub_word, start, end))
                    start += 1
                valid_words.sort(key=lambda x: len(x[0]), reverse=True)

                for word, start, end in valid_words:
                    overlap = False
                    for i in range(start, end):
                        if i in used_indices:
                            overlap = True
                            break
                    if not overlap:
                        for col_index in range(start, end):
                            if row[col_index] != ' ':
                                if base_color == original_color:
                                    self.boards[player][row_index][col_index].config(fg="darkred", bg="#E0F7FA")
                                elif base_color == light_brown_color:
                                    self.boards[player][row_index][col_index].config(fg="white", bg=darker_brown_color)
                                used_indices.add(col_index)
                        # 更新行分数
                        word_score = len(word) ** 2
                        current_score = int(self.row_score_labels[player][row_index].cget("text"))
                        self.row_score_labels[player][row_index].config(text=str(current_score + word_score))

            # 检查列单词
            for col_index in range(5):
                col_letters = [board[row][col_index] for row in range(5)]
                word_str = ''.join(col_letters).strip()
                used_indices = set()
                # 找出所有有效单词并按长度排序
                valid_words = []
                start = 0
                while start < len(col_letters):
                    for end in range(start + 3, len(col_letters) + 1):
                        sub_word = ''.join(col_letters[start:end]).strip()
                        if self.is_valid_word(sub_word):
                            valid_words.append((sub_word, start, end))
                    start += 1
                valid_words.sort(key=lambda x: len(x[0]), reverse=True)

                for word, start, end in valid_words:
                    overlap = False
                    for i in range(start, end):
                        if i in used_indices:
                            overlap = True
                            break
                    if not overlap:
                        for row_index in range(start, end):
                            if col_letters[row_index] != ' ':
                                if base_color == original_color:
                                    self.boards[player][row_index][col_index].config(fg="darkred", bg="#E0F7FA")
                                elif base_color == light_brown_color:
                                    self.boards[player][row_index][col_index].config(fg="white", bg=darker_brown_color)
                                used_indices.add(row_index)
                        # 更新列分数
                        word_score = len(word) ** 2
                        current_score = int(self.col_score_labels[player][col_index].cget("text"))
                        self.col_score_labels[player][col_index].config(text=str(current_score + word_score))

            # 更新总分数标签
            row_total = sum(int(self.row_score_labels[player][i].cget("text")) for i in range(5))
            col_total = sum(int(self.col_score_labels[player][i].cget("text")) for i in range(5))
            total_score = row_total + col_total
            self.total_score_labels[player].config(text=f"Player {player + 1} Total Score: {total_score}")

            # 更新行、列和总分数标签背景色
            for row in range(5):
                self.row_score_labels[player][row].config(bg=base_color)
            for col in range(5):
                self.col_score_labels[player][col].config(bg=base_color)
            self.total_score_labels[player].config(bg="#F8EDE3")

            # 更新确认按钮的背景色
            if "please enter a letter" in prompt_text:
                button_color = light_brown_color
            elif "Player 1, please place the letter" in prompt_text:
                button_color = original_color if player == 0 else light_brown_color
            elif "Player 2, please place the letter" in prompt_text:
                button_color = original_color if player == 1 else light_brown_color
            self.confirm_buttons[player].config(bg=button_color)

    def calculate_scores(self):
        # 由于 update_board_colors 已经计算了分数，这里可以简化
        scores = [0, 0]
        for player in range(2):
            row_total = sum(int(self.row_score_labels[player][i].cget("text")) for i in range(5))
            col_total = sum(int(self.col_score_labels[player][i].cget("text")) for i in range(5))
            scores[player] = row_total + col_total
        return scores

    def place_letter(self, player, row, col):
        if self.boards[player][row][col]['text'] != ' ':
            return

        if not self.both_players_placed:
            if (not self.waiting_for_player2 and player == self.current_player) or (self.waiting_for_player2 and player == 1 - self.current_player):
                # 清除之前的临时标记
                if self.temp_placement[player]:
                    prev_row, prev_col = self.temp_placement[player]
                    self.boards[player][prev_row][prev_col].config(text=' ', fg="#8B4513", bg="#D2B4DE")

                # 临时标记字母
                self.boards[player][row][col].config(text=self.current_letter.get(), bg="#D2B4DE", fg="blue")
                self.temp_placement[player] = (row, col)

    def confirm_placement(self, player):
        if self.temp_placement[player]:
            row, col = self.temp_placement[player]
            self.boards[player][row][col].config(fg="#8B4513")
            self.players_boards[player][row][col] = self.current_letter.get()
            self.temp_placement[player] = None

            if not self.waiting_for_player2:
                self.waiting_for_player2 = True
                self.turn_label.config(text=f"Player {2 - self.current_player}, please place the letter {self.current_letter.get()}")
                self.confirm_buttons[player].config(state='disabled')
                self.confirm_buttons[1 - player].config(state='normal')
            else:
                self.both_players_placed = True
                self.current_letter.set('')
                self.letter_entry.config(state='normal')
                self.remaining_spaces -= 1
                scores = self.calculate_scores()  # 先计算分数
                if self.remaining_spaces == 0:
                    # 创建新的弹窗
                    result_window = tk.Toplevel(self.master)
                    # 修改前：result_window.title("游戏结果")
                    result_window.title("Game Result")
                    result_window.configure(bg="#F8EDE3")

                    if scores[0] > scores[1]:
                        # 修改前：winner_text = f"玩家 1 获胜！\n"
                        winner_text = f"Player 1 Wins!\n"
                        player1_text = f"Player 1 Score: {scores[0]}"
                        player2_text = f"Player 2 Score: {scores[1]}"
                        player1_color = "darkred"
                        player2_color = "#D2B4DE"
                    elif scores[1] > scores[0]:
                        # 修改前：winner_text = f"玩家 2 获胜！\n"
                        winner_text = f"Player 2 Wins!\n"
                        player1_text = f"Player 1 Score: {scores[0]}"
                        player2_text = f"Player 2 Score: {scores[1]}"
                        player1_color = "#D2B4DE"
                        player2_color = "darkred"
                    else:
                        # 修改前：winner_text = f"平局！\n"
                        winner_text = f"Tie!\n"
                        player1_text = f"Player 1 Score: {scores[0]}"
                        player2_text = f"Player 2 Score: {scores[1]}"
                        player1_color = "#D2B4DE"
                        player2_color = "#D2B4DE"

                    winner_label = tk.Label(result_window, text=winner_text, font=('Comic Sans MS', 14), bg="#F8EDE3", fg="darkred")
                    winner_label.pack(pady=5)

                    player1_label = tk.Label(result_window, text=player1_text, font=('Comic Sans MS', 14), bg="#F8EDE3", fg=player1_color)
                    player1_label.pack(pady=5)

                    player2_label = tk.Label(result_window, text=player2_text, font=('Comic Sans MS', 14), bg="#F8EDE3", fg=player2_color)
                    player2_label.pack(pady=5)

                    next_game_button = tk.Button(result_window, text="Next Game", command=lambda: (result_window.destroy(), self.reset_game()), bg="#D2B4DE", fg="#F8EDE3", font=('Comic Sans MS', 14))
                    next_game_button.pack(pady=20)
                else:
                    self.current_player = 1 - self.current_player
                    self.turn_label.config(text=f"Player {self.current_player + 1}, please enter a letter")
                self.confirm_buttons[player].config(state='disabled')

            self.update_board_colors()

    def reset_game(self):
        self.players_boards = [[[' ' for _ in range(5)] for _ in range(5)] for _ in range(2)]
        self.current_letter.set('')
        self.current_player = 0
        self.remaining_spaces = 25
        self.waiting_for_player2 = False
        self.temp_placement = [None, None]

        prompt_text = "Player 1, please enter a letter"
        light_brown_color = "#E9DCC9"  # 浅黄棕色
        original_color = "#D2B4DE"  # 原粉紫配色
        original_text_color = "#8B4513"  # 原字母颜色
        disabled_text_color = "white"  # 棕黄配色时的字母颜色

        for i in range(2):
            board = self.players_boards[i]
            if "please enter a letter" in prompt_text:
                base_color = light_brown_color
                text_color = disabled_text_color

            for row in range(5):
                self.row_score_labels[i][row].config(text="0", bg=base_color, fg=text_color)
            for col in range(5):
                self.col_score_labels[i][col].config(text="0", bg=base_color, fg=text_color)
            self.total_score_labels[i].config(text=f"Player {i + 1} Total Score: 0")
            self.confirm_buttons[i].config(state='disabled')

        for player in range(2):
            for row in range(5):
                for col in range(5):
                    self.boards[player][row][col].config(text=' ', fg="black")

        self.turn_label.config(text="Player 1, please enter a letter")
        self.letter_entry.config(state='normal')
        self.letter_entry.delete(0, tk.END)
        self.update_board_colors()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()