import sys
import os

# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, SessionLocal, Base
from app import models

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

def seed_testimonials_only():
    print("Seeding testimonials table ONLY...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing testimonials to prevent name collision/overwriting
        db.query(models.Testimonial).delete()
        db.commit()

        count = 0
        for test_data in TESTIMONIALS_SEED:
            testimonial = models.Testimonial(**test_data)
            db.add(testimonial)
            count += 1
        db.commit()
        print(f"Successfully seeded {count} testimonials into database!")
    except Exception as e:
        db.rollback()
        print("Error seeding testimonials:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_testimonials_only()
