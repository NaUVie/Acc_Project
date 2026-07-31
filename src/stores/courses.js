import { defineStore } from 'pinia';

export const useCourseStore = defineStore('courses', {
  state: () => ({
    courses: [
      // Kỹ năng AI
      {
        id: 10800458137911,
        title: "AI Center of Excellence: Lộ Trình Quản Trị & Vận Hành AI Cho Doanh Nghiệp",
        category: "ky-nang-ai",
        handle: "ai-center-of-excellence",
        price: 3629000,
        originalPrice: 4500000,
        image: "/images/Square-Cover-_1.webp",
        tags: ["Course", "E-learning", "Quản trị AI"],
        description: "Lộ trình toàn diện để tích hợp, quản trị và vận hành các mô hình trí tuệ nhân tạo (AI) hiệu quả trong cơ cấu doanh nghiệp hiện đại.",
        duration: "6 tuần",
        level: "Nâng cao"
      },
      {
        id: 10800448438583,
        title: "ChatGPT Work Automation: 10X Tốc độ hoàn thành công việc với ChatGPT & hệ sinh thái OpenAI",
        category: "ky-nang-ai",
        handle: "chatgpt-work-automation",
        price: 3449000,
        originalPrice: 4200000,
        image: "/images/Square_Cover_b1dc8f1b-edc2-473f-ada7-6756dae8a281.png",
        tags: ["Codex", "E-learning", "Kỹ năng AI", "Trí tuệ nhân tạo (AI)"],
        description: "Làm chủ các prompt chuyên sâu để tự động hóa soạn thảo, phân tích tài liệu và tối ưu hóa hiệu suất làm việc văn phòng với ChatGPT.",
        duration: "5 tuần",
        level: "Cơ bản - Nâng cao"
      },
      {
        id: 10681994740023,
        title: "Gen AI Studio: X5 Số Lượng Hình Ảnh, Video Mà Không Tăng Thêm Chi Phí Và Nguồn Lực",
        category: "ky-nang-ai",
        handle: "gen-ai-studio",
        price: 3249000,
        originalPrice: 3800000,
        image: "/images/Square-Cover_c232d7ad-fa2d-4744-b359-5ee042cd9eda.webp",
        tags: ["AI Creative", "Beginner", "E-learning", "Trí tuệ nhân tạo (AI)"],
        description: "Khai phá sức mạnh của AI trong thiết kế hình ảnh, sản xuất video tự động, giúp tối giản chi phí marketing và tăng năng suất nội dung.",
        duration: "4 tuần",
        level: "Cơ bản"
      },
      {
        id: 10523458044215,
        title: "Claude Productivity: X2 Chất lượng công việc với cộng sự điều hành Claude AI",
        category: "ky-nang-ai",
        handle: "claude-productivity",
        price: 3449000,
        originalPrice: 4000000,
        image: "/images/Claude_Productivity.png",
        tags: ["Course", "Intermediate", "Productivity", "Trí tuệ nhân tạo (AI)"],
        description: "Sử dụng Claude AI như một trợ lý thông minh hỗ trợ xử lý dữ liệu phức tạp, xây dựng nội dung chất lượng cao và quản lý dự án.",
        duration: "4 tuần",
        level: "Trung cấp"
      },
      {
        id: 10454235545911,
        title: "AI Workflows for Business Operations",
        category: "ky-nang-ai",
        handle: "ai-workflow-operations",
        price: 1999000,
        originalPrice: 2500000,
        image: "/images/AIW2_c1252e7c-2e62-4a53-8846-496332c851a1.png",
        tags: ["Advanced", "E-learning", "Trí tuệ nhân tạo (AI)", "Workflow"],
        description: "Thiết kế các quy trình tự động hóa vận hành doanh nghiệp bằng cách kết hợp AI với các hệ thống hiện tại.",
        duration: "5 tuần",
        level: "Nâng cao"
      },
      {
        id: 10382239858999,
        title: "Gemini Productivity: X5 Hiệu suất làm việc với hệ sinh thái Google AI",
        category: "ky-nang-ai",
        handle: "gemini-productivity",
        price: 2699000,
        originalPrice: 3200000,
        image: "/images/Gemini_Productivity.png",
        tags: ["Automation", "Beginner", "E-learning", "Productivity", "Trí tuệ nhân tạo (AI)"],
        description: "Tận dụng tối đa Google Workspace tích hợp Gemini để làm việc nhóm hiệu quả, lập kế hoạch và quản lý email thông minh.",
        duration: "4 tuần",
        level: "Cơ bản"
      },
      {
        id: 10322225529143,
        title: "Khoá học AI Survival Kit - Bộ 6 kỹ năng sống còn thời AI",
        category: "ky-nang-ai",
        handle: "khoa-hoc-ai-survival-kit",
        price: 1599000,
        originalPrice: 2000000,
        image: "/images/AI_Survival_Kit_a9bbf9b4-480d-4467-9571-804887d45212.png",
        tags: ["Beginner", "E-learning", "Trí tuệ nhân tạo (AI)"],
        description: "Trang bị đầy đủ kiến thức và kỹ năng cơ bản nhất để thích ứng và phát triển trong kỷ nguyên trí tuệ nhân tạo bùng nổ.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 10296150753591,
        title: "Khoá học AI Workflow Automation - Tự động hóa quy trình với Zapier, Make AI, N8N",
        category: "ky-nang-ai",
        handle: "ai-workflow-automation",
        price: 1799000,
        originalPrice: 2200000,
        image: "/images/AI_Workflow_Automation_8decdc78-096c-4924-9bf9-128ca34359a4.png",
        tags: ["E-learning", "Intermediate", "Trí tuệ nhân tạo (AI)", "Workflow Automation"],
        description: "Kết nối các ứng dụng và xây dựng luồng công việc tự động hóa hoàn toàn không cần code thông qua Zapier và Make.",
        duration: "5 tuần",
        level: "Trung cấp"
      },
      {
        id: 10202599489847,
        title: "Khóa học Data Processing - X5 Hiệu suất xử lý dữ liệu với AI",
        category: "ky-nang-ai",
        handle: "data-processing",
        price: 950000,
        originalPrice: 1500000,
        image: "/images/Data_Processing.png",
        tags: ["Beginner", "Data", "E-learning", "Trí tuệ nhân tạo (AI)"],
        description: "Học cách thu thập, làm sạch và phân tích dữ liệu lớn nhanh chóng bằng các công cụ hỗ trợ AI.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 10202576421175,
        title: "Khóa học AI Content Mastery - Tạo nội dung có cảm xúc, đúng giọng điệu thương hiệu với AI",
        category: "ky-nang-ai",
        handle: "ai-content-mastery",
        price: 899000,
        originalPrice: 1200000,
        image: "/images/AI_Content_Mastery.png",
        tags: ["Beginner", "Content", "E-learning", "Trí tuệ nhân tạo (AI)"],
        description: "Phương pháp xây dựng bài viết sáng tạo, cá nhân hóa nội dung thương hiệu đầy cảm xúc kết hợp sức mạnh AI.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 10061680935223,
        title: "Khóa học AI for Decision Making - Phân tích Dữ Liệu Và Ra Quyết Định Chiến Lược Với AI",
        category: "ky-nang-ai",
        handle: "khoa-hoc-ai-for-decision-making",
        price: 2999000,
        originalPrice: 3800000,
        image: "/images/AID_AI_for_Decision_Making_SQR.png",
        tags: ["Data", "E-learning", "Intermediate", "Trí tuệ nhân tạo (AI)"],
        description: "Phân tích xu hướng thị trường, dự báo kinh doanh và đưa ra quyết định sáng suốt bằng các công cụ phân tích AI.",
        duration: "5 tuần",
        level: "Trung cấp"
      },
      {
        id: 10060640813367,
        title: "GenAI for Office: Tự động hóa Google Sheets, Slide, Lịch trình và Botchat",
        category: "ky-nang-ai",
        handle: "genai-for-office-product",
        price: 799000,
        originalPrice: 1100000,
        image: "/images/GenAI_for_Office.png",
        tags: ["Course", "Thinkific", "Trí tuệ nhân tạo (AI)"],
        description: "Tăng tốc công việc văn phòng thông qua tự động hóa bảng biểu Sheets, tạo slides tự động và thiết kế botchat hỗ trợ.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 9796370956599,
        title: "Khóa học AI Productivity: X10 Hiệu Suất Công Việc Với AI",
        category: "ky-nang-ai",
        handle: "khoa-hoc-ai-productivity",
        price: 1699000,
        originalPrice: 2200000,
        image: "/images/AIP_AIProductivity_SQR.png",
        tags: ["Beginner", "E-learning", "Trí tuệ nhân tạo (AI)"],
        description: "Phương pháp tư duy và bộ công cụ giúp tối ưu hóa thời gian, tăng tốc độ thực thi dự án cá nhân vượt trội.",
        duration: "4 tuần",
        level: "Cơ bản"
      },

      // Kỹ năng mềm
      {
        id: 8250507854135,
        title: "Khóa học Thuyết Trình Thuyết Phục Chuyên Nghiệp",
        category: "ky-nang-mem",
        handle: "khoa-hoc-ky-nang-thuyet-trinh-thuyet-phuc",
        price: 3990000,
        originalPrice: 4800000,
        image: "/images/7_3fd889db-0fdf-43aa-867f-67d166f045c7.png",
        tags: ["Giao tiếp", "Quản lý - Lãnh đạo", "Thuyết trình"],
        description: "Làm chủ giọng nói, ngôn ngữ cơ thể và cấu trúc slide logic để cuốn hút và thuyết phục mọi đối tượng khán giả.",
        duration: "6 tuần",
        level: "Cơ bản - Nâng cao"
      },
      {
        id: 8027323826487,
        title: "Giao Tiếp Khéo Léo – Chinh Phục Cấp Trên, Dẫn Dắt Cấp Dưới",
        category: "ky-nang-mem",
        handle: "khoa-hoc-giao-tiep-tao-anh-huong",
        price: 3990000,
        originalPrice: 4500000,
        image: "/images/6_76841af7-348d-4ff0-960c-2bc1b568e791.png",
        tags: ["Giao tiếp", "Quản lý - Lãnh đạo"],
        description: "Nghệ thuật giao tiếp ứng xử thông minh nơi công sở, giúp xây dựng lòng tin với sếp và tạo động lực cho nhân viên.",
        duration: "5 tuần",
        level: "Cơ bản - Nâng cao"
      },
      {
        id: 8152702583095,
        title: "Lập Kế Hoạch Quản Lý Dự Án – Nghệ Thuật Quản Trị Chuyên Nghiệp",
        category: "ky-nang-mem",
        handle: "khoa-hoc-lap-ke-hoach-quan-ly-chuyen-nghiep",
        price: 4990000,
        originalPrice: 5800000,
        image: "/images/5_6aae1a70-ead0-4301-96ae-b697f7767949.png",
        tags: ["Quản lý", "Quản lý - Lãnh đạo", "Dự án"],
        description: "Phương pháp lập tiến độ, quản trị rủi ro và điều phối tài nguyên dự án một cách khoa học, đúng tiến độ.",
        duration: "6 tuần",
        level: "Trung cấp"
      },
      {
        id: 8027317797175,
        title: "Lãnh Đạo Thông Minh – Bí Quyết Giao Việc & Quản Lý Hiệu Quả",
        category: "ky-nang-mem",
        handle: "khoa-hoc-quan-ly-thoi-gian-va-trao-quyen",
        price: 4990000,
        originalPrice: 6000000,
        image: "/images/1.png",
        tags: ["Lãnh đạo", "Quản lý - Lãnh đạo", "Quản lý thời gian"],
        description: "Kỹ thuật giao việc đúng người đúng việc, giám sát hiệu quả và tối ưu hóa thời gian làm việc của nhà quản lý.",
        duration: "6 tuần",
        level: "Trung cấp - Nâng cao"
      },
      {
        id: 8315656077623,
        title: "Lãnh Đạo Chuyên Nghiệp – Tuyệt chiêu dẫn dắt đội nhóm vững mạnh",
        category: "ky-nang-mem",
        handle: "khoa-hoc-ky-nang-quan-ly-doi-nhom",
        price: 4990000,
        originalPrice: 5800000,
        image: "/images/2.png",
        tags: ["Lãnh đạo", "Quản lý - Lãnh đạo", "Đội nhóm"],
        description: "Bí quyết giải quyết mâu thuẫn, xây dựng văn hóa đội nhóm gắn kết và thúc đẩy từng thành viên vượt chỉ tiêu.",
        duration: "6 tuần",
        level: "Trung cấp - Nâng cao"
      },
      {
        id: 8250507690295,
        title: "Nghệ thuật đàm phán - Chiến Lược Win-Win Trong Kinh Doanh",
        category: "ky-nang-mem",
        handle: "khoa-hoc-ky-nang-dam-phan-thuong-luong",
        price: 3990000,
        originalPrice: 4800000,
        image: "/images/4.png",
        tags: ["Giao tiếp", "Quản lý - Lãnh đạo", "Đàm phán"],
        description: "Chuẩn bị kịch bản thương lượng, nắm bắt tâm lý đối tác và áp dụng các chiến thuật đàm phán để đạt thỏa thuận tối ưu.",
        duration: "5 tuần",
        level: "Trung cấp"
      },
      {
        id: 8002542272823,
        title: "Business Networking – Mở rộng mối quan hệ trong kinh doanh",
        category: "ky-nang-mem",
        handle: "tron-bo-khoa-hoc-business-networking-mo-rong-moi-quan-he-hieu-qua",
        price: 1997000,
        originalPrice: 2500000,
        image: "/images/3.png",
        tags: ["Giao tiếp", "Mở rộng quan hệ", "Networking"],
        description: "Phương pháp tạo ấn tượng ban đầu, duy trì và phát triển mạng lưới đối tác kinh doanh chất lượng, bền vững.",
        duration: "4 tuần",
        level: "Cơ bản"
      },
      {
        id: 10376877605175,
        title: "Khoá học Winning Your Interview - Chiến thắng buổi phỏng vấn",
        category: "ky-nang-mem",
        handle: "winning-your-interview",
        price: 499000,
        originalPrice: 800000,
        image: "/images/Wining_your_interview_e55db67d-30a0-410b-957f-894d6609fb47.png",
        tags: ["Course", "Soft Skills", "Phỏng vấn"],
        description: "Chuẩn bị tâm lý, trả lời các câu hỏi tình huống hóc búa và thương lượng mức lương mong muốn đầy thuyết phục.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 10376877670711,
        title: "Khoá học Winning Your CV - Trở thành ứng viên ưu tiên từ vòng CV",
        category: "ky-nang-mem",
        handle: "winning-your-cv",
        price: 499000,
        originalPrice: 700000,
        image: "/images/Wining_your_CV_def5dc91-fd52-42b3-87dd-1cfb78de8f08.png",
        tags: ["Course", "Thinkific", "CV"],
        description: "Thiết kế CV chuẩn ATS chuyên nghiệp, làm nổi bật thế mạnh bản thân để thu hút nhà tuyển dụng ngay từ cái nhìn đầu tiên.",
        duration: "3 tuần",
        level: "Cơ bản"
      },

      // Kỹ năng chuyên môn
      {
        id: 10249474572599,
        title: "Looker Studio for Everyone (Google data studio) - 1 Click Tự Động Hoá Báo Cáo",
        category: "ky-nang-chuyen-mon",
        handle: "looker-studio-for-everyone",
        price: 1799000,
        originalPrice: 2400000,
        image: "/images/LS_Looker_Studio_for_Everyone_SQR.png",
        tags: ["Data Visualization", "E-learning", "Intermediate", "Dashboard"],
        description: "Học cách kết nối các nguồn dữ liệu khác nhau và tự động hóa toàn bộ hệ thống báo cáo trực quan trong 1 click.",
        duration: "4 tuần",
        level: "Trung cấp"
      },
      {
        id: 10376862499127,
        title: "Khoá học Excel AI - Làm chủ kỹ năng Excel với AI",
        category: "ky-nang-chuyen-mon",
        handle: "excel-ai",
        price: 569000,
        originalPrice: 900000,
        image: "/images/Excell_skill_e9651cdc-6ff9-48ed-9e96-d4e0b6419a41.png",
        tags: ["Course", "Thinkific", "Excel AI"],
        description: "Kết hợp sức mạnh AI vào Excel giúp viết hàm nhanh chóng, xử lý dữ liệu tự động và lập báo cáo thần tốc.",
        duration: "3 tuần",
        level: "Cơ bản"
      },
      {
        id: 10250137960759,
        title: "Looker Studio Template - Mẫu báo cáo dựng sẵn cho bộ phận Kinh doanh và Tài Chính",
        category: "ky-nang-chuyen-mon",
        handle: "mau-bao-cao-looker-studio",
        price: 739000,
        originalPrice: 1200000,
        image: "/images/Data_template_1_56b2cbbf-7e34-47eb-9fe4-8a065d0ee06b.png",
        tags: ["Course", "Thinkific", "Templates"],
        description: "Bộ Dashboard thiết kế sẵn chuyên nghiệp, kết nối ngay lập tức để trực quan hóa hiệu quả kinh doanh và dòng tiền.",
        duration: "Mẫu dựng sẵn",
        level: "Mọi cấp độ"
      },
      {
        id: 10250143760695,
        title: "Looker Studio Template - Mẫu báo cáo dựng sẵn cho C-level, Marketing và Nhân sự",
        category: "ky-nang-chuyen-mon",
        handle: "looker-studio-template",
        price: 800000,
        originalPrice: 1300000,
        image: "/images/Data_template_2_2661e75d-ca99-4eb0-8564-66ff893b7d6c.png",
        tags: ["Course", "Thinkific", "Templates"],
        description: "Giải pháp báo cáo tối ưu cho lãnh đạo quản lý, đo lường chính xác các KPI Marketing và nhân sự nhanh chóng.",
        duration: "Mẫu dựng sẵn",
        level: "Mọi cấp độ"
      },

      // Bundles / Combos
      {
        id: 10205877633335,
        title: "Data Bootcamp - Combo 2 khoá học AI For Decision Making và Data Processing",
        category: "bundles",
        handle: "data-bootcamp",
        price: 3659000,
        originalPrice: 4500000,
        image: "/images/Data_Bootcamp.png",
        tags: ["Beginner", "Combo", "Data", "AI", "Video on-demand"],
        description: "Combo hoàn hảo giúp bạn nâng tầm tư duy số, tự động hóa xử lý dữ liệu và đưa ra quyết định dựa trên số liệu thực tế.",
        duration: "8 tuần",
        level: "Cơ bản - Trung cấp"
      },
      {
        id: 10101184725303,
        title: "Combo khóa học: AI Productivity, AI for Decision Making và Data Processing",
        category: "bundles",
        handle: "khoa-hoc-ai-boost-camp",
        price: 5080000,
        originalPrice: 6500000,
        image: "/images/AI_Bootcamp.png",
        tags: ["Beginner", "Combo", "Data", "Productivity", "AI"],
        description: "Chương trình huấn luyện toàn diện đưa hiệu suất làm việc văn phòng và khả năng phân tích dữ liệu của bạn lên gấp 10 lần.",
        duration: "10 tuần",
        level: "Cơ bản - Trung cấp"
      },
      {
        id: 10339275899191,
        title: "Bộ 3 khóa học AI Intelligence Workflow",
        category: "bundles",
        handle: "ai-intelligent-workflow",
        price: 3895000,
        originalPrice: 5000000,
        image: "/images/AI_Interlligence_Workflow.png",
        tags: ["E-learning", "Intermediate", "Combo", "Workflow Automation"],
        description: "Thiết lập hệ thống làm việc thông minh tự động hóa kết hợp ChatGPT, Make và Claude cho doanh nghiệp của bạn.",
        duration: "8 tuần",
        level: "Trung cấp"
      },
      {
        id: 10339278717239,
        title: "Bộ khóa học DataFlow Automation",
        category: "bundles",
        handle: "dataflow-automation",
        price: 2280000,
        originalPrice: 3000000,
        image: "/images/DataFlow_Automation.png",
        tags: ["Automation", "Beginner", "Bundle", "Data AI"],
        description: "Tự động hóa luồng dữ liệu của bộ phận kinh doanh, tài chính tự động đồng bộ hóa lên dashboards thời gian thực.",
        duration: "6 tuần",
        level: "Cơ bản - Trung cấp"
      },
      {
        id: 10339217211703,
        title: "AI ALL IN ONE - Bộ 6 khóa học AI",
        category: "bundles",
        handle: "ai-all-in-one",
        price: 8069000,
        originalPrice: 10500000,
        image: "/images/AI_All_In_One.png",
        tags: ["Advanced", "Combo", "Content", "Data", "Productivity", "Workflow"],
        description: "Học viện AI thu nhỏ toàn diện nhất, đồng hành giúp bạn làm chủ mọi công cụ GenAI tiên tiến nhất hiện nay.",
        duration: "12 tuần",
        level: "Mọi cấp độ"
      }
    ],
    blogPosts: [
      {
        id: 101,
        title: "1 Giờ Tạo TVC Với AI! (Không Cần Máy Quay, Studio, Ekip)",
        handle: "1-gio-tao-tvc-voi-ai",
        category: "AI Automation",
        excerpt: "Trong bài viết này, Linh sẽ chia sẻ với các bạn cách tạo TVC chuyên nghiệp với AI mà ai...",
        image: "/images/LBVA-Thumbnail_5_d0857985-e0a2-437b-b9f1-a37aafcfea88.png",
        date: "Jul 15, 2026",
        link: "#/blog/1-gio-tao-tvc-voi-ai"
      },
      {
        id: 102,
        title: "Khi AI Copilot Trở Thành Trợ Lý Chiến Lược Tại Amway",
        handle: "khi-ai-copilot-tro-thanh-tro-ly-chien-luoc",
        category: "Lãnh đạo & Quản lý",
        excerpt: "Nhằm hiện thực hóa chiến lược này, ACC Academy đã vinh dự đồng hành cùng đội ngũ nhân sự Amway...",
        image: "/images/Blog_Thumbnail_12_39a02613-d986-43b8-8462-bdb4046a2153.png",
        date: "Jul 14, 2026",
        link: "#/blog/khi-ai-copilot-tro-thanh-tro-ly-chien-luoc"
      },
      {
        id: 103,
        title: "Kimi K2.6: AI Giúp Bạn Làm Web, Slide Và AI Skills",
        handle: "kimi-ai",
        category: "Công cụ AI",
        excerpt: "Khi nhắc đến AI, thì ai cũng biết ChatGPT, Gemini, Claude hay Deep Seek. Nhưng bạn đã biết đến Kimi...",
        image: "/images/AI_Tut_Thumbnail_72f219cc-a95d-41ae-a7b5-8f1699cdde97.png",
        date: "Jul 10, 2026",
        link: "#/blog/kimi-ai"
      },
      {
        id: 104,
        title: "Tư Duy Giải Quyết Vấn Đề: Từ Phản Ứng Thụ Động Đến Năng Lực Điều Hướng Chiến Lược",
        handle: "tu-duy-giai-quyet-van-de",
        category: "Lãnh đạo & Quản lý",
        excerpt: "Trong môi trường công nghệ thay đổi rất nhanh, nhiều vấn đề trong tổ chức không chỉ đến từ lỗi...",
        image: "/images/Blog_Thumbnail_11_ba37dd28-a3e3-4cf2-8284-6cef487efd14.png",
        date: "Jul 9, 2026",
        link: "#/blog/tu-duy-giai-quyet-van-de"
      },
      {
        id: 1,
        title: "Kimi K3 Là Gì? Có Nên Dùng Thay Claude Hay GPT Không?",
        handle: "kimi-k3",
        category: "Công cụ AI",
        excerpt: "Ngày 16/07/2026, Moonshot AI ra mắt Kimi K3, mô hình mã nguồn mở có tổng cộng 2,8 nghìn tỷ tham số, trở thành mô hình mở lớn nhất từng được công bố tính đến thời điểm này. Điểm đáng chú ý không nằm...",
        image: "/images/Blog_Thumbnail_60771c24-064c-424b-8b24-ac3f0f427f6c.png",
        date: "Jul 27, 2026",
        link: "#/blog/kimi-k3"
      },
      {
        id: 2,
        title: "Google Ra Mắt Gemini 3.6 Flash, 3.5 Flash-Lite Và 3.5 Flash Cyber",
        handle: "gemini-new",
        category: "Công cụ AI",
        excerpt: "Bài viết sẽ phân tích đặc điểm chính của từng mô hình trong hệ sinh thái Gemini mới của Google. Trong đó, Gemini 3.6 Flash tập trung vào các tác vụ phức tạp; Gemini 3.5 Flash-Lite ưu tiên tốc độ, c...",
        image: "/images/Blog_Thumbnail_6_069e6121-2d59-4def-b68d-e4f375ebb10b.png",
        date: "Jul 24, 2026",
        link: "#/blog/gemini-new"
      },
      {
        id: 3,
        title: "X10 Sức Mạnh ChatGPT Work Với Plugins (+ Quy Trình Áp Dụng Thực Tế)",
        handle: "chatgpt-plugins",
        category: "Làm việc hiệu suất",
        excerpt: "Trong vòng chưa đầy 30 phút, Linh đã có thể làm xong 3 nhiệm vụ là: tạo một dashboard phân tích dữ liệu hoàn chỉnh, thiết kế bộ hình ảnh quảng cáo cho sản phẩm và tổng hợp tất cả những thông tin ng...",
        image: "/images/LBVA-Thumbnail_1_fc98e21c-8306-4a49-a425-0de79240752d.png",
        date: "Jul 23, 2026",
        link: "#/blog/chatgpt-plugins"
      },
      {
        id: 4,
        title: "Tăng Tốc Tạo Video: Tự Động Hóa Kịch Bản, Nhân Vật & Bối Cảnh Với Storyboard Studio",
        handle: "storyboard-studio",
        category: "AI Automation",
        excerpt: "Bạn nào muốn tạo phim hoạt hình, phim ngắn, hoặc video quảng cáo bằng AI thì phải xem bài viết này nha! Trong các bài viết trước của chị Linh, nhiều bạn nói rằng một trong những việc khó nhất khi t...",
        image: "/images/AI_Tut_Thumbnail_6_f5d6ed9e-10f2-460f-85e5-81d8dbd00cc0.png",
        date: "Jul 21, 2026",
        link: "#/blog/storyboard-studio"
      },
      {
        id: 5,
        title: "Tự Động Hoá 99% Quy Trình Đăng Nội Dung Với Codex (+ Hướng Dẫn Từng Bước)",
        handle: "auto-post-codex",
        category: "Công cụ AI",
        excerpt: "Linh sẽ nói với bạn 1 bí mật: VIDEO NÀY ĐƯỢC ĐĂNG BỞI Codex AI. Toàn bộ những công việc: tải file video lên, điền tiêu đề, dán mô tả, chèn hình thumbnail, thêm từ khoá, lên lịch video… ĐỀU...",
        image: "/images/LBVA-Thumbnail_3_a9f84a7a-3f8a-49cd-b3d0-3f91c32b5aa4.png",
        date: "Jul 16, 2026",
        link: "#/blog/auto-post-codex"
      },
      {
        id: 6,
        title: "OpenAI Cập Nhật ChatGPT Work! (+3 Ứng Dụng Thực Tế)",
        handle: "chatgpt-work-update",
        category: "Công cụ AI",
        excerpt: "OpenAI chính thức tung ra một bản cập nhật cực kỳ \"khủng\" mang tên ChatGPT Work đi kèm dòng mô hình GPT-5.6 gồm bộ ba: Sol, Terra, và Luna. Cập nhật này giúp ChatGPT không còn là một chatbot trò ch...",
        image: "/images/AI_Tut_Thumbnail_5_91eb932e-d5bd-4a6b-ba9c-09503259e702.png",
        date: "Jul 14, 2026",
        link: "#/blog/chatgpt-work-update"
      },
      {
        id: 7,
        title: "“AI Có Thể Làm Gì?”: Cái Bẫy Khiến Doanh Nghiệp Lãng Phí Nguồn Lực AI (+ Mô Hình Đánh Giá)",
        handle: "ai-trap-businesses",
        category: "Lãnh đạo & Quản lý",
        excerpt: "Bạn có để ý một điều là: hầu hết các buổi họp về AI trong công ty thường bắt đầu bằng câu hỏi \"AI có thể làm gì cho chúng ta?\" Nghe rất hợp lý và rất chiến lược, đúng không? Nhưng thực tế, đây là...",
        image: "/images/LBVA-Thumbnail_7_a8013c81-73fd-40da-acf4-09c4c7b9b02e.png",
        date: "Jul 9, 2026",
        link: "#/blog/ai-trap-businesses"
      },
      {
        id: 8,
        title: "Codex Là Gì? Khác Gì ChatGPT?",
        handle: "codex-vs-chatgpt",
        category: "Công cụ AI",
        excerpt: "Rất nhiều người nghĩ Codex chỉ dành cho dân lập trình, nhưng thực ra đây là một ứng dụng AI chạy ngay trên máy tính (desktop app), giúp bạn làm việc trực tiếp với dữ liệu và tài liệu thật của mình,...",
        image: "/images/Blog_Thumbnail_3df6ed8a-d2dd-4c4a-a09d-f6c76db93398.png",
        date: "Jul 9, 2026",
        link: "#/blog/codex-vs-chatgpt"
      },
      {
        id: 9,
        title: "Bạn Chưa Khai Thác Hết Tính Năng Project Của Codex!",
        handle: "codex-project-tips",
        category: "Công cụ AI",
        excerpt: "Bạn đang bỏ qua 1 trong những tính năng mạnh nhất của Codex mà không hề biết! Nhiều bạn mở Codex lên chỉ để hỏi một câu, chờ trả lời, copy kết quả ra ngoài rồi đóng lại. Nhưng ngay cạnh bạn có một ...",
        image: "/images/AI_Tut_Thumbnail_1_722d7246-b041-46bc-8a74-46162a214b51.png",
        date: "Jul 7, 2026",
        link: "#/blog/codex-project-tips"
      },
      {
        id: 10,
        title: "Tạo Video Short Dạng Dọc Trên NotebookLM Với 1 Click",
        handle: "notebooklm-shorts",
        category: "Công cụ AI",
        excerpt: "Công cụ hỗ trợ nghiên cứu rất nổi tiếng của Google là Notebook LM vừa chính thức tung ra tính năng Short Video Overviews, tức là tổng quan bằng video ngắn, cho tất cả tài khoản, kể cả bản miễn phí....",
        image: "/images/AI_Tut_Thumbnail_1_c4b07290-739c-46ab-98c6-7c1e220380d6.png",
        date: "Jul 3, 2026",
        link: "#/blog/notebooklm-shorts"
      }
    ]
  }),
  getters: {
    getCoursesByCategory: (state) => (category) => {
      return state.courses.filter(course => course.category === category);
    },
    getCourseByHandle: (state) => (handle) => {
      return state.courses.find(course => course.handle === handle);
    },
    getBlogPosts: (state) => {
      return state.blogPosts;
    }
  }
});
