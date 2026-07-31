import { defineStore } from 'pinia';

export const useTestimonialStore = defineStore('testimonials', {
  state: () => ({
    testimonials: [
      {
        id: 1,
        text: "Tôi đã học được rất nhiều, không chỉ về kỹ năng giải quyết vấn đề và ra quyết định, mà còn ở cách tư duy và áp dụng vào công việc thực tế.",
        name: "Công ty TNHH An toàn Công Cộng Đông Nam Á Axon",
        role: "Chủ đề đào tạo: Problem Solving",
        image: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=400&auto=format&fit=crop"
      },
      {
        id: 2,
        text: "Khóa học được chuẩn bị một cách kỹ lưỡng, thể hiện qua các hoạt động tình huống sinh động và lôi cuốn, giúp tôi dễ dàng tiếp cận và ghi nhớ kiến thức.",
        name: "MAYBANK",
        role: "Chủ đề đào tạo: Problem Solving",
        image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=400&auto=format&fit=crop"
      },
      {
        id: 3,
        text: "Khóa học cung cấp phương pháp tiếp cận từng bước để xử lý các tình huống thực tế liên quan đến năng lực văn hóa (CQ), giúp tôi dễ dàng áp dụng vào công việc.",
        name: "Công ty cổ phần VNG",
        role: "Chủ đề đào tạo: Cultural Intelligence",
        image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=400&auto=format&fit=crop"
      }
    ]
  })
});
