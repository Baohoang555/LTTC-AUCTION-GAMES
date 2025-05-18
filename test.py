import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import time
import os

# --- MVC: Logic Layer ---
class Player:
    def __init__(self, id, money):
        self.id = id
        self.money = money
        self.original_money = money
        self.won_items = []

    def win_item(self, item_id, price):
        self.won_items.append(item_id)
        self.money -= price

class AuctionGame:
    def __init__(self, num_players=3, num_items=5, difficulty="Medium", timer=15):
        self.num_players = num_players
        self.num_items = num_items
        self.difficulty = difficulty
        self.timer_duration = timer
        self.reset()
        self.load_scores()

    def reset(self):
        self.players = [Player(i, random.randint(70, 120)) for i in range(self.num_players)]
        self.items = [f"Món hàng {i}" for i in range(self.num_items)]
        self.min_prices = [random.randint(15, 30) for _ in range(self.num_items)]
        self.current_item = 0
        self.user = None
        self.user_skipped = False
        self.history = []
        self.user_interest = {i: 0 for i in range(self.num_items)}
        self.INTEREST_THRESHOLD = 2

    def set_user(self, player_id):
        self.user = self.players[player_id]
        self.targets = random.sample(range(self.num_items), 2)

    def get_bids(self, user_bid=None):
        item_id = self.current_item
        floor = self.min_prices[item_id]
        bids = []
        for p in self.players:
            if p == self.user:
                bids.append(user_bid)
            else:
                if p.money < floor:
                    bids.append(0)
                else:
                    low, high = floor, floor + (30 if self.difficulty == "Easy" else 30 if self.difficulty == "Medium" else 40)
                    if self.user_skipped:
                        low += 10
                        high += 10
                    if self.user_interest[item_id] >= self.INTEREST_THRESHOLD:
                        low += 10
                        high += 10
                    bid = random.randint(low, min(high, p.money))
                    bids.append(bid)
        return bids

    def submit(self, bid):
        item_id = self.current_item
        floor = self.min_prices[item_id]
        if bid - floor > 5:
            self.user_interest[item_id] += 1
        bids = self.get_bids(bid)
        winner = max(range(len(bids)), key=lambda i: bids[i])
        price = bids[winner]
        if winner == 0:
            self.user.win_item(item_id, bid)
            result = (True, bid)
        else:
            self.players[winner].win_item(item_id, price)
            result = (False, price)
        self.history.append({"item": item_id, "bids": bids.copy(), "winner": winner, "price": price})
        self.user_skipped = False
        self.current_item += 1
        return result

    def skip(self):
        self.user_skipped = True
        self.history.append({"item": self.current_item, "bids": "skipped"})
        self.current_item += 1

    def is_over(self):
        return self.current_item >= self.num_items

    def save_score(self):
        score = len(set(self.user.won_items) & set(self.targets))
        record = {"date": time.strftime("%Y-%m-%d %H:%M"), "player": self.user.id, "score": score}
        self.scores.append(record)
        with open('scores.json', 'w') as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=2)

    def load_scores(self):
        if os.path.exists('scores.json'):
            with open('scores.json', 'r') as f:
                self.scores = json.load(f)
        else:
            self.scores = []

# --- UI Layer ---
class AuctionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎮 Trò chơi Đấu giá - MVC & Tiến Hóa")
        self.geometry("700x500")
        self.game = AuctionGame()
        self.create_widgets()

    def create_widgets(self):
        self.main = ttk.Frame(self)
        self.main.pack(fill='both', expand=True, padx=10, pady=10)
        self.show_player_select()

    def clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    def show_player_select(self):
        self.clear()
        ttk.Label(self.main, text="Chọn Player", font=(None, 16)).pack(pady=10)
        for i in range(self.game.num_players):
            ttk.Button(self.main, text=f"Player {i}", command=lambda i=i: self.start(i)).pack(pady=5)

    def start(self, pid):
        self.game.reset()
        self.game.set_user(pid)
        self.show_auction()

    def show_auction(self):
        self.clear()
        item = self.game.items[self.game.current_item]
        floor = self.game.min_prices[self.game.current_item]
        ttk.Label(self.main, text=f"Mục tiêu: {self.game.targets}").pack()
        ttk.Label(self.main, text=f"Player {self.game.user.id} | Tiền: {self.game.user.money}").pack()
        ttk.Label(self.main, text=f"Đấu giá: {item}").pack(pady=5)
        ttk.Label(self.main, text=f"Giá sàn: {floor}").pack()
        self.bid_var = tk.IntVar()
        ttk.Entry(self.main, textvariable=self.bid_var).pack(pady=5)
        ttk.Button(self.main, text="Đặt giá", command=self.on_bid).pack(side='left', padx=10)
        ttk.Button(self.main, text="Bỏ qua", command=self.on_skip).pack(side='left')
        self.start_timer()

    def start_timer(self):
        self.remaining = self.game.timer_duration
        self.timer_lbl = ttk.Label(self.main, text=f"Thời gian: {self.remaining}")
        self.timer_lbl.pack(pady=5)
        self._countdown()

    def _countdown(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.timer_lbl.config(text=f"Thời gian: {self.remaining}")
            self.after(1000, self._countdown)
        else:
            self.on_skip()

    def on_bid(self):
        bid = self.bid_var.get()
        ok, price = self.game.submit(bid)
        messagebox.showinfo("Kết quả", f"{'Win' if ok else 'Lose'} giá: {price}")
        self.next_or_end()

    def on_skip(self):
        self.game.skip()
        self.next_or_end()

    def next_or_end(self):
        if self.game.is_over():
            self.show_result()
        else:
            self.show_auction()

    def show_result(self):
        self.clear()
        won = self.game.user.won_items
        tgt = self.game.targets
        match = len(set(won) & set(tgt))
        ttk.Label(self.main, text=f"Bạn thắng: {won}").pack()
        ttk.Label(self.main, text=f"Mục tiêu: {tgt}").pack()
        ttk.Label(self.main, text=f"Đúng: {match}").pack()
        ttk.Button(self.main, text="Chơi lại", command=self.show_player_select).pack()
        self.game.save_score()
        ttk.Button(self.main, text="Xem BXH", command=self.show_scores).pack(pady=5)

    def show_scores(self):
        self.clear()
        cols = ("date", "player", "score")
        for c in cols:
            ttk.Label(self.main, text=c).grid(row=0, column=cols.index(c))
        for i, r in enumerate(self.game.scores):
            for j, c in enumerate(cols):
                ttk.Label(self.main, text=r[c]).grid(row=i+1, column=j)
        ttk.Button(self.main, text="Quay lại", command=self.show_player_select).grid(row=len(self.game.scores)+1, column=0)

if __name__ == "__main__":
    app = AuctionApp()
    app.mainloop()
