import sys
import os
# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app import models

# Sample data translated from Pinia store (courses.js)
CATEGORIES_SEED = [
    {"slug": "dao-tao-doanh-nghiep", "name": "Đào tạo cho doanh nghiệp"},
    {"slug": "dao-tao-ca-nhan", "name": "Đào tạo cho cá nhân"},
    {"slug": "dao-tao-co-quan-nha-nuoc", "name": "Đào tạo cho khối cơ quan - nhà nước"},
    {"slug": "bundles", "name": "Combo khóa học"}
]

COURSES_SEED = [
    # 1. Đào tạo cho doanh nghiệp
    {
        "id": 10800458137911,
        "title": "AI Center of Excellence: Lộ Trình Quản Trị & Vận Hành AI Cho Doanh Nghiệp",
        "category_slug": "dao-tao-doanh-nghiep",
        "handle": "ai-center-of-excellence",
        "price": 3629000,
        "original_price": 4500000,
        "image": "/images/Square-Cover-_1.webp",
        "tags": ["Doanh nghiệp", "Quản trị AI", "CoE"],
        "description": "Lộ trình toàn diện để tích hợp, quản trị và vận hành các mô hình trí tuệ nhân tạo (AI) hiệu quả trong cơ cấu doanh nghiệp hiện đại.",
        "duration": "6 tuần",
        "level": "Nâng cao"
    },
    {
        "id": 10800448438583,
        "title": "ChatGPT Work Automation: 10X Tốc độ hoàn thành công việc với ChatGPT & hệ sinh thái OpenAI",
        "category_slug": "dao-tao-doanh-nghiep",
        "handle": "chatgpt-work-automation",
        "price": 3449000,
        "original_price": 4200000,
        "image": "/images/Square_Cover_b1dc8f1b-edc2-473f-ada7-6756dae8a281.png",
        "tags": ["Doanh nghiệp", "Tự động hóa", "Kỹ năng AI"],
        "description": "Làm chủ các prompt chuyên sâu để tự động hóa soạn thảo, phân tích tài liệu và tối ưu hóa hiệu suất làm việc văn phòng với ChatGPT.",
        "duration": "5 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 10681994740023,
        "title": "Gen AI Studio: X5 Số Lượng Hình Ảnh, Video Cho Marketing & Doanh Nghiệp",
        "category_slug": "dao-tao-doanh-nghiep",
        "handle": "gen-ai-studio",
        "price": 3249000,
        "original_price": 3800000,
        "image": "/images/Square-Cover_c232d7ad-fa2d-4744-b359-5ee042cd9eda.webp",
        "tags": ["Doanh nghiệp", "AI Creative", "Marketing"],
        "description": "Khai phá sức mạnh của AI trong thiết kế hình ảnh, sản xuất video tự động, giúp tối giản chi phí marketing và tăng năng suất nội dung.",
        "duration": "4 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10454235545911,
        "title": "AI Workflows for Business Operations",
        "category_slug": "dao-tao-doanh-nghiep",
        "handle": "ai-workflow-operations",
        "price": 1999000,
        "original_price": 2500000,
        "image": "/images/AIW2_c1252e7c-2e62-4a53-8846-496332c851a1.png",
        "tags": ["Doanh nghiệp", "Workflow", "Vận hành"],
        "description": "Thiết kế các quy trình tự động hóa vận hành doanh nghiệp bằng cách kết hợp AI với các hệ thống hiện tại.",
        "duration": "5 tuần",
        "level": "Nâng cao"
    },
    {
        "id": 8152702583095,
        "title": "Lập Kế Hoạch Quản Lý Dự Án – Nghệ Thuật Quản Trị Chuyên Nghiệp",
        "category_slug": "dao-tao-doanh-nghiep",
        "handle": "khoa-hoc-lap-ke-hoach-quan-ly-chuyen-nghiep",
        "price": 4990000,
        "original_price": 5800000,
        "image": "/images/5_6aae1a70-ead0-4301-96ae-b697f7767949.png",
        "tags": ["Doanh nghiệp", "Quản lý dự án", "Lãnh đạo"],
        "description": "Phương pháp lập tiến độ, quản trị rủi ro và điều phối tài nguyên dự án một cách khoa học, đúng tiến độ.",
        "duration": "6 tuần",
        "level": "Trung cấp"
    },

    # 2. Đào tạo cho cá nhân
    {
        "id": 10523458044215,
        "title": "Claude Productivity: X2 Chất lượng công việc với cộng sự điều hành Claude AI",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "claude-productivity",
        "price": 3449000,
        "original_price": 4000000,
        "image": "/images/Claude_Productivity.png",
        "tags": ["Cá nhân", "Productivity", "Claude AI"],
        "description": "Sử dụng Claude AI như một trợ lý thông minh hỗ trợ xử lý dữ liệu phức tạp, xây dựng nội dung chất lượng cao và quản lý dự án.",
        "duration": "4 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10382239858999,
        "title": "Gemini Productivity: X5 Hiệu suất làm việc với hệ sinh thái Google AI",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "gemini-productivity",
        "price": 2699000,
        "original_price": 3200000,
        "image": "/images/Gemini_Productivity.png",
        "tags": ["Cá nhân", "Google Workspace", "Gemini"],
        "description": "Tận dụng tối đa Google Workspace tích hợp Gemini để làm việc nhóm hiệu quả, lập kế hoạch và quản lý email thông minh.",
        "duration": "4 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10322225529143,
        "title": "Khoá học AI Survival Kit - Bộ 6 kỹ năng sống còn thời AI",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "khoa-hoc-ai-survival-kit",
        "price": 1599000,
        "original_price": 2000000,
        "image": "/images/AI_Survival_Kit_a9bbf9b4-480d-4467-9571-804887d45212.png",
        "tags": ["Cá nhân", "Kỹ năng sống còn", "Beginner"],
        "description": "Trang bị đầy đủ kiến thức và kỹ năng cơ bản nhất để thích ứng và phát triển trong kỷ nguyên trí tuệ nhân tạo bùng nổ.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 10296150753591,
        "title": "Khoá học AI Workflow Automation - Tự động hóa quy trình cá nhân",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "ai-workflow-automation",
        "price": 1799000,
        "original_price": 2200000,
        "image": "/images/AI_Workflow_Automation_8decdc78-096c-4924-9bf9-128ca34359a4.png",
        "tags": ["Cá nhân", "Make", "Zapier"],
        "description": "Kết nối các ứng dụng và xây dựng luồng công việc tự động hóa hoàn toàn không cần code thông qua Zapier và Make.",
        "duration": "5 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10202599489847,
        "title": "Khóa học Data Processing - X5 Hiệu suất xử lý dữ liệu với AI",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "data-processing",
        "price": 950000,
        "original_price": 1500000,
        "image": "/images/Data_Processing.png",
        "tags": ["Cá nhân", "Dữ liệu", "AI Tools"],
        "description": "Học cách thu thập, làm sạch và phân tích dữ liệu lớn nhanh chóng bằng các công cụ hỗ trợ AI.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },
    {
        "id": 8250507854135,
        "title": "Khóa học Thuyết Trình Thuyết Phục Chuyên Nghiệp",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "khoa-hoc-ky-nang-thuyet-trinh-thuyet-phuc",
        "price": 3990000,
        "original_price": 4800000,
        "image": "/images/7_3fd889db-0fdf-43aa-867f-67d166f045c7.png",
        "tags": ["Cá nhân", "Thuyết trình", "Giao tiếp"],
        "description": "Làm chủ giọng nói, ngôn ngữ cơ thể và cấu trúc slide logic để cuốn hút và thuyết phục mọi đối tượng khán giả.",
        "duration": "6 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 8027323826487,
        "title": "Giao Tiếp Khéo Léo – Chinh Phục Cấp Trên, Dẫn Dắt Cấp Dưới",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "khoa-hoc-giao-tiep-tao-anh-huong",
        "price": 3990000,
        "original_price": 4500000,
        "image": "/images/6_76841af7-348d-4ff0-960c-2bc1b568e791.png",
        "tags": ["Cá nhân", "Ứng xử", "Công sở"],
        "description": "Nghệ thuật giao tiếp ứng xử thông minh nơi công sở, giúp xây dựng lòng tin với sếp và tạo động lực cho đồng nghiệp.",
        "duration": "5 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 10249474572599,
        "title": "Looker Studio for Everyone - 1 Click Tự Động Hoá Báo Cáo",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "looker-studio-for-everyone",
        "price": 1799000,
        "original_price": 2400000,
        "image": "/images/LS_Looker_Studio_for_Everyone_SQR.png",
        "tags": ["Cá nhân", "Dashboard", "Looker Studio"],
        "description": "Học cách kết nối các nguồn dữ liệu khác nhau và tự động hóa toàn bộ hệ thống báo cáo trực quan trong 1 click.",
        "duration": "4 tuần",
        "level": "Trung cấp"
    },
    {
        "id": 10376862499127,
        "title": "Khoá học Excel AI - Làm chủ kỹ năng Excel với AI",
        "category_slug": "dao-tao-ca-nhan",
        "handle": "excel-ai",
        "price": 569000,
        "original_price": 900000,
        "image": "/images/Excell_skill_e9651cdc-6ff9-48ed-9e96-d4e0b6419a41.png",
        "tags": ["Cá nhân", "Excel AI", "Kỹ năng văn phòng"],
        "description": "Kết hợp sức mạnh AI vào Excel giúp viết hàm nhanh chóng, xử lý dữ liệu tự động và lập báo cáo thần tốc.",
        "duration": "3 tuần",
        "level": "Cơ bản"
    },

    # 3. Đào tạo cho khối cơ quan - nhà nước
    {
        "id": 1090011112222,
        "title": "Đào Tạo AI & Tự Động Hóa Hành Chính Cho Khối Cơ Quan Nhà Nước",
        "category_slug": "dao-tao-co-quan-nha-nuoc",
        "handle": "ai-hanh-chinh-nha-nuoc",
        "price": 3890000,
        "original_price": 4800000,
        "image": "/images/CoE-Web.png",
        "tags": ["Cơ quan nhà nước", "Hành chính công", "AI"],
        "description": "Lộ trình đào tạo chuyên biệt hỗ trợ cán bộ công chức ứng dụng AI xử lý hồ sơ, văn bản hành chính và chuẩn hóa dịch vụ công.",
        "duration": "5 tuần",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 1090033334444,
        "title": "Quản Trị & Bảo Mật Dữ Liệu Số Trong Cơ Quan Công Quyền",
        "category_slug": "dao-tao-co-quan-nha-nuoc",
        "handle": "quan-tri-du-lieu-nha-nuoc",
        "price": 4200000,
        "original_price": 5000000,
        "image": "/images/Square-Cover-_1.webp",
        "tags": ["Cơ quan nhà nước", "Bảo mật", "Chuyển đổi số"],
        "description": "Khóa huấn luyện chuyên sâu về an toàn thông tin, bảo mật dữ liệu công quyền và tuân thủ Nghị định bảo vệ dữ liệu cá nhân trong đơn vị hành chính.",
        "duration": "6 tuần",
        "level": "Nâng cao"
    },
    {
        "id": 1090055556666,
        "title": "Xây Dựng Khung Năng Lực Số & Chuyển Đổi Số Khối Cơ Quan - Nhà Nước",
        "category_slug": "dao-tao-co-quan-nha-nuoc",
        "handle": "khung-nang-luc-so-nha-nuoc",
        "price": 3500000,
        "original_price": 4500000,
        "image": "/images/Leader_Shift.webp",
        "tags": ["Cơ quan nhà nước", "Khung năng lực số", "Chính phủ số"],
        "description": "Hệ thống ma trận năng lực số và lộ trình nâng cao năng lực công nghệ cho đội ngũ lãnh đạo, quản lý khối cơ quan nhà nước và đơn vị sự nghiệp công lập.",
        "duration": "4 tuần",
        "level": "Trung cấp"
    },

    # Combos / Bundles
    {
        "id": 9000000000001,
        "title": "Bundle 2026 Master VIP Tất Cả Khóa Học",
        "category_slug": "bundles",
        "handle": "bundle-2026-master",
        "price": 5990000,
        "original_price": 15900000,
        "image": "/images/Data_Bootcamp.png",
        "tags": ["VIP", "Combo", "Bundle"],
        "description": "Sở hữu trọn bộ tất cả các khóa học cao cấp tại ACC Academy với đặc quyền cập nhật kiến thức mới miễn phí trong suốt năm 2026.",
        "duration": "Trọn đời",
        "level": "Tất cả trình độ"
    },
    {
        "id": 9000000000002,
        "title": "AI & Automation Master Bundle",
        "category_slug": "bundles",
        "handle": "ai-master-bundle",
        "price": 3990000,
        "original_price": 9800000,
        "image": "/images/Square_Cover_b1dc8f1b-edc2-473f-ada7-6756dae8a281.png",
        "tags": ["AI", "Combo", "Automation"],
        "description": "Trọn bộ các khóa học AI cốt lõi: ChatGPT Work Automation, AI COE, Gen AI Studio và Claude Productivity.",
        "duration": "Trọn đời",
        "level": "Cơ bản - Nâng cao"
    },
    {
        "id": 9000000000003,
        "title": "Data Bootcamp - Combo AI For Decision Making & Data Processing",
        "category_slug": "bundles",
        "handle": "data-bootcamp-combo",
        "price": 4500000,
        "original_price": 8400000,
        "image": "/images/Data_Bootcamp.png",
        "tags": ["Data", "Combo", "AI"],
        "description": "Combo toàn diện xử lý dữ liệu tự động, xây dựng Dashboard Looker Studio và ứng dụng AI ra quyết định kinh doanh.",
        "duration": "Trọn đời",
        "level": "Cơ bản - Trung cấp"
    },
    {
        "id": 9000000000004,
        "title": "Combo Quản Trị & Lãnh Đạo Chuyên Nghiệp",
        "category_slug": "bundles",
        "handle": "leadership-master-combo",
        "price": 3200000,
        "original_price": 6800000,
        "image": "/images/Leader_Shift.webp",
        "tags": ["Management", "Combo", "Leadership"],
        "description": "Lộ trình nâng cao năng lực lãnh đạo, giao tiếp thuyết phục cấp trên và quản trị dự án hiệu quả.",
        "duration": "Trọn đời",
        "level": "Cơ bản - Nâng cao"
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

TESTIMONIALS_SEED = [
    # Video Feedback YouTube
    {
        "name": "Nguyễn Văn Hoàng",
        "role": "Giám đốc Vận hành (COO)",
        "company": "VinaLogistics Corp",
        "text": "Chia sẻ từ Học viên về tính thực chiến của khóa học AI",
        "testimonial_type": "video",
        "youtube_id": "BC9rvc1F3dA",
        "thumbnail": "https://img.youtube.com/vi/BC9rvc1F3dA/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/BC9rvc1F3dA?autoplay=1",
        "course_name": "Khóa học Generative AI trong Quản trị",
        "rating": 5
    },
    {
        "name": "Lê Thị Thu Trang",
        "role": "Trưởng phòng Marketing",
        "company": "Tập đoàn Bất động sản SunLand",
        "text": "Học viên nhận xét về đội ngũ Giảng viên ACC Academy",
        "testimonial_type": "video",
        "youtube_id": "HaSNGppB85E",
        "thumbnail": "https://img.youtube.com/vi/HaSNGppB85E/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/HaSNGppB85E?autoplay=1",
        "course_name": "Chương trình Đào tạo In-house cho Doanh nghiệp",
        "rating": 5
    },
    {
        "name": "Phạm Đức Anh",
        "role": "Founder & CEO",
        "company": "TechGrowth Solution",
        "text": "Tối ưu hiệu suất 300% sau khóa học AI Productivity",
        "testimonial_type": "video",
        "youtube_id": "93oV5sP--HE",
        "thumbnail": "https://img.youtube.com/vi/93oV5sP--HE/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/93oV5sP--HE?autoplay=1",
        "course_name": "AI Productivity Mastery 1:1",
        "rating": 5
    },
    {
        "name": "Đặng Ngọc Minh",
        "role": "Giám đốc Nhân sự (CHRO)",
        "company": "Tập đoàn Tài chính ACB",
        "text": "Đánh giá chương trình Đào tạo Lãnh đạo Chuyển đổi số",
        "testimonial_type": "video",
        "youtube_id": "HSSUMQVDWDo",
        "thumbnail": "https://img.youtube.com/vi/HSSUMQVDWDo/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/HSSUMQVDWDo?autoplay=1",
        "course_name": "MBA Andrews & Khung năng lực Số",
        "rating": 5
    },
    {
        "name": "Trần Quốc Bảo",
        "role": "Chủ tịch HĐQT",
        "company": "Bảo Phát Group",
        "text": "Cảm nhận Học viên về giải pháp may đo cho Doanh nghiệp",
        "testimonial_type": "video",
        "youtube_id": "4ZKYSjoDHtw",
        "thumbnail": "https://img.youtube.com/vi/4ZKYSjoDHtw/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/4ZKYSjoDHtw?autoplay=1",
        "course_name": "Chương trình Đào tạo Doanh nghiệp May đo",
        "rating": 5
    },
    {
        "name": "Vũ Thị Mai Phương",
        "role": "Giám đốc Khối Kinh doanh",
        "company": "Pháp lý & Đầu tư An Việt",
        "text": "Trải nghiệm học ứng dụng ChatGPT & Claude tại ACC",
        "testimonial_type": "video",
        "youtube_id": "WbBCGAYIMCk",
        "thumbnail": "https://img.youtube.com/vi/WbBCGAYIMCk/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/WbBCGAYIMCk?autoplay=1",
        "course_name": "Khóa học AI Skills Cho Doanh Nhân",
        "rating": 5
    },
    {
        "name": "Nguyễn Thành Nam",
        "role": "Kỹ sư Trưởng Vận hành",
        "company": "Bosch Việt Nam",
        "text": "Phản hồi từ Học viên khóa Tư duy Phản biện & 8D Problem Solving",
        "testimonial_type": "video",
        "youtube_id": "u-vPXxsbKLI",
        "thumbnail": "https://img.youtube.com/vi/u-vPXxsbKLI/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/u-vPXxsbKLI?autoplay=1",
        "course_name": "Huấn luyện Kỹ năng Giải quyết Vấn đề",
        "rating": 5
    },
    {
        "name": "Phan Văn Hùng",
        "role": "Phó Trưởng phòng Chuyển đổi số",
        "company": "Khối Cơ quan - Nhà nước",
        "text": "Phản hồi Học viên về Chương trình Đào tạo Khối Cơ quan Nhà nước",
        "testimonial_type": "video",
        "youtube_id": "mpPmDOKkGoM",
        "thumbnail": "https://img.youtube.com/vi/mpPmDOKkGoM/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/mpPmDOKkGoM?autoplay=1",
        "course_name": "Bồi dưỡng Năng lực Số & An toàn Dữ liệu",
        "rating": 5
    },
    {
        "name": "Hoàng Kim Liên",
        "role": "Giám đốc Sáng tạo Content",
        "company": "Media Digital Network",
        "text": "Cảm nhận thực tế của Học viên về hệ thống tài liệu & trợ lý AI",
        "testimonial_type": "video",
        "youtube_id": "MKS-5t7vvr0",
        "thumbnail": "https://img.youtube.com/vi/MKS-5t7vvr0/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/MKS-5t7vvr0?autoplay=1",
        "course_name": "Công thức Prompt & Trợ lý AI Cá nhân",
        "rating": 5
    },
    {
        "name": "Đỗ Tuấn Anh",
        "role": "Tổng Giám đốc (CEO)",
        "company": "Tập đoàn Công nghệ NextGen",
        "text": "Tổng kết đánh giá từ các Lãnh đạo Doanh nghiệp sau khóa học",
        "testimonial_type": "video",
        "youtube_id": "Zt9JgDisfHk",
        "thumbnail": "https://img.youtube.com/vi/Zt9JgDisfHk/hqdefault.jpg",
        "video_url": "https://www.youtube.com/embed/Zt9JgDisfHk?autoplay=1",
        "course_name": "AI Leadership & Tự động hóa Vận hành",
        "rating": 5
    },

    # Photo Feedbacks
    {
        "name": "Nguyễn Thanh Tùng",
        "role": "Founder & CEO",
        "company": "TechVision Group",
        "text": "Chương trình ứng dụng AI trong quản trị doanh nghiệp tại ACC Academy đã giúp chúng tôi tối ưu 40% chi phí vận hành nhân sự và tăng tốc độ làm việc vượt bậc!",
        "quote": "Chương trình ứng dụng AI trong quản trị doanh nghiệp tại ACC Academy đã giúp chúng tôi tối ưu 40% chi phí vận hành nhân sự và tăng tốc độ làm việc vượt bậc!",
        "image": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=800&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "course_name": "Khóa học AI Skills Cho Doanh Nhân",
        "testimonial_type": "photo"
    },
    {
        "name": "Trần Minh Đức",
        "role": "Chủ tịch HĐQT",
        "company": "Alpha Media & Marketing",
        "text": "Kiến thức thực chiến, đóng gói quy trình chuẩn hóa. Cảm ơn đội ngũ giảng viên ACC Academy đã tư vấn cực kỳ tận tâm!",
        "quote": "Kiến thức thực chiến, đóng gói quy trình chuẩn hóa. Cảm ơn đội ngũ giảng viên ACC Academy đã tư vấn cực kỳ tận tâm!",
        "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "course_name": "Chương Trình Đào Tạo Doanh Nghiệp",
        "testimonial_type": "photo"
    },
    {
        "name": "Hoàng Anh Thư",
        "role": "KOL & Content Creator",
        "company": "1.2M Followers TikTok",
        "text": "Kho khóa học và thư viện prompt của ACC là vũ khí bí mật giúp tôi sản xuất nội dung chuyên nghiệp hàng ngày!",
        "quote": "Kho khóa học và thư viện prompt của ACC là vũ khí bí mật giúp tôi sản xuất nội dung chuyên nghiệp hàng ngày!",
        "image": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
        "rating": 5,
        "course_name": "Ebook & Công thức Prompt",
        "testimonial_type": "photo"
    },
    {
        "name": "Lê Hồng Minh",
        "role": "Founder & CEO",
        "company": "VNG Corporation",
        "text": "Đội ngũ kỹ sư và nhân viên VNG đã cải thiện vượt bậc hiệu suất làm việc nhờ các khóa học và quy trình tự động hóa được thiết kế bởi ACC Academy.",
        "image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=400&auto=format&fit=crop",
        "rating": 5,
        "testimonial_type": "text"
    }
]

LECTURERS_SEED = [
    {
        "id": "nguyen-tan-binh",
        "name": "TS. Nguyễn Tấn Bình",
        "title": "Viện trưởng Leadman Institute",
        "tagline": "Viện trưởng Leadman – Viện nghiên cứu khoa học Lãnh đạo và Quản trị doanh nghiệp",
        "avatar": "/images/T-Binh-tach-nen-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Thầy nổi tiếng trong giới giảng viên, doanh nhân, là người có khả năng truyền đạt kiến thức quản trị tài chính, kế toán vốn khô khan với ngôn ngữ gần gũi, truyền cảm hứng.",
        "details_html": "<p>TS. Nguyễn Tấn Bình là Viện trưởng Viện Nghiên cứu Khoa học Lãnh đạo & Quản trị Doanh nghiệp (LEADMAN Institute), chuyên gia hàng đầu về Quản trị Tài chính và Chiến lược Lãnh đạo.</p>"
    },
    {
        "id": "nguyen-vu-huy-hoang",
        "name": "ThS. Nguyễn Vũ Huy Hoàng",
        "title": "Giám đốc Đào tạo ACC Academy & Master AI Trainer",
        "tagline": "Giám đốc Đào tạo - Chuyên gia tư vấn về AI, Xây dựng khung năng lực số và ứng dụng công nghệ trong quản trị doanh nghiệp.",
        "avatar": "https://lh3.googleusercontent.com/d/1NornFFlN9I_tSIDn3WWQUQxfjK5B21vl",
        "avatar_drive_link": "https://drive.google.com/file/d/1NornFFlN9I_tSIDn3WWQUQxfjK5B21vl/view?usp=drive_link",
        "drive_profile": "",
        "bio_short": "Có gần 15 năm kinh nghiệm trong đào tạo, tư vấn quản trị và chuyển đổi số, ông tập trung nghiên cứu và triển khai các giải pháp ứng dụng AI vào quản trị, nhân sự, Marketing, kinh doanh và vận hành.",
        "details_html": "<p>ThS. Nguyễn Vũ Huy Hoàng là Giám đốc Đào tạo ACC Academy, Master AI Trainer và chuyên gia hàng đầu về ứng dụng AI, xây dựng khung năng lực số và quản trị bảo mật dữ liệu doanh nghiệp tại Việt Nam.</p>"
    },
    {
        "id": "do-xuan-tuan",
        "name": "ThS. Nguyễn Anh Tuấn",
        "title": "Chuyên gia Đào tạo Quản trị Vận hành & AI Workflows",
        "tagline": "Chuyên gia huấn luyện tự động hóa quy trình vận hành và ứng dụng AI trong quản trị doanh nghiệp.",
        "avatar": "https://lh3.googleusercontent.com/d/1sGiCe18WnDNjwH_m6c3kwrdgQ5uSRUYA",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Chuyên gia tư vấn tái cấu trúc quy trình vận hành và triển khai AI Workflow cho các tổng công ty và tập đoàn lớn.",
        "details_html": "<p>ThS. Nguyễn Anh Tuấn sở hữu hơn 12 năm kinh nghiệm trong tư vấn quản trị vận hành và tự động hóa quy trình cho doanh nghiệp.</p>"
    },
    {
        "id": "bui-huynh-thuong",
        "name": "Giảng viên Bùi Huỳnh Thương",
        "title": "Chuyên gia đào tạo AI & Phát triển năng lực công nghệ",
        "tagline": "Chuyên gia đào tạo AI và phát triển năng lực ứng dụng công nghệ cho doanh nghiệp.",
        "avatar": "https://lh3.googleusercontent.com/d/1mDIsbAnM-4965taEYhaQvAONqNgD9MKm",
        "avatar_drive_link": "https://drive.google.com/file/d/1mDIsbAnM-4965taEYhaQvAONqNgD9MKm/view?usp=drive_link",
        "drive_profile": "",
        "bio_short": "Tập trung nghiên cứu, đào tạo và triển khai các giải pháp AI phục vụ quản trị, vận hành và nâng cao hiệu suất nhân sự.",
        "details_html": "<p>Giảng viên Bùi Huỳnh Thương là nhà huấn luyện công nghệ tiên phong trong lĩnh vực ứng dụng Generative AI cho đội ngũ nhân sự và quản lý doanh nghiệp.</p>"
    },
    {
        "id": "pham-van-hung",
        "name": "ThS. Phạm Văn Hùng",
        "title": "Chuyên gia Tư vấn Quản trị Chiến lược & Nhân sự",
        "tagline": "Chuyên gia cao cấp về xây dựng khung năng lực nhân sự và chiến lược tăng trưởng doanh nghiệp.",
        "avatar": "/images/thay-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Hơn 15 năm tư vấn khung năng lực nhân sự và huấn luyện đội ngũ quản lý cấp trung tại các doanh nghiệp hàng đầu.",
        "details_html": "<p>ThS. Phạm Văn Hùng chuyên tư vấn tái cấu trúc phòng ban và chuẩn hóa ma trận năng lực cho tổ chức.</p>"
    },
    {
        "id": "helen-lam-hien",
        "name": "Giảng viên Helen Lâm Hiền",
        "title": "Trainer, ICF Coach & Trưởng Bộ môn Marketing & Sales",
        "tagline": "Trainer, ICF Coach – Chuyên gia đào tạo, phát triển năng lực lãnh đạo, Sales & Marketing và ứng dụng AI trong doanh nghiệp.",
        "avatar": "https://lh3.googleusercontent.com/d/1B7vaiEA8KNBUQq_qcNPqHED3ZzhEQTWk",
        "avatar_drive_link": "https://drive.google.com/file/d/1B7vaiEA8KNBUQq_qcNPqHED3ZzhEQTWk/view?usp=drive_link",
        "drive_profile": "",
        "bio_short": "Với hơn 10 năm kinh nghiệm trong Marketing, tư vấn và phát triển tổ chức, cô đã đồng hành cùng nhiều doanh nghiệp trong đào tạo đội ngũ, xây dựng năng lực quản lý.",
        "details_html": "<p>Cô Helen Lâm Hiền là Chuyên gia Đào tạo, Khai vấn Quốc tế ICF Coach và hiện giữ vị trí Trưởng Bộ môn Marketing & Sales tại Học viện ACC.</p>"
    },
    {
        "id": "nguyen-thi-my-dung",
        "name": "ThS. Nguyễn Thị Mỹ Dung",
        "title": "Chuyên gia Softskills, Sale & Thương hiệu",
        "tagline": "Giảng viên, chuyên gia tư vấn về: Softskills, Sale, Thương hiệu",
        "avatar": "/images/chidung-2-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Với hơn 12 năm kinh nghiệm làm việc, đào tạo và dẫn dắt đội ngũ, là quản lý ở các công ty lớn khi tuổi còn rất trẻ.",
        "details_html": "<p>ThS. Nguyễn Thị Mỹ Dung có hơn 12 năm kinh nghiệm điều hành và tư vấn chiến lược Thương hiệu, Kỹ năng mềm và Bán hàng.</p>"
    },
    {
        "id": "nguyen-thi-thu-hoa",
        "name": "Doanh nhân Nguyễn Thị Thu Hoà",
        "title": "Chuyên gia Trải nghiệm khách hàng & Marketing",
        "tagline": "Giảng viên, chuyên gia tư vấn về: Trải nghiệm khách hàng, Bán hàng, Marketing",
        "avatar": "/images/bdh-1-tach-nen-1-400x401.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Hơn 10 năm làm quản lý cấp cao ở các tập đoàn lớn tại Việt Nam khi còn rất trẻ, cô áp dụng phương pháp giảng dạy thực tiễn.",
        "details_html": "<p>Doanh nhân Nguyễn Thị Thu Hoà là chuyên gia cao cấp về Quản trị Trải nghiệm Khách hàng (CX) và Marketing.</p>"
    },
    {
        "id": "do-xuan-hoa",
        "name": "ThS. Đỗ Xuân Hoà",
        "title": "Nhà huấn luyện Lãnh đạo & Soft Skills",
        "tagline": "Giảng viên, nhà huấn luyện về: kỹ năng lãnh đạo, soft skills để làm việc hiệu quả.",
        "avatar": "/images/thaygiao-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Với hơn 17 năm kinh nghiệm giảng dạy các kỹ năng lãnh đạo và quản lý cho các tập đoàn trong và ngoài nước.",
        "details_html": "<p>ThS. Đỗ Xuân Hoà sở hữu hơn 17 năm bề dày kinh nghiệm trong việc đào tạo năng lực Lãnh đạo.</p>"
    },
    {
        "id": "nguyen-hoang-diem",
        "name": "ThS. Nguyễn Hoàng Diễm",
        "title": "Chuyên gia Chăm sóc khách hàng & CRM",
        "tagline": "Giảng viên đào tạo và tư vấn về: Chăm sóc khách hàng và xử lý khiếu nại.",
        "avatar": "/images/DSC3781-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Gần 20 năm kinh nghiệm làm việc và đào tạo tại các tập đoàn lớn ở nhiều lĩnh vực khác nhau.",
        "details_html": "<p>ThS. Nguyễn Hoàng Diễm có gần 20 năm kinh nghiệm thực chiến trong ngành Chăm sóc Khách hàng.</p>"
    },
    {
        "id": "hoang-minh-nghiep",
        "name": "ThS. Hoàng Minh Nghiệp",
        "title": "Chuyên gia Tư vấn Quản lý & Sản xuất",
        "tagline": "Giảng viên, chuyên gia cao cấp về Tư vấn quản lý và sản xuất.",
        "avatar": "/images/thay-400x400.png",
        "avatar_drive_link": "",
        "drive_profile": "",
        "bio_short": "Với 15 năm kinh nghiệm trong ngành sản xuất trải qua nhiều vị trí ở các cấp bậc khác nhau.",
        "details_html": "<p>ThS. Hoàng Minh Nghiệp là cố vấn cao cấp về Tối ưu hóa Sản xuất, Lean Management và Quản trị Vận hành.</p>"
    }
]

PROJECTS_SEED = [
    {
        "id": "dao-tao-ai-acb",
        "category": "du-an-da-thuc-hien",
        "category_name": "Dự án đã thực hiện",
        "title": "Đào tạo ứng dụng Generative AI cho 150+ nhân sự quản lý Tập đoàn ACB",
        "summary": "Giúp bộ phận nhân sự và kinh doanh ứng dụng ChatGPT & Generative AI nâng cao hiệu suất làm việc, tự động hóa báo cáo và phân tích dữ liệu chuyên sâu.",
        "image": "https://drive.google.com/thumbnail?id=120WyoSixRMCuWCMFeNjFKxsDzt74filf&sz=w800",
        "date": "15/08/2026",
        "client": "Tập đoàn Tài chính ACB",
        "drive_profile": "https://drive.google.com/file/d/1p6MtWI5Xk0E00o9TmDhQJA4dFK1j9m0i/view?usp=drive_link",
        "content": '[{"type": "paragraph", "text": "Học viện ACC vừa phối hợp cùng Tập đoàn Tài chính ACB triển khai thành công chương trình đào tạo chuyên sâu Generative AI."}]'
    },
    {
        "id": "khung-nang-luc-so-bosch",
        "category": "du-an-da-thuc-hien",
        "category_name": "Dự án đã thực hiện",
        "title": "Xây dựng Khung năng lực số & Đào tạo Tư duy Phản biện Bosch Việt Nam",
        "summary": "Tư vấn xây dựng ma trận năng lực số và huấn luyện kỹ năng giải quyết vấn đề phức tạp (Problem Solving) theo tiêu chuẩn quốc tế cho đội ngũ kỹ sư Bosch.",
        "image": "https://drive.google.com/thumbnail?id=1ZININwRW94lavoqqoJ3eAArE5v6vsyZ5&sz=w800",
        "date": "28/07/2026",
        "client": "Bosch Việt Nam",
        "drive_profile": "",
        "content": '[{"type": "paragraph", "text": "ACC Academy đã đồng hành cùng Bosch Việt Nam triển khai dự án khảo sát, tư vấn xây dựng ma trận năng lực số."}]'
    }
]


def seed_database():
    print("Initializing Database tables...")
    # This will create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    
    # Auto-add missing columns to existing tables
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(engine)
        with engine.begin() as conn:
            if inspector.has_table("courses"):
                courses_cols = [c["name"] for c in inspector.get_columns("courses")]
                if "program_id" not in courses_cols:
                    conn.execute(text("ALTER TABLE courses ADD COLUMN program_id INT NULL"))
                    print("Migrated: Added program_id column to courses table.")
    except Exception as me:
        print(f"Migration error: {me}")

    db = SessionLocal()
    try:
        # 1. Seed Categories
        print("Seeding categories...")
        for cat_data in CATEGORIES_SEED:
            existing = db.query(models.Category).filter(models.Category.slug == cat_data["slug"]).first()
            if not existing:
                cat = models.Category(slug=cat_data["slug"], name=cat_data["name"])
                db.add(cat)
            else:
                existing.name = cat_data["name"]
        db.commit()

        # 2. Seed Programs & Courses
        print("Seeding programs...")
        prog1 = db.query(models.Program).filter(models.Program.slug == "chuong-trinh-chuyen-gia-ai-2026").first()
        if not prog1:
            prog1 = models.Program(
                title="Chương Trình Đào Tạo Chuyên Gia AI & Tự Động Hóa Doanh Nghiệp 2026",
                slug="chuong-trinh-chuyen-gia-ai-2026",
                description="Lộ trình đào tạo tổng thể từ tư duy ứng dụng AI, làm chủ ChatGPT/Claude/Gemini đến tự động hóa quy trình vận hành toàn doanh nghiệp.",
                image="/images/Square-Cover-_1.webp"
            )
            db.add(prog1)
            db.commit()
            db.refresh(prog1)

        prog2 = db.query(models.Program).filter(models.Program.slug == "chuong-trinh-lanh-dao-quan-tri-2026").first()
        if not prog2:
            prog2 = models.Program(
                title="Chương Trình Kỹ Năng Lãnh Đạo & Quản Trị Dự Án Hiện Đại",
                slug="chuong-trinh-lanh-dao-quan-tri-2026",
                description="Lộ trình rèn luyện kỹ năng mềm, thuyết trình thuyết phục, giao tiếp tạo ảnh hưởng và quản lý tiến độ dự án chuyên nghiệp.",
                image="/images/7_3fd889db-0fdf-43aa-867f-67d166f045c7.png"
            )
            db.add(prog2)
            db.commit()
            db.refresh(prog2)

        print("Seeding courses...")
        for course_data in COURSES_SEED:
            existing = db.query(models.Course).filter(models.Course.id == course_data["id"]).first()
            p_id = prog1.id if course_data["category_slug"] in ["dao-tao-doanh-nghiep", "dao-tao-co-quan-nha-nuoc", "ky-nang-ai"] else (prog2.id if course_data["category_slug"] in ["dao-tao-ca-nhan", "ky-nang-mem"] else None)
            
            # Default assign sample lecturers based on course category
            lec_ids = "nguyen-vu-huy-hoang,bui-huynh-thuong" if course_data["category_slug"] in ["dao-tao-doanh-nghiep", "dao-tao-co-quan-nha-nuoc"] else "helen-lam-hien,nguyen-vu-huy-hoang"

            if not existing:
                course = models.Course(
                    id=course_data["id"],
                    title=course_data["title"],
                    category_slug=course_data["category_slug"],
                    program_id=p_id,
                    handle=course_data["handle"],
                    price=course_data["price"],
                    original_price=course_data["original_price"],
                    image=course_data["image"],
                    description=course_data["description"],
                    duration=course_data["duration"],
                    level=course_data["level"],
                    lecturer_ids=lec_ids
                )
                db.add(course)
                db.flush() # Get session persistence to relate tags
                
                for tag_name in course_data["tags"]:
                    tag = models.CourseTag(course_id=course.id, tag=tag_name)
                    db.add(tag)
            else:
                existing.title = course_data["title"]
                existing.category_slug = course_data["category_slug"]
                existing.program_id = p_id
                existing.handle = course_data["handle"]
                existing.price = course_data["price"]
                existing.original_price = course_data["original_price"]
                existing.image = course_data["image"]
                existing.description = course_data["description"]
                existing.duration = course_data["duration"]
                existing.level = course_data["level"]
                if not existing.lecturer_ids:
                    existing.lecturer_ids = lec_ids
        db.commit()

        # Seed Bundles
        print("Seeding bundles...")
        all_courses = db.query(models.Course).all()
        
        b1 = db.query(models.Bundle).filter(models.Bundle.handle == "bundle-2026-master").first()
        if not b1:
            b1 = models.Bundle(
                title="Bundle 2026 Master VIP Tất Cả Khóa Học",
                handle="bundle-2026-master",
                description="Sở hữu trọn bộ tất cả các khóa học cao cấp tại ACC Academy với đặc quyền cập nhật kiến thức mới miễn phí trong suốt năm 2026.",
                price=5990000,
                original_price=15900000,
                image="/images/Data_Bootcamp.png",
                courses=all_courses
            )
            db.add(b1)

        b2 = db.query(models.Bundle).filter(models.Bundle.handle == "ai-master-bundle").first()
        ai_courses = db.query(models.Course).filter(models.Course.category_slug == "ky-nang-ai").all()
        if not b2:
            b2 = models.Bundle(
                title="AI & Automation Master Bundle",
                handle="ai-master-bundle",
                description="Trọn bộ các khóa học AI cốt lõi: ChatGPT Work Automation, AI COE, Gen AI Studio và Claude Productivity.",
                price=3990000,
                original_price=9800000,
                image="/images/Square_Cover_b1dc8f1b-edc2-473f-ada7-6756dae8a281.png",
                courses=ai_courses
            )
            db.add(b2)

        b3 = db.query(models.Bundle).filter(models.Bundle.handle == "data-bootcamp-combo").first()
        prof_courses = db.query(models.Course).filter(models.Course.category_slug == "ky-nang-chuyen-mon").all()
        if not b3:
            b3 = models.Bundle(
                title="Data Bootcamp - Combo AI For Decision Making & Data Processing",
                handle="data-bootcamp-combo",
                description="Combo toàn diện xử lý dữ liệu tự động, xây dựng Dashboard Looker Studio và ứng dụng AI ra quyết định kinh doanh.",
                price=4500000,
                original_price=8400000,
                image="/images/Data_Bootcamp.png",
                courses=prof_courses
            )
            db.add(b3)

        b4 = db.query(models.Bundle).filter(models.Bundle.handle == "leadership-master-combo").first()
        soft_courses = db.query(models.Course).filter(models.Course.category_slug == "ky-nang-mem").all()
        if not b4:
            b4 = models.Bundle(
                title="Combo Quản Trị & Lãnh Đạo Chuyên Nghiệp",
                handle="leadership-master-combo",
                description="Lộ trình nâng cao năng lực lãnh đạo, giao tiếp thuyết phục cấp trên và quản trị dự án hiệu quả.",
                price=3200000,
                original_price=6800000,
                image="/images/Leader_Shift.webp",
                courses=soft_courses
            )
            db.add(b4)

        db.commit()

        # Ensure all bundles have corresponding Course entries with category_slug='bundles'
        all_bundles = db.query(models.Bundle).all()
        for idx, b in enumerate(all_bundles, start=1):
            c_entry = db.query(models.Course).filter(
                (models.Course.handle == b.handle) | (models.Course.title == b.title)
            ).first()
            if not c_entry:
                c_entry = models.Course(
                    id=9000000000000 + idx,
                    title=b.title,
                    category_slug="bundles",
                    handle=b.handle,
                    price=b.price,
                    original_price=b.original_price,
                    image=b.image or "/images/Data_Bootcamp.png",
                    tags="[\"Bundle\", \"Combo\"]",
                    description=b.description,
                    duration="Trọn đời",
                    level="Tất cả trình độ"
                )
                db.add(c_entry)
            else:
                c_entry.price = b.price
                c_entry.original_price = b.original_price
                c_entry.category_slug = "bundles"

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
            else:
                existing.title = blog_data["title"]
                existing.handle = blog_data["handle"]
                existing.category = blog_data["category"]
                existing.excerpt = blog_data["excerpt"]
                existing.image = blog_data["image"]
                existing.date = blog_data["date"]
                existing.link = blog_data["link"]
        db.commit()

        # 4. Seed Testimonials
        print("Seeding testimonials...")
        for test_data in TESTIMONIALS_SEED:
            existing = db.query(models.Testimonial).filter(models.Testimonial.name == test_data["name"]).first()
            if not existing:
                testimonial = models.Testimonial(**test_data)
                db.add(testimonial)
            else:
                for k, v in test_data.items():
                    setattr(existing, k, v)
        db.commit()

        # 5. Seed Lecturers
        print("Seeding lecturers...")
        valid_seed_ids = [l["id"] for l in LECTURERS_SEED]
        # Delete extra DB lecturers that are not in the seed array
        db.query(models.Lecturer).filter(~models.Lecturer.id.in_(valid_seed_ids)).delete(synchronize_session=False)
        
        for idx, lec_data in enumerate(LECTURERS_SEED):
            existing = db.query(models.Lecturer).filter(models.Lecturer.id == lec_data["id"]).first()
            if not existing:
                lecturer = models.Lecturer(**lec_data, position=idx + 1)
                db.add(lecturer)
            else:
                for k, v in lec_data.items():
                    setattr(existing, k, v)
        db.commit()

        # 6. Seed Projects
        print("Seeding projects...")
        for proj_data in PROJECTS_SEED:
            existing = db.query(models.Project).filter(models.Project.id == proj_data["id"]).first()
            if not existing:
                project = models.Project(**proj_data)
                db.add(project)
            else:
                for k, v in proj_data.items():
                    setattr(existing, k, v)
        db.commit()


        # 5. Seed Banners
        print("Seeding banners...")
        BANNERS_SEED = [
            {
                "title": "AI Center of Excellence",
                "desktop_image": "/images/CoE-Web.png",
                "mobile_image": "/images/CoE-Mobile.png",
                "link": "/corporate/coe",
                "is_external": False,
                "position": 1,
                "is_active": True
            },
            {
                "title": "ChatGPT Work Automation",
                "desktop_image": "/images/Website_dd1fbf97-8fbe-44ed-bfd9-1eaaa069fdb3.png",
                "mobile_image": "/images/SEB_Mobile.png",
                "link": "/courses/category/ky-nang-ai",
                "is_external": False,
                "position": 2,
                "is_active": True
            },
            {
                "title": "teamlacquan.vn",
                "desktop_image": "/images/website_bbadf8f3-a076-4351-ba9e-f9f077fd6271.webp",
                "mobile_image": "/images/mobile_34381454-0cf6-416c-9487-9a341853b38f.webp",
                "link": "https://teamlacquan.vn/",
                "is_external": True,
                "position": 3,
                "is_active": True
            }
        ]
        for banner_data in BANNERS_SEED:
            existing = db.query(models.Banner).filter(models.Banner.title == banner_data["title"]).first()
            if not existing:
                banner = models.Banner(**banner_data)
                db.add(banner)
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
