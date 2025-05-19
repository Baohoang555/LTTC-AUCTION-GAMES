import tkinter as tk
from tkinter import messagebox
import random

# Trò chơi mô phỏng một tình huống đấu giá trong môi trường cạnh tranh, nơi người chơi cần sử dụng chiến lược hợp lý để chiến thắng các món hàng mục tiêu. Trò chơi được
# thiết kế theo góc nhìn của lý thuyết trò chơi (Game Theory), trong đó người chơi không chỉ phải tính toán khả năng tài chính mà còn phải cân nhắc các hành vi của đối
# thủ và ảnh hưởng của hành vi của mình lên chiến lược của AI.
# --- Player Class ---
class Player:
    def __init__(self, id, money):
        self.id = id
        self.money = money
        self.original_money = money
        self.won_items = []

    def win_item(self, item_id, price):
        self.won_items.append(item_id)
        self.money -= price
#  Cấu trúc dữ liệu

# Lớp Player: Mỗi người chơi có id, số tiền ban đầu (money), và danh sách các món hàng đã chiến thắng (won_items).

# --- Khởi tạo dữ liệu ---
players = [Player(i, random.randint(70,120)) for i in range(3)]
items = [f"Món hàng {i}" for i in range(5)]
min_prices = [random.randint(15,30) for _ in range(5)]


# Danh sách người chơi: Gồm 3 người chơi được khởi tạo với số tiền ngẫu nhiên từ 70 đến 120.
# Món hàng đấu giá: Có 5 món hàng với giá sàn ngẫu nhiên từ 15 đến 30.


user = None
user_target_items = []
current_item = 0
user_skipped_last_round = False

user_interest_score = {i: 0 for i in range(5)}  # AI theo dõi hành vi người chơi
INTEREST_THRESHOLD = 2  # Ngưỡng nghi ngờ người chơi cần món này

# --- Giao diện ---
root = tk.Tk()
root.title("🎮 Trò chơi Đấu giá - Lý thuyết Trò chơi")
root.geometry("560x420")

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# --- Chọn người chơi ---
def choose_player(player_id):
    global user, user_target_items
    user = players[player_id]
    user_target_items = random.sample(range(5), 2)
    show_auction_screen()
    

# Hệ thống sẽ chọn ngẫu nhiên 2 món hàng mà người chơi cần giành chiến thắng (được lưu trong user_target_items).


def show_player_selection():
    clear_frame(main_frame)
    tk.Label(main_frame, text="🧍 Chọn người chơi của bạn", font=("Arial", 14)).pack(pady=10)
    for i in range(3):
        tk.Button(main_frame, text=f"Player {i}", font=("Arial", 12),
                  command=lambda i=i: choose_player(i)).pack(pady=5)
        
            
# Chọn người chơi và xác định mục tiêu
# Khi bắt đầu, người chơi sẽ chọn một trong 3 người chơi để đại diện.

