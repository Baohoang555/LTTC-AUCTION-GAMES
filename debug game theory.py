import random

# --- Player Class ---
class Player:
    def __init__(self, id, money):
        self.id = id
        self.money = money
        self.original_money = money
        self.won_items = []  # ds các món đã thắng
        self.target_items = [] 

    def win_item(self, item_id, price):
        self.won_items.append(item_id)  # Thêm món đã thắng vào ds
        self.money -= price  # Giảm tiền còn lại sau khi thắng món

    def show_history(self):
        # Hiển thị lịch sử và tiền còn lại
        print(f"Người chơi {self.id} đã thắng các món: {self.won_items}")
        print(f"Tiền còn lại: {self.money}")
        print(f"Mục tiêu cần thắng: {self.target_items}")

# --- Khởi tạo dữ liệu ---
def initialize_game(num_players=3, num_items=5):
    players = [Player(i, random.randint(70, 120)) for i in range(num_players)]
    items = [f"Món hàng {i}" for i in range(num_items)]
    min_prices = [random.randint(15, 30) for _ in range(num_items)]
    
    # Gán mục tiêu cho từng người chơi (2 món ngẫu nhiên)
    for player in players:
        player.target_items = random.sample(range(num_items), 2)
    
    return players, items, min_prices

# --- Ví dụ về việc thắng món ---
def simulate_auction(player, item_id, bid_price, min_price, items):
    if bid_price >= min_price and bid_price <= player.money:
        player.win_item(item_id, bid_price)  # Người chơi thắng món
        print(f"Người chơi {player.id} đã thắng {items[item_id]} với giá {bid_price}")
    else:
        print(f"Người chơi {player.id} không thể thắng món {items[item_id]}")

# --- So sánh kết quả thắng thua ---
def compare_results(players):
    max_wins = max(len(player.won_items) for player in players)
    winners = [player for player in players if len(player.won_items) == max_wins]

    if len(winners) > 1:
        print("Có nhiều người chơi thắng cùng số món:")
        for winner in winners:
            print(f"Người chơi {winner.id} với {len(winner.won_items)} món thắng.")
    else:
        print(f"Người chơi {winners[0].id} là người thắng cuộc với {len(winners[0].won_items)} món thắng.")

# --- Kiểm thử toàn bộ luồng chơi ---
def play_game():
    players, items, min_prices = initialize_game()
    
    # Mô phỏng các vòng đấu giá
    for current_item in range(len(items)):
        print(f"\n💎 Đang đấu giá: {items[current_item]} | 💵 Giá sàn: {min_prices[current_item]}")
        for player in players:
            # Đặt giá ngẫu nhiên trong khoảng hợp lệ
            if player.money >= min_prices[current_item]:
                bid_price = random.randint(min_prices[current_item], player.money)  # Đặt giá ngẫu nhiên
                simulate_auction(player, current_item, bid_price, min_prices[current_item], items)
            else:
                print(f"Người chơi {player.id} không đủ tiền để tham gia đấu giá cho {items[current_item]}.")

    # Hiển thị lịch sử của từng người chơi
    for player in players:
        player.show_history()

    # So sánh kết quả thắng thua
    compare_results(players)

# --- Chức năng Chơi lại ---
def restart_game():
    print("\n🔄 Đang khởi động lại trò chơi...")
    play_game()

# --- Chạy kiểm thử ---
play_game()

# Gọi chức năng Chơi lại
restart_game()
