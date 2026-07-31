<template>
  <div class="recipes-view container">
    <div class="header-section">
      <div class="badge">FREE RESOURCE</div>
      <h1>Công thức <span class="gradient-text">Viết Prompt</span></h1>
      <p class="subtitle">Thư viện câu lệnh AI (Prompt Recipes) mẫu thực chiến giúp bạn tối ưu hóa công việc hàng ngày ngay lập tức.</p>
    </div>

    <div class="recipes-grid">
      <div class="recipe-card glass-card">
        <h3>📋 Prompt Tóm tắt Tài liệu chuyên sâu</h3>
        <p class="desc">Dùng để tóm tắt các báo cáo tài chính hoặc bài báo nghiên cứu dài thành các luận điểm cốt lõi và hành động cần thiết.</p>
        <div class="prompt-box">
          <code>"Hãy tóm tắt tài liệu sau thành 5 luận điểm cốt lõi dưới dạng bullet points, tập trung vào [mục tiêu chính] và chỉ ra 3 hành động thực thi khả thi nhất..."</code>
        </div>
      </div>

      <div class="recipe-card glass-card">
        <h3>✍️ Prompt Lên ý tưởng nội dung đa kênh</h3>
        <p class="desc">Dùng để phát triển 1 chủ đề cốt lõi thành các bài đăng định dạng khác nhau cho Facebook, TikTok và LinkedIn.</p>
        <div class="prompt-box">
          <code>"Tôi có chủ đề: [nhập chủ đề]. Hãy viết 1 bài đăng LinkedIn định dạng chuyên nghiệp, 1 kịch bản ngắn TikTok 30s và 1 bài đăng Facebook thu hút tương tác..."</code>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.recipes-view {
  padding: 60px 24px;
}

.header-section {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 60px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.badge {
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: var(--primary);
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.header-section h1 {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 800;
}

.subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.recipes-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
}

.recipe-card {
  padding: 40px;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.recipe-card h3 {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
}

.desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.prompt-box {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-color);
  padding: 20px;
  border-radius: var(--radius-md);
  font-family: monospace;
  font-size: 13px;
  color: #38bdf8;
  line-height: 1.5;
  word-break: break-word;
}

@media (max-width: 768px) {
  .recipes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
