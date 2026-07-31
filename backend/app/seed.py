import sys
import os
# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app import models

# Sample data translated from Pinia store (courses.js)
CATEGORIES_SEED = [
    {"slug": "ky-nang-ai", "name": "Kỹ năng AI"},
    {"slug": "ky-nang-mem", "name": "Kỹ năng mềm"},
    {"slug": "ky-nang-chuyen-mon", "name": "Kỹ năng chuyên môn"},
    {"slug": "bundles", "name": "Combo khóa học"}
]

COURSES_SEED = [
    # Kỹ năng AI
    {
        "id": 10800458137911,
        "title": "AI Center of Excellence: Lộ Trình Quản Trị & Vận Hành AI Cho Doanh Nghiệp",
        "category_slug": "ky-nang-ai",
        "handle": "ai-center-of-excellence",
        "price": 3629000,
        "original_price": 4500000,
        "image": "/images/Square-Cover-_1.webp",
        "tags": ["Course", "E-learning", "Quản trị AI"],
        "description": "Lộ trình toàn diện để tích hợp, quản trị và vận hành các mô hình trí tuệ nhân tạo (AI) hiệu quả trong cơ cấu doanh nghiệp hiện đại.",
        "duration": "6 tuần",
        "level": "Nâng cao"
    },
    {
        "id": 10800448438583,
        "title": "ChatGPT Work Automation: 10X Tốc độ hoàn thành công việc với ChatGPT & hệ sinh thái OpenAI",
        "category_slug": "ky-nang-ai",
        "handle": "chatgpt-work-automation",
        "price": 3449000,
        "original_price": 4200000,
        "image": "/images/Square_Cover_b1dc8f1b-edc2-473f-ada7-6756dae8a281.png",
        "tags": ["Codex", "E-learning", "Kỹ năng AI", "Trí tuệ nhân tạo (AI)"],
        "description": "Làm chủ các prompt chuyên sâu để tự động hóa soạn thảo, phân tích tài liệu và tối ưu hóa hiệu suất làm việc văn phòng với ChatGPT.",
        "duration": "5 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 10681994740023,
        "title": "Gen AI Studio: X5 Số Lượng Hình Ảnh, Video Mà Không Tăng Thêm Chi Phí Và Nguồn Lực",
        "category_slug": "ky-nang-ai",
        "handle": "gen-ai-studio",
        "price": 3249000,
        "original_price": 3800000,
        "image": "/images/Square-Cover_c232d7ad-fa2d-4744-b359-5ee042cd9eda.webp",
        "tags": ["AI Creative", "Beginner", "E-learning", "Trí tuệ nhân tạo (AI)"],
        "description": "Khai phá sức mạnh của AI trong thiết kế hình ảnh, sản xuất video tự động, giúp tối giản chi phí marketing và tăng năng suất nội dung.",
        "duration": "4 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10523458044215,
        "title": "Claude Productivity: X2 Chất lượng công việc với cộng sự điều hành Claude AI",
        "category_slug": "ky-nang-ai",
        "handle": "claude-productivity",
        "price": 3449000,
        "original_price": 4000000,
        "image": "/images/Claude_Productivity.png",
        "tags": ["Course", "Intermediate", "Productivity", "Trí tuệ nhân tạo (AI)"],
        "description": "Sử dụng Claude AI như một trợ lý thông minh hỗ trợ xử lý dữ liệu phức tạp, xây dựng nội dung chất lượng cao và quản lý dự án.",
        "duration": "4 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10454235545911,
        "title": "AI Workflows for Business Operations",
        "category_slug": "ky-nang-ai",
        "handle": "ai-workflow-operations",
        "price": 1999000,
        "original_price": 2500000,
        "image": "/images/AIW2_c1252e7c-2e62-4a53-8846-496332c851a1.png",
        "tags": ["Advanced", "E-learning", "Trí tuệ nhân tạo (AI)", "Workflow"],
        "description": "Thiết kế các quy trình tự động hóa vận hành doanh nghiệp bằng cách kết hợp AI với các hệ thống hiện tại.",
        "duration": "5 tuần",
        "level": "Nâng cao"
    },
    {
        "id": 10382239858999,
        "title": "Gemini Productivity: X5 Hiệu suất làm việc với hệ sinh thái Google AI",
        "category_slug": "ky-nang-ai",
        "handle": "gemini-productivity",
        "price": 2699000,
        "original_price": 3200000,
        "image": "/images/Gemini_Productivity.png",
        "tags": ["Automation", "Beginner", "E-learning", "Productivity", "Trí tuệ nhân tạo (AI)"],
        "description": "Tận dụng tối đa Google Workspace tích hợp Gemini để làm việc nhóm hiệu quả, lập kế hoạch và quản lý email thông minh.",
        "duration": "4 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10322225529143,
        "title": "Khoá học AI Survival Kit - Bộ 6 kỹ năng sống còn thời AI",
        "category_slug": "ky-nang-ai",
        "handle": "khoa-hoc-ai-survival-kit",
        "price": 1599000,
        "original_price": 2000000,
        "image": "/images/AI_Survival_Kit_a9bbf9b4-480d-4467-9571-804887d45212.png",
        "tags": ["Beginner", "E-learning", "Trí tuệ nhân tạo (AI)"],
        "description": "Trang bị đầy đủ kiến thức và kỹ năng cơ bản nhất để thích ứng và phát triển trong kỷ nguyên trí tuệ nhân tạo bùng nổ.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10296150753591,
        "title": "Khoá học AI Workflow Automation - Tự động hóa quy trình với Zapier, Make AI, N8N",
        "category_slug": "ky-nang-ai",
        "handle": "ai-workflow-automation",
        "price": 1799000,
        "original_price": 2200000,
        "image": "/images/AI_Workflow_Automation_8decdc78-096c-4924-9bf9-128ca34359a4.png",
        "tags": ["E-learning", "Intermediate", "Trí tuệ nhân tạo (AI)", "Workflow Automation"],
        "description": "Kết nối các ứng dụng và xây dựng luồng công việc tự động hóa hoàn toàn không cần code thông qua Zapier và Make.",
        "duration": "5 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10202599489847,
        "title": "Khóa học Data Processing - X5 Hiệu suất xử lý dữ liệu với AI",
        "category_slug": "ky-nang-ai",
        "handle": "data-processing",
        "price": 950000,
        "original_price": 1500000,
        "image": "/images/Data_Processing.png",
        "tags": ["Beginner", "Data", "E-learning", "Trí tuệ nhân tạo (AI)"],
        "description": "Học cách thu thập, làm sạch và phân tích dữ liệu lớn nhanh chóng bằng các công cụ hỗ trợ AI.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },

    # Kỹ năng mềm
    {
        "id": 8250507854135,
        "title": "Khóa học Thuyết Trình Thuyết Phục Chuyên Nghiệp",
        "category_slug": "ky-nang-mem",
        "handle": "khoa-hoc-ky-nang-thuyet-trinh-thuyet-phuc",
        "price": 3990000,
        "original_price": 4800000,
        "image": "/images/7_3fd889db-0fdf-43aa-867f-67d166f045c7.png",
        "tags": ["Giao tiếp", "Quản lý - Lãnh đạo", "Thuyết trình"],
        "description": "Làm chủ giọng nói, ngôn ngữ cơ thể và cấu trúc slide logic để cuốn hút và thuyết phục mọi đối tượng khán giả.",
        "duration": "6 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 8027323826487,
        "title": "Giao Tiếp Khéo Léo – Chinh Phục Cấp Trên, Dẫn Dắt Cấp Dưới",
        "category_slug": "ky-nang-mem",
        "handle": "khoa-hoc-giao-tiep-tao-anh-huong",
        "price": 3990000,
        "original_price": 4500000,
        "image": "/images/6_76841af7-348d-4ff0-960c-2bc1b568e791.png",
        "tags": ["Giao tiếp", "Quản lý - Lãnh đạo"],
        "description": "Nghệ thuật giao tiếp ứng xử thông minh nơi công sở, giúp xây dựng lòng tin với sếp và tạo động lực cho nhân viên.",
        "duration": "5 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 8152702583095,
        "title": "Lập Kế Hoạch Quản Lý Dự Án – Nghệ Thuật Quản Trị Chuyên Nghiệp",
        "category_slug": "ky-nang-mem",
        "handle": "khoa-hoc-lap-ke-hoach-quan-ly-chuyen-nghiep",
        "price": 4990000,
        "original_price": 5800000,
        "image": "/images/5_6aae1a70-ead0-4301-96ae-b697f7767949.png",
        "tags": ["Quản lý", "Quản lý - Lãnh đạo", "Dự án"],
        "description": "Phương pháp lập tiến độ, quản trị rủi ro và điều phối tài nguyên dự án một cách khoa học, đúng tiến độ.",
        "duration": "6 tuần",
        "level": "Trung cấp"
    },

    # Kỹ năng chuyên môn
    {
        "id": 10249474572599,
        "title": "Looker Studio for Everyone (Google data studio) - 1 Click Tự Động Hoá Báo Cáo",
        "category_slug": "ky-nang-chuyen-mon",
        "handle": "looker-studio-for-everyone",
        "price": 1799000,
        "original_price": 2400000,
        "image": "/images/LS_Looker_Studio_for_Everyone_SQR.png",
        "tags": ["Data Visualization", "E-learning", "Intermediate", "Dashboard"],
        "description": "Học cách kết nối các nguồn dữ liệu khác nhau và tự động hóa toàn bộ hệ thống báo cáo trực quan trong 1 click.",
        "duration": "4 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10376862499127,
        "title": "Khoá học Excel AI - Làm chủ kỹ năng Excel với AI",
        "category_slug": "ky-nang-chuyen-mon",
        "handle": "excel-ai",
        "price": 569000,
        "original_price": 900000,
        "image": "/images/Excell_skill_e9651cdc-6ff9-48ed-9e96-d4e0b6419a41.png",
        "tags": ["Course", "Thinkific", "Excel AI"],
        "description": "Kết hợp sức mạnh AI vào Excel giúp viết hàm nhanh chóng, xử lý dữ liệu tự động và lập báo cáo thần tốc.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },

    # Combos / Bundles
    {
        "id": 10205877633335,
        "title": "Data Bootcamp - Combo 2 khoá học AI For Decision Making và Data Processing",
        "category_slug": "bundles",
        "handle": "data-bootcamp",
        "price": 3659000,
        "original_price": 4500000,
        "image": "/images/Data_Bootcamp.png",
        "tags": ["Beginner", "Combo", "Data", "AI", "Video on-demand"],
        "description": "Combo hoàn hảo giúp bạn nâng tầm tư duy số, tự động hóa xử lý dữ liệu và đưa ra quyết định dựa trên số liệu thực tế.",
        "duration": "8 tuần",
        "level": "Cơ bản - Trung cấp"
    }
]

BLOG_POSTS_SEED = [
    {
        "id": 101,
        "title": "1 Giờ Tạo TVC Với AI! (Không Cần Máy Quay, Studio, Ekip)",
        "handle": "1-gio-tao-tvc-voi-ai",
        "category": "AI Automation",
        "excerpt": "Trong bài viết này, Linh sẽ chia sẻ với các bạn cách tạo TVC chuyên nghiệp với AI mà ai...",
        "image": "/images/LBVA-Thumbnail_5_d0857985-e0a2-437b-b9f1-a37aafcfea88.png",
        "date": "Jul 15, 2026",
        "link": "#/blog/1-gio-tao-tvc-voi-ai"
    },
    {
        "id": 102,
        "title": "Khi AI Copilot Trở Thành Trợ Lý Chiến Lược Tại Amway",
        "handle": "khi-ai-copilot-tro-thanh-tro-ly-chien-luoc",
        "category": "Lãnh đạo & Quản lý",
        "excerpt": "Nhằm hiện thực hóa chiến lược này, ACC Academy đã vinh dự đồng hành cùng đội ngũ nhân sự Amway...",
        "image": "/images/Blog_Thumbnail_12_39a02613-d986-43b8-8462-bdb4046a2153.png",
        "date": "Jul 14, 2026",
        "link": "#/blog/khi-ai-copilot-tro-thanh-tro-ly-chien-luoc"
    },
    {
        "id": 103,
        "title": "Kimi K2.6: AI Giúp Bạn Làm Web, Slide Và AI Skills",
        "handle": "kimi-ai",
        "category": "Công cụ AI",
        "excerpt": "Khi nhắc đến AI, thì ai cũng biết ChatGPT, Gemini, Claude hay Deep Seek. Nhưng bạn đã biết đến Kimi...",
        "image": "/images/AI_Tut_Thumbnail_72f219cc-a95d-41ae-a7b5-8f1699cdde97.png",
        "date": "Jul 10, 2026",
        "link": "#/blog/kimi-ai"
    }
]

def seed_database():
    print("Initializing Database tables...")
    # This will create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Seed Categories
        print("Seeding categories...")
        for cat_data in CATEGORIES_SEED:
            existing = db.query(models.Category).filter(models.Category.slug == cat_data["slug"]).first()
            if not existing:
                cat = models.Category(slug=cat_data["slug"], name=cat_data["name"])
                db.add(cat)
        db.commit()

        # 2. Seed Courses
        print("Seeding courses...")
        for course_data in COURSES_SEED:
            existing = db.query(models.Course).filter(models.Course.id == course_data["id"]).first()
            if not existing:
                course = models.Course(
                    id=course_data["id"],
                    title=course_data["title"],
                    category_slug=course_data["category_slug"],
                    handle=course_data["handle"],
                    price=course_data["price"],
                    original_price=course_data["original_price"],
                    image=course_data["image"],
                    description=course_data["description"],
                    duration=course_data["duration"],
                    level=course_data["level"]
                )
                db.add(course)
                db.flush() # Get session persistence to relate tags
                
                for tag_name in course_data["tags"]:
                    tag = models.CourseTag(course_id=course.id, tag=tag_name)
                    db.add(tag)
        db.commit()

        # 3. Seed Blogs
        print("Seeding blog posts...")
        for blog_data in BLOG_POSTS_SEED:
            existing = db.query(models.BlogPost).filter(models.BlogPost.id == blog_data["id"]).first()
            if not existing:
                blog = models.BlogPost(
                    id=blog_data["id"],
                    title=blog_data["title"],
                    handle=blog_data["handle"],
                    category=blog_data["category"],
                    excerpt=blog_data["excerpt"],
                    image=blog_data["image"],
                    date=blog_data["date"],
                    link=blog_data["link"]
                )
                db.add(blog)
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
