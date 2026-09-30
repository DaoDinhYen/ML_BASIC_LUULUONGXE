"""
Chương trình: run_option_b.py
Mô tả: Khởi chạy riêng biệt Phương án B: 3D Khối Đồ họa Thành phố & Cao tốc Three.js / WebGL.
       Chạy tại cổng 8002 (hoặc kết nối backend chính).
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
import webbrowser
from pathlib import Path
import uvicorn
from fastapi.responses import FileResponse

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Nạp ứng dụng FastAPI gốc chứa đầy đủ các API suy luận (/api/traffic-forecast, /api/health, ...)
from app.backend import app as main_app

# Tạo route chính tại root cho Phương án B nếu cần
FRONTEND_B_DIR = PROJECT_ROOT / "frontend_option_b"

@main_app.get("/standalone-b", include_in_schema=False)
def serve_option_b_root():
    index_file = FRONTEND_B_DIR / "index.html"
    return FileResponse(str(index_file))

if __name__ == "__main__":
    port = 8002
    url = f"http://127.0.0.1:{port}/option-b"
    print("=" * 75)
    print("🚀 ĐANG KHỞI CHẠY PHƯƠNG ÁN B: 3D THREE.JS WEBGL THÀNH PHỐ & CAO TỐC I-94")
    print("=" * 75)
    print(f"👉 Mở trình duyệt Web tại: {url}")
    print(f"   (Hoặc truy cập: http://127.0.0.1:{port}/)")
    print("=" * 75)
    
    try:
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run("app.backend:app", host="127.0.0.1", port=port, reload=False)
