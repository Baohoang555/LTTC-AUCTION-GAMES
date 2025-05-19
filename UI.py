import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("🎮 Trò chơi Đấu giá - Lý thuyết Trò chơi")
root.geometry("560x420")

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_welcome_screen():
    clear_frame(main_frame)
    tk.Label(main_frame, text="Chào mừng đến với trò chơi Đấu Giá!", font=("Arial", 18, "bold")).pack(pady=30)
    tk.Label(main_frame, text="Hãy thử vận may và chiến thuật để chiến thắng các món hàng mục tiêu!", font=("Arial", 12)).pack(pady=10)
    tk.Button(
        main_frame,
        text="Chơi",
        font=("Arial", 14),
        width=12,
        command=show_player_selection
    ).pack(pady=30)
    
def show_player_selection():
    clear_frame(main_frame)
    tk.Label(main_frame, text="Chọn người chơi", font=("Arial", 16)).pack(pady=10)

    for i in range(3):
        tk.Button(
            main_frame,
            text=f"Người chơi {i+1}",
            font=("Arial", 12),
            width=20,
            command=lambda i=i: choose_player(i)
        ).pack(pady=5)

def show_auction_screen():
    clear_frame(main_frame)
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
    won_items = [str(i) for i in user.won_items]
    target_items = [str(i) for i in user_target_items]
    target_items_won = len(set(user_target_items).intersection(user.won_items))

    # Thông báo thắng/thua
    if target_items_won == len(user_target_items):
        tk.Label(main_frame, text="Chúc mừng! Bạn đã thắng trò chơi!", font=("Arial", 14), fg="green").pack(pady=5)
    else:
        tk.Label(main_frame, text="Rất tiếc! Bạn đã thua trò chơi!", font=("Arial", 14), fg="red").pack(pady=5)

    # Hiển thị danh sách các món đã thắng
    tk.Label(
        main_frame,
        text="Bạn đã thắng món: " + (", ".join(won_items) if won_items else "Không có"),
        font=("Arial", 12)
    ).pack(pady=3)

    # Hiển thị mục tiêu cần thắng
    tk.Label(
        main_frame,
        text="Mục tiêu cần: " + (", ".join(target_items)),
        font=("Arial", 12)
    ).pack(pady=3)

    # Hiển thị số món mục tiêu đã thắng
    tk.Label(
        main_frame,
        text=f"Số món mục tiêu đã thắng: {target_items_won}/{len(user_target_items)}",
        font=("Arial", 12)
    ).pack(pady=3)

    # Hiển thị số tiền còn lại
    tk.Label(
        main_frame,
        text=f"Số tiền còn lại: {user.money}",
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Button(
        main_frame,
        text="Chơi lại",
        font=("Arial", 12),
        command=restart_game
    ).pack(pady=10)

# --- Khởi động ---
show_welcome_screen()
root.mainloop()