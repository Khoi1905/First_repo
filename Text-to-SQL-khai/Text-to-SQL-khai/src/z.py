


def get_all_table_summaries():
    table_summaries = [
        {
            "table_id": "users",
            "description": "Chứa thông tin người dùng: id, tên, email, ngày tạo tài khoản.",
            "columns": ["id", "name", "email", "created_at"]
        },
        {
            "table_id": "orders",
            "description": "Chứa thông tin đơn hàng: id, id người dùng, tổng tiền, trạng thái, ngày tạo đơn.",
            "columns": ["id", "user_id", "total_amount", "status", "created_at"]
        }
    ]
    return table_summaries

def get_table_details(table_ids):
    table_descriptions = [
        {
            "table_id": "users",
            "description": "Bảng lưu trữ thông tin chi tiết về từng người dùng đã đăng ký trên hệ thống.",
            "columns": [
                {"name": "id", "type": "INTEGER", "description": "Khóa chính (Primary Key), định danh duy nhất cho mỗi người dùng.", "example": 101, "primary_key": True, "nullable": False},
                {"name": "name", "type": "TEXT", "description": "Họ và tên đầy đủ của người dùng.", "example": "Nguyễn Văn A", "nullable": False},
                {"name": "email", "type": "TEXT", "description": "Địa chỉ email duy nhất của người dùng (unique).", "example": "vana@example.com", "unique": True, "nullable": False},
                {"name": "created_at", "type": "DATETIME", "description": "Thời điểm tài khoản được tạo trên hệ thống.", "example": "2023-09-27 14:22:00", "nullable": False}
            ],
            "note": "Mỗi người dùng chỉ có một tài khoản duy nhất trong hệ thống.",
        },
        {
            "table_id": "orders",
            "description": "Bảng lưu trữ tất cả các đơn hàng được đặt bởi người dùng",
            "columns": [
                {"name": "id", "type": "INTEGER", "description": "Khóa chính (Primary Key), định danh duy nhất cho mỗi đơn hàng", "example": 5001, "primary_key": True, "nullable": False},
                {"name": "user_id", "type": "INTEGER", "description": "Khóa ngoại (Foreign Key), liên kết tới người dùng đặt đơn (users.id).", "example": 101, "foreign_key": "users.id", "nullable": False},
                {"name": "total_amount", "type": "FLOAT", "description": "Tổng số tiền của đơn hàng (đơn vị: VNĐ hoặc USD tùy hệ thống).", "example": 1500000.0, "nullable": False},
                {"name": "status", "type": "TEXT", "description": "Trạng thái hiện tại của đơn hàng. Có thể là: 'pending' (chờ xử lý), 'completed' (hoàn tất), 'cancelled' (đã hủy), ...", "example": "completed", "nullable": False},
                {"name": "created_at", "type": "DATETIME", "description": "Thời điểm đơn hàng được tạo.", "example": "2023-09-27 15:10:30", "nullable": False},
            ],
            "note": "Mỗi đơn hàng thuộc về một người dùng. Khi xóa user, cần cân nhắc về dữ liệu đơn hàng liên quan."
        }
    ]

    return [table for table in table_descriptions if table["table_id"] in table_ids]

