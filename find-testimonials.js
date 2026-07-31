const fs = require('fs');
const html = fs.readFileSync('f:\\Project_Ngoai\\ACC\\ThamKhao\\skillbright_all\\index.html', 'utf8');
const lines = html.split('\n');
const keywords = ['học viên', 'doanh nghiệp', 'đối tác', 'đánh giá', 'review', 'testimonial', 'nhận xét', 'chia sẻ'];

lines.forEach((line, index) => {
  const matches = keywords.filter(kw => line.toLowerCase().includes(kw));
  if (matches.length > 0 && line.length < 500) {
    console.log(`Line ${index + 1} [${matches.join(', ')}]: ${line.trim()}`);
  }
});