# --- Đấu giá ---
def submit_bid():
    global current_item, user_skipped_last_round
    try:
        bid = int(bid_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ.")
        return

    item_price = min_prices[current_item]
    if bid < item_price:
        messagebox.showwarning("❌ Giá thấp quá", f"Giá sàn là {item_price}.")
        return
    if bid > user.money:
        messagebox.showwarning("❌ Thiếu tiền", "Bạn không đủ tiền.")
        return

    # AI học hành vi người chơi
    if bid - item_price > 5:
        user_interest_score[current_item] += 1
# Việc theo dõi user_interest_score thể hiện tính năng learning (học hành vi) của đối thủ AI.
# Đây là một mô hình đơn giản của học máy (machine learning theo luật IF-ELSE), cho phép AI điều chỉnh chiến lược để gây khó khăn cho người chơi.

    # AI đấu giá
    opponents = [p for p in players if p != user]
    opponent_bids = []
    for p in opponents:
        if p.money >= item_price:
            # Logic AI
            if user_skipped_last_round:
                lower = item_price + 10
                upper = item_price + 40
            else:
                lower = item_price
                upper = item_price + 30

            # Nếu nghi ngờ bạn cần món này -> AI đặt giá cao hơn để gây nhiễu
            if user_interest_score.get(current_item, 0) >= INTEREST_THRESHOLD:
                lower += 10
                upper += 10

            opp_bid = random.randint(lower, min(p.money, upper))
        else:
            opp_bid = 0
        opponent_bids.append(opp_bid)
# Chiến lược "Gây nhiễu"
# Khi phát hiện người chơi quan tâm đến món hàng, AI nâng giá vượt lên để người chơi phải trả giá cao hoặc bỏ lỡ món hàng quan trọng.
# Điều này tạo nên một mô hình đấu giá cạnh tranh không hợp tác, đúng tinh thần của Nash Equilibrium: mỗi bên cố tối ưu kết quả của mình dựa vào phán đoán
# hành vi của đối phương.
    all_bids = [bid] + opponent_bids
    winner_index = all_bids.index(max(all_bids))
    price_paid = all_bids[winner_index]

    if winner_index == 0:
        user.win_item(current_item, bid)
        messagebox.showinfo("✅ Kết quả", f"Bạn đã thắng {items[current_item]} với giá {bid}")
    else:
        opponents[winner_index - 1].win_item(current_item, price_paid)
        messagebox.showinfo("❌ Kết quả", f"Bạn đã thua. Đối thủ thắng {items[current_item]} với giá {price_paid}")

    user_skipped_last_round = False
    next_item()

def skip_bid():
    global user_skipped_last_round
    user_skipped_last_round = True
    next_item()

def next_item():
    global current_item
    current_item += 1
    if current_item < len(items):
        show_auction_screen()
    else:
        show_result()
#  Vòng đấu giá
# Mỗi vòng đấu giá diễn ra trên một món hàng (tuần tự theo danh sách).
# Người chơi có thể: Nhập giá và đấu giá.Hoặc bỏ qua (skip).

# Xử lý giá người chơi
# Nếu giá người chơi < giá sàn ⇒ bị cảnh báo.
# Nếu giá > số tiền hiện có ⇒ cảnh báo thiếu tiền.
# Nếu giá đặt cao hơn giá sàn nhiều (cụ thể > 5 đơn vị) ⇒ được xem là biểu hiện quan tâm cao → tăng điểm nghi ngờ (user_interest_score) với món hàng đó.

#Chiến lược của đối thủ (AI)
# AI sẽ đặt giá trong một khoảng nhất định, tùy vào:
# Tình huống vòng trước: Nếu người chơi đã bỏ qua, AI sẽ tăng cường đặt giá cao hơn (do đoán người chơi muốn để dành tiền).
# Điểm nghi ngờ: Nếu AI phát hiện người chơi có vẻ muốn món hàng này (qua số lần ra giá cao) → sẽ cố tình đấu giá cao hơn để gây nhiễu.


#Cách tính kết quả vòng
# SSo sánh tất cả giá đặt: Người có giá cao nhất thắng, và bị trừ tiền tương ứng.
#Nếu người chơi thắng ⇒ thêm món hàng vào danh sách user.won_items.

# --- Màn hình đấu giá ---
def show_auction_screen():
    clear_frame(main_frame)
    tk.Label(main_frame, text="Chào mừng đến với trò chơi Đấu Giá!", font=("Arial", 18, "bold")).pack(pady=30)
    tk.Label(main_frame, text="Hãy thử vận may và chiến thuật để chiến thắng các món hàng mục tiêu!", font=("Arial", 12)).pack(pady=10)
    tk.Label(main_frame, text=f"🎯 Mục tiêu: thắng món {user_target_items[0]} và {user_target_items[1]}",
             font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(main_frame, text=f"🧍 Bạn là Player {user.id} | 💰 Tiền: {user.money}", font=("Arial", 11)).pack(pady=5)

    tk.Label(main_frame, text=f"💎 Đang đấu giá: {items[current_item]}", font=("Arial", 13, "bold")).pack(pady=10)
    tk.Label(main_frame, text=f"💵 Giá sàn: {min_prices[current_item]}", font=("Arial", 11)).pack()

    global bid_entry
    bid_entry = tk.Entry(main_frame, font=("Arial", 12))
    bid_entry.pack(pady=10)

    tk.Button(main_frame, text="💰 Đặt giá", command=submit_bid).pack(pady=5)
    tk.Button(main_frame, text="⏭️ Bỏ qua", command=skip_bid).pack(pady=5)

# --- Kết quả ---
def show_result():
    clear_frame(main_frame)
    win_items = set(user.won_items)
    goal_items = set(user_target_items)
    matched = win_items & goal_items

    tk.Label(main_frame, text="📊 KẾT QUẢ", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(main_frame, text=f"Bạn đã thắng các món: {sorted(user.won_items)}", font=("Arial", 12)).pack()
    tk.Label(main_frame, text=f"Mục tiêu cần: {sorted(user_target_items)}", font=("Arial", 12)).pack()
    tk.Label(main_frame, text=f"Số món mục tiêu đã thắng: {len(matched)}", font=("Arial", 12)).pack()

    if len(matched) >= 2:
        tk.Label(main_frame, text="🏆 CHÚC MỪNG! BẠN ĐÃ THẮNG!", font=("Arial", 14), fg="green").pack(pady=10)
    else:
        tk.Label(main_frame, text="❌ BẠN ĐÃ THUA! HẸN GẶP LẠI.", font=("Arial", 14), fg="red").pack(pady=10)

    tk.Button(main_frame, text="🔁 Chơi lại", command=restart_game).pack(pady=10)

def restart_game():
    global players, user, user_target_items, current_item, user_skipped_last_round, user_interest_score
    players = [Player(i, random.randint(70, 120)) for i in range(3)]
    user = None
    user_target_items = []
    current_item = 0
    user_skipped_last_round = False
    user_interest_score = {i: 0 for i in range(5)}
    show_player_selection()

# --- Khởi động ---
show_player_selection()
root.mainloop()
# Tổng kết ưu điểm và tiềm năng mở rộng
# Ưu điểm:
# Giao diện trực quan, thân thiện với người học.
# AI có yếu tố "học hành vi" đơn giản, giúp người chơi học cách ẩn giấu ý định và tư duy chiến lược.
# Hệ thống có thể tái khởi động và chơi lại nhiều lần với dữ liệu ngẫu nhiên.

# Tiềm năng mở rộng:
# Thêm hệ thống đấu giá theo vòng kín (sealed-bid auction).
# Tăng số món hàng, số người chơi, hoặc áp dụng thuật toán học tăng cường (reinforcement learning) cho AI.
# Hiển thị biểu đồ hoặc thống kê để giúp người chơi học lý thuyết trò chơi hiệu quả hơn.