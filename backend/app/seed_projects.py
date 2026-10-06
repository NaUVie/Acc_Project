import sys
import os
import json

# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app import models

PROJECTS_SEED = [
    {
        "id": "dao-tao-ai-acb",
        "category": "du-an-doanh-nghiep",
        "category_name": "Dự án Doanh nghiệp",
        "title": "Đào tạo ứng dụng Generative AI cho 150+ nhân sự quản lý Tập đoàn ACB",
        "summary": "Giúp bộ phận nhân sự và kinh doanh ứng dụng ChatGPT & Generative AI nâng cao hiệu suất làm việc, tự động hóa báo cáo và phân tích dữ liệu chuyên sâu.",
        "image": "https://drive.google.com/thumbnail?id=120WyoSixRMCuWCMFeNjFKxsDzt74filf&sz=w800",
        "date": "15/08/2026",
        "client": "Tập đoàn Tài chính ACB",
        "drive_profile": "https://drive.google.com/file/d/1p6MtWI5Xk0E00o9TmDhQJA4dFK1j9m0i/view?usp=drive_link",
        "content": json.dumps([
            {
                "type": "paragraph",
                "text": "Học viện ACC vừa phối hợp cùng Tập đoàn Tài chính ACB triển khai thành công chương trình đào tạo chuyên sâu \"Generative AI trong Quản trị & Vận hành Doanh nghiệp\" dành cho hơn 150 cán bộ quản lý và nhân sự cấp cao."
            },
            {
                "type": "heading",
                "text": "Mục tiêu chương trình"
            },
            {
                "type": "paragraph",
                "text": "Chương trình hướng tới việc chuẩn hóa tư duy ứng dụng công nghệ mới, giúp đội ngũ nhân sự ACB tối ưu hóa quy trình làm việc hàng ngày, giảm thiểu các công tác thủ công lặp lại và nâng cao năng lực phân tích dữ liệu tài chính."
            },
            {
                "type": "bullets",
                "items": [
                    "Ứng dụng ChatGPT & Claude trong soạn thảo văn bản, báo cáo và quy trình nội bộ",
                    "Tự động hóa xử lý và làm sạch dữ liệu khách hàng bằng các công cụ AI hiện đại",
                    "Xây dựng khung bảo mật thông tin và an toàn dữ liệu ngân hàng khi sử dụng AI",
                    "Thực hành 100% trên các bài toán thực tế của từng phòng ban ACB"
                ]
            },
            {
                "type": "heading",
                "text": "Kết quả đạt được"
            },
            {
                "type": "paragraph",
                "text": "Sau 4 tuần học và thực hành, 100% học viên đã hoàn thành sản phẩm thực tế áp dụng trực tiếp vào công việc. Hơn 85% nhân sự báo cáo tiết kiệm được trung bình 6–8 giờ làm việc mỗi tuần."
            }
        ], ensure_ascii=False)
    },
    {
        "id": "khung-nang-luc-so-bosch",
        "category": "du-an-doanh-nghiep",
        "category_name": "Dự án Doanh nghiệp",
        "title": "Xây dựng Khung năng lực số & Đào tạo Tư duy Phản biện Bosch Việt Nam",
        "summary": "Tư vấn xây dựng ma trận năng lực số và huấn luyện kỹ năng giải quyết vấn đề phức tạp (Problem Solving) theo tiêu chuẩn quốc tế cho đội ngũ kỹ sư Bosch.",
        "image": "https://drive.google.com/thumbnail?id=1ZININwRW94lavoqqoJ3eAArE5v6vsyZ5&sz=w800",
        "date": "28/07/2026",
        "client": "Bosch Việt Nam",
        "drive_profile": "",
        "content": json.dumps([
            {
                "type": "paragraph",
                "text": "ACC Academy đã đồng hành cùng Bosch Việt Nam triển khai dự án khảo sát, tư vấn xây dựng ma trận năng lực số và đào tạo phương pháp tư duy 8D cùng kỹ năng giải quyết vấn đề phức tạp cho kỹ sư công nghệ."
            },
            {
                "type": "heading",
                "text": "Nội dung triển khai chính"
            },
            {
                "type": "bullets",
                "items": [
                    "Đánh giá thực trạng ma trận năng lực nhân sự hiện tại",
                    "Tích hợp năng lực ứng dụng AI & công nghệ số vào lộ trình phát triển nghề nghiệp",
                    "Huấn luyện trực tiếp phương pháp phân tích nguyên nhân gốc rễ (Root Cause Analysis)",
                    "Thực hành đóng vai và xử lý các sự cố vận hành kỹ thuật quy mô lớn"
                ]
            }
        ], ensure_ascii=False)
    },
    {
        "id": "du-an-trien-khai-ai-shb",
        "category": "du-an-doanh-nghiep",
        "category_name": "Dự án Doanh nghiệp",
        "title": "Tư vấn & Triển khai Lộ trình AI Leadership & Tự động hóa Vận hành SHB",
        "summary": "Dự án chiến lược tư vấn và huấn luyện trực tiếp cho C-Level và các Giám đốc Khối ngân hàng xây dựng trung tâm năng lực AI (CoE) và văn hóa đổi mới sáng tạo.",
        "image": "https://drive.google.com/thumbnail?id=1CU6Pq9-wx_l2DPlb7uigkGIvCtcl921E&sz=w800",
        "date": "Tháng 09/2026",
        "client": "Ngân hàng SHB",
        "drive_profile": "",
        "content": json.dumps([
            {
                "type": "paragraph",
                "text": "ACC Academy hiện đang trực tiếp đồng hành cùng Ngân hàng SHB trong dự án tư vấn chiến lược \"AI Leadership & Digital Transformation\" nhằm hiện đại hóa mô hình vận hành và nâng cao trải nghiệm khách hàng số."
            },
            {
                "type": "heading",
                "text": "Hạng mục triển khai trọng tâm"
            },
            {
                "type": "bullets",
                "items": [
                    "Huấn luyện tư duy lãnh đạo số (Digital Leadership) cho ban điều hành",
                    "Tư vấn thiết lập Trung tâm Năng lực AI xuất sắc (AI Center of Excellence)",
                    "Tự động hóa các luồng xử lý chứng từ và thẩm định tín dụng bằng Generative AI",
                    "Xây dựng chính sách An toàn dữ liệu và Bảo mật thông tin tài chính"
                ]
            }
        ], ensure_ascii=False)
    },
    {
        "id": "du-an-dao-tao-ca-nhan-ai-mastery",
        "category": "du-an-ca-nhan",
        "category_name": "Dự án Cá nhân",
        "title": "Dự án Huấn luyện 1:1 AI Productivity Mastery cho Lãnh đạo & Chủ Doanh nghiệp",
        "summary": "Chương trình huấn luyện cá nhân hóa 1:1 giúp các nhà quản lý, chủ doanh nghiệp làm chủ hệ sinh thái AI, tự động hóa 80% công việc điều hành cá nhân.",
        "image": "https://drive.google.com/thumbnail?id=1miKA4icyQ_nAgwQe5vQge3bqg2W_f8zg&sz=w800",
        "date": "Tháng 08/2026",
        "client": "Cá nhân & Executive Leaders",
        "drive_profile": "",
        "content": json.dumps([
            {
                "type": "paragraph",
                "text": "Chương trình tư vấn và gia tốc năng lực cá nhân dành riêng cho các C-Level, Founders và Quản lý cấp cao muốn làm chủ trợ lý AI cá nhân."
            },
            {
                "type": "heading",
                "text": "Các mảng nội dung chính"
            },
            {
                "type": "bullets",
                "items": [
                    "Tối ưu hóa trợ lý AI cá nhân xử lý Email, Lịch trình & Báo cáo quản trị",
                    "Xây dựng bộ Prompting cá nhân hóa theo phong cách lãnh đạo riêng",
                    "Huấn luyện phân tích số liệu tài chính & dự báo xu hướng thị trường"
                ]
            }
        ], ensure_ascii=False)
    },
    {
        "id": "du-an-chuyen-doi-so-khoi-nha-nuoc",
        "category": "du-an-nha-nuoc",
        "category_name": "Dự án Nhà nước",
        "title": "Dự án Đào tạo Nâng cao Năng lực Số & An toàn Thông tin cho Khối Cơ quan Nhà nước",
        "summary": "Chương trình tư vấn bồi dưỡng kỹ năng ứng dụng CNTT, AI và An toàn dữ liệu công quyền cho cán bộ, công chức các Sở, Ban, Ngành.",
        "image": "https://drive.google.com/thumbnail?id=1CU6Pq9-wx_l2DPlb7uigkGIvCtcl921E&sz=w800",
        "date": "Tháng 07/2026",
        "client": "Khối Cơ quan - Nhà nước",
        "drive_profile": "",
        "content": json.dumps([
            {
                "type": "paragraph",
                "text": "ACC Academy phối hợp tổ chức khóa bồi dưỡng chuyên sâu về Chuyển đổi số, Kỹ năng Số hành chính và Bảo mật An ninh thông tin cho cán bộ công quyền."
            },
            {
                "type": "heading",
                "text": "Hạng mục triển khai trọng tâm"
            },
            {
                "type": "bullets",
                "items": [
                    "Số hóa quy trình xử lý văn bản và hồ sơ công quyền",
                    "Bồi dưỡng kỹ năng ứng dụng AI trong tổng hợp báo cáo và văn bản hành chính",
                    "Chuẩn hóa kiến thức An toàn an ninh thông tin và bảo vệ dữ liệu công"
                ]
            }
        ], ensure_ascii=False)
    }
]

def seed_projects_only():
    print("Seeding projects table ONLY...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing projects table
        db.query(models.Project).delete()
        db.commit()

        count = 0
        for proj_data in PROJECTS_SEED:
            project = models.Project(**proj_data)
            db.add(project)
            count += 1
        db.commit()
        print(f"Successfully seeded {count} projects into database!")
    except Exception as e:
        db.rollback()
        print("Error seeding projects:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_projects_only()
