import sys
import os

# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app import models

BLOGS_SEED = [
    {
        "title": "Top 10 Công cụ AI hỗ trợ tự động hóa vận hành doanh nghiệp năm 2026",
        "handle": "top-10-cong-cu-ai-tu-dong-hoa-doanh-nghiep-2026",
        "category": "AI 2026",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop",
        "excerpt": "Tổng hợp các công cụ Trí tuệ nhân tạo (AI) giúp tối ưu hóa quy trình làm việc, giảm thời gian xử lý thủ công và gia tăng năng suất doanh nghiệp vượt trội.",
        "date": "05/10/2026",
        "link": "/blog/top-10-cong-cu-ai-tu-dong-hoa-doanh-nghiep-2026",
        "content": """
<h2>1. Tổng quan về làn sóng AI Automation 2026</h2>
<p>Năm 2026 đánh dấu sự bùng nổ của các mô hình AI agent tự động hóa quy trình phức tạp end-to-end trong doanh nghiệp. Việc ứng dụng AI không còn dừng lại ở mức thử nghiệm hay trò chuyện đơn thuần, mà đã trở thành <strong>yếu tố sinh tồn</strong> quyết định năng lực cạnh tranh của mọi tổ chức.</p>

<h2>2. Các nhóm công cụ AI trọng tâm</h2>
<ul>
  <li><strong>Xử lý dữ liệu & Báo cáo:</strong> Tự động làm sạch, phân tích và trích xuất thông tin từ file Excel, PDF, dữ liệu ERP.</li>
  <li><strong>Tự động hóa chăm sóc khách hàng:</strong> AI Agent phản hồi đa kênh 24/7 với ngữ cảnh chuyên sâu.</li>
  <li><strong>Soạn thảo & Truyền thông nội bộ:</strong> Tạo lập văn bản hành chính, slide thuyết trình và nội dung marketing chuẩn thương hiệu.</li>
</ul>

<h2>3. Lộ trình triển khai hiệu quả cho quản lý</h2>
<p>Để triển khai thành công, các nhà quản lý nên bắt đầu từ việc chuẩn hóa quy trình nội bộ, sau đó lựa chọn 1-2 bài toán lặp lại nhiều nhất để thử nghiệm tự động hóa với AI trước khi mở rộng toàn diện.</p>
"""
    },
    {
        "title": "Ứng dụng ChatGPT & Claude 3.5 trong phân tích dữ liệu kinh doanh cho nhà quản lý",
        "handle": "ung-dung-chatgpt-claude-phan-tich-du-lieu-kinh-doanh",
        "category": "Công cụ AI",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop",
        "excerpt": "Hướng dẫn chi tiết cách viết prompt chuyên sâu để biến AI thành trợ lý phân tích tài chính và dự báo doanh thu thực chiến.",
        "date": "02/10/2026",
        "link": "/blog/ung-dung-chatgpt-claude-phan-tich-du-lieu-kinh-doanh",
        "content": """
<h2>Tối ưu hóa năng lực phân tích với Prompt Engineering</h2>
<p>Các công cụ như Claude 3.5 Sonnet và ChatGPT-4o có khả năng xử lý các bảng tính hàng triệu hàng và trích xuất các insight kinh doanh đắt giá chỉ trong vài giây.</p>

<h3>Các dạng bài toán phổ biến:</h3>
<ul>
  <li>Dự báo xu hướng doanh thu dựa trên dữ liệu lịch sử.</li>
  <li>Phân nhóm khách hàng mục tiêu và hành vi tiêu dùng.</li>
  <li>Phát hiện bất thường và rủi ro dòng tiền trong doanh nghiệp.</li>
</ul>

<p>Học viện ACC đã thiết kế quy trình 5 bước viết Prompt phân tích dữ liệu chuẩn giúp học viên tiết kiệm 80% thời gian làm báo cáo hàng tuần.</p>
"""
    },
    {
        "title": "Bí quyết xây dựng tư duy Lãnh đạo trong kỷ nguyên AI & Chuyển đổi số",
        "handle": "bi-quyet-xay-dung-tu-duy-lanh-dao-ky-nguyen-ai",
        "category": "Lãnh đạo & Quản lý",
        "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=800&auto=format&fit=crop",
        "excerpt": "Làm thế nào để nhà quản lý định hướng đội ngũ, thúc đẩy văn hóa đổi mới sáng tạo và áp dụng thành công AI vào mô hình kinh doanh?",
        "date": "28/09/2026",
        "link": "/blog/bi-quyet-xay-dung-tu-duy-lanh-dao-ky-nguyen-ai",
        "content": """
<h2>Thách thức của nhà quản lý hiện đại</h2>
<p>Sự phát triển nhanh chóng của công nghệ đòi hỏi người lãnh đạo không chỉ hiểu về công cụ mà phải sở hữu <strong>tư duy thiết kế quy trình (Process Design Thinking)</strong> và năng lực dẫn dắt sự thay đổi.</p>

<h2>3 Trụ cột văn hóa doanh nghiệp thời đại AI</h2>
<ul>
  <li><strong>Cởi mở & Thử nghiệm:</strong> Khuyến khích nhân sự chủ động tìm kiếm giải pháp AI mới cho công việc hàng ngày.</li>
  <li><strong>Bảo mật & Trách nhiệm:</strong> Xây dựng bộ quy tắc ứng xử và bảo vệ dữ liệu khách hàng khi dùng AI.</li>
  <li><strong>Học tập liên tục:</strong> Cập nhật liên tục các khóa bồi dưỡng ngắn hạn để không bị tụt hậu.</li>
</ul>
"""
    },
    {
        "title": "Cách tối ưu 8 giờ làm việc thành 3 giờ nhờ quy trình tự động hóa cá nhân",
        "handle": "toi-uu-8-gio-lam-viec-thanh-3-gio-nho-ai",
        "category": "Làm việc hiệu suất",
        "image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=800&auto=format&fit=crop",
        "excerpt": "Khám phá các phương pháp sắp xếp công việc thông minh, kết hợp AI để giải phóng thời gian cho những nhiệm vụ chiến lược.",
        "date": "20/09/2026",
        "link": "/blog/toi-uu-8-gio-lam-viec-thanh-3-gio-nho-ai",
        "content": """
<h2>Chiến lược loại bỏ công việc lặp lại</h2>
<p>Bằng cách kết hợp Zapier/Make cùng với ChatGPT, bạn có thể tự động hóa 90% công việc xử lý email, tổng hợp lịch hẹn và soạn thảo tài liệu phản hồi ban đầu.</p>

<p>Tham khảo ngay các mẫu workflow tự động hóa làm việc hiệu suất tại kho tài nguyên của ACC Academy!</p>
"""
    }
]

def seed_blogs_only():
    print("Seeding blog_posts table ONLY...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if content column exists in blog_posts, if not add it via ALTER TABLE
        from sqlalchemy import text
        try:
            db.execute(text("SELECT content FROM blog_posts LIMIT 1;"))
        except Exception:
            db.rollback()
            print("Adding missing 'content' column to 'blog_posts' table...")
            db.execute(text("ALTER TABLE blog_posts ADD COLUMN content TEXT NULL;"))
            db.commit()

        # Clear existing blog_posts table to ensure clean state
        db.query(models.BlogPost).delete()
        db.commit()

        count = 0
        for blog_data in BLOGS_SEED:
            blog = models.BlogPost(**blog_data)
            db.add(blog)
            count += 1
        db.commit()
        print(f"Successfully seeded {count} blog posts into database!")
    except Exception as e:
        db.rollback()
        print("Error seeding blog posts:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_blogs_only()
