import smtplib
import logging
import json
import urllib.request
import urllib.error
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
from . import config, models

logger = logging.getLogger(__name__)

def get_vietnam_time(dt=None):
    if dt is None:
        dt = datetime.now(timezone.utc)
    vn_tz = timezone(timedelta(hours=7))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(vn_tz)

def resolve_admin_recipient(db=None):
    """
    Determine the admin email address to receive contact alerts.
    Priority:
    1. config.ADMIN_NOTIFICATION_EMAIL (from .env)
    2. models.ContactSetting.email (from database settings)
    3. First admin in models.User
    """
    if config.ADMIN_NOTIFICATION_EMAIL and config.ADMIN_NOTIFICATION_EMAIL.strip():
        return config.ADMIN_NOTIFICATION_EMAIL.strip()
    
    if db is not None:
        try:
            setting = db.query(models.ContactSetting).first()
            if setting and setting.email and setting.email.strip():
                return setting.email.strip()
            
            admin_user = db.query(models.User).filter(models.User.role == "admin").first()
            if admin_user and admin_user.email and admin_user.email.strip():
                return admin_user.email.strip()
        except Exception as e:
            logger.warning(f"Could not resolve admin email from DB: {e}")
            
    return None

def send_via_resend(subject, html_content, recipient_email):
    """
    Send email via modern Resend REST API (https://resend.com) using standard library urllib.
    Zero external dependencies required.
    """
    api_key = config.RESEND_API_KEY.strip()
    from_email = config.RESEND_FROM_EMAIL.strip() or "ACC Academy <onboarding@resend.dev>"
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "ACC-Academy-Backend/1.0"
    }
    payload = {
        "from": from_email,
        "to": [recipient_email],
        "subject": subject,
        "html": html_content
    }
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as response:
            status_code = response.getcode()
            response_body = response.read().decode("utf-8")
            if 200 <= status_code < 300:
                logger.info(f"[RESEND] Successfully sent contact alert email to {recipient_email}. Resp: {response_body}")
                return True
            else:
                logger.error(f"[RESEND] Failed to send email (Status {status_code}): {response_body}")
                return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        logger.error(f"[RESEND] HTTP error {e.code}: {error_body}")
        return False
    except Exception as e:
        logger.error(f"[RESEND] Network error while calling Resend API: {e}")
        return False

def send_via_smtp(subject, html_content, recipient_email):
    """
    Send email via standard SMTP (Gmail/Custom SMTP)
    """
    smtp_user = config.SMTP_USER.strip() if config.SMTP_USER else ""
    smtp_password = config.SMTP_PASSWORD.strip() if config.SMTP_PASSWORD else ""
    smtp_host = config.SMTP_HOST.strip() if config.SMTP_HOST else "smtp.gmail.com"
    smtp_port = config.SMTP_PORT

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"ACC Academy <{smtp_user}>"
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()
            
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [recipient_email], msg.as_string())
        server.quit()
        logger.info(f"[SMTP] Successfully sent contact alert email to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"[SMTP] Failed to send contact notification email: {e}")
        return False

CATEGORY_TITLE_MAP = {
    "individual": "Đào tạo cho cá nhân",
    "corporate": "Đào tạo cho doanh nghiệp",
    "postgraduate": "Tuyển sinh các chương trình sau đại học",
    "consultation-popup": "Đăng ký tư vấn (Popup Trang Chủ)",
    "course-register": "Đăng ký tư vấn khóa học",
    "forgot_password": "Yêu cầu cấp lại mật khẩu",
    "forgot-password": "Yêu cầu cấp lại mật khẩu",
    "lien-he": "Tư vấn thông tin chung",
}

def send_admin_contact_notification(contact, recipient_email=None):
    """
    Send an email notification to the admin when a new contact inquiry arrives.
    Priority:
    1. Resend API (if RESEND_API_KEY is configured in .env)
    2. SMTP (if SMTP_USER and SMTP_PASSWORD are configured in .env)
    Runs safely inside FastAPI BackgroundTasks.
    """
    has_resend = bool(config.RESEND_API_KEY and config.RESEND_API_KEY.strip())
    has_smtp = bool(config.SMTP_USER and config.SMTP_PASSWORD)

    if not has_resend and not has_smtp:
        logger.info(
            "[EMAIL SERVICE] Neither RESEND_API_KEY nor SMTP credentials configured. "
            "Skipping email alert. Configure RESEND_API_KEY or SMTP_USER in backend/.env to enable."
        )
        return False

    if not recipient_email:
        recipient_email = resolve_admin_recipient()
    if not recipient_email and config.SMTP_USER:
        recipient_email = config.SMTP_USER

    if not recipient_email:
        logger.warning("[EMAIL SERVICE] No recipient email found for admin notification.")
        return False

    full_name = " ".join(filter(None, [contact.first_name, contact.middle_name, contact.last_name])) or "Khách hàng"
    phone = contact.phone or "Chưa cung cấp"
    client_email = contact.email or "Chưa cung cấp"

    raw_course = (contact.course_handle or "").strip()
    course_name = CATEGORY_TITLE_MAP.get(raw_course.lower(), raw_course) if raw_course else "Tư vấn thông tin chung"

    message_content = contact.message or "(Khách hàng không để lại ghi chú thêm)"
    for k, v in CATEGORY_TITLE_MAP.items():
        message_content = message_content.replace(f"Mục dịch vụ: {k}", f"Mục dịch vụ: {v}")
    
    created_vn = get_vietnam_time(contact.created_at).strftime("%H:%M:%S ngày %d/%m/%Y")

    is_password_reset = (
        (contact.course_handle or "").lower() in ("forgot_password", "forgot-password")
        or "[quên mk]" in (contact.first_name or "").lower()
    )

    clean_display_name = full_name.replace("[Quên MK]", "").strip() or "Học viên"

    if is_password_reset:
        subject = f"[ACC Academy] 🔐 Cấp lại mật khẩu: {clean_display_name} ({client_email})"
        header_badge = "HỖ TRỢ TÀI KHOẢN KHẨN"
        header_subtitle = "Hệ thống Thông báo Yêu cầu Cấp lại Mật khẩu"
        alert_intro = f"Xin chào Quản trị viên, vừa có một học viên gửi <strong>yêu cầu cấp lại mật khẩu</strong> cho tài khoản <strong>{client_email}</strong>. Vui lòng kiểm tra thông tin dưới đây để kịp thời hỗ trợ học viên:"
    else:
        subject = f"[ACC Academy] Yêu cầu liên hệ mới: {full_name} - {course_name}"
        header_badge = "YÊU CẦU LIÊN HỆ MỚI"
        header_subtitle = "Hệ thống Thông báo Quản trị Viên"
        alert_intro = "Xin chào Quản trị viên, vừa có một khách hàng gửi biểu mẫu liên hệ/đăng ký tư vấn trên website <strong>ACC Academy</strong>. Dưới đây là thông tin chi tiết:"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
      <meta charset="UTF-8">
      <title>{subject}</title>
      <style>
        body {{
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          background-color: #f1f5f9;
          margin: 0;
          padding: 30px 15px;
          color: #1e293b;
        }}
        .container {{
          max-width: 600px;
          margin: 0 auto;
          background: #ffffff;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          border: 1px solid #e2e8f0;
        }}
        .header {{
          background: linear-gradient(135deg, #022B9F 0%, #0284c7 100%);
          color: #ffffff;
          padding: 28px 24px;
          text-align: center;
        }}
        .header h1 {{
          margin: 0;
          font-size: 22px;
          font-weight: 800;
          letter-spacing: 0.5px;
        }}
        .header p {{
          margin: 6px 0 0;
          font-size: 13px;
          color: #e0f2fe;
          font-weight: 500;
        }}
        .badge {{
          display: inline-block;
          background: #fbbf24;
          color: #0f172a;
          font-size: 11px;
          font-weight: 800;
          padding: 4px 12px;
          border-radius: 12px;
          letter-spacing: 1px;
          text-transform: uppercase;
          margin-bottom: 8px;
        }}
        .content {{
          padding: 28px 24px;
        }}
        .alert-intro {{
          font-size: 15px;
          color: #334155;
          margin-top: 0;
          margin-bottom: 20px;
          line-height: 1.6;
        }}
        .info-table {{
          width: 100%;
          border-collapse: collapse;
          margin-bottom: 24px;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          overflow: hidden;
        }}
        .info-table tr {{
          border-bottom: 1px solid #f1f5f9;
        }}
        .info-table tr:last-child {{
          border-bottom: none;
        }}
        .info-label {{
          width: 35%;
          background: #f8fafc;
          padding: 12px 16px;
          font-size: 13.5px;
          font-weight: 700;
          color: #475569;
          vertical-align: top;
        }}
        .info-value {{
          padding: 12px 16px;
          font-size: 14.5px;
          color: #0f172a;
          font-weight: 500;
        }}
        .info-value a {{
          color: #022B9F;
          text-decoration: none;
          font-weight: 700;
        }}
        .message-box {{
          background: #f8fafc;
          border-left: 4px solid #022B9F;
          padding: 14px 16px;
          border-radius: 4px;
          font-size: 14px;
          line-height: 1.6;
          color: #334155;
          white-space: pre-wrap;
        }}
        .action-buttons {{
          margin-top: 24px;
          padding-top: 20px;
          border-top: 1px solid #e2e8f0;
          text-align: center;
        }}
        .btn {{
          display: inline-block;
          padding: 11px 22px;
          border-radius: 8px;
          text-decoration: none;
          font-size: 13.5px;
          font-weight: 700;
          margin: 4px 6px;
        }}
        .btn-call {{
          background: #022B9F;
          color: #ffffff !important;
        }}
        .btn-email {{
          background: #f1f5f9;
          color: #0f172a !important;
          border: 1px solid #cbd5e1;
        }}
        .footer {{
          background: #f8fafc;
          padding: 18px 24px;
          font-size: 12px;
          color: #64748b;
          text-align: center;
          border-top: 1px solid #e2e8f0;
          line-height: 1.6;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <span class="badge">{header_badge}</span>
          <h1>ACC ACADEMY</h1>
          <p>{header_subtitle}</p>
        </div>
        <div class="content">
          <p class="alert-intro">
            {alert_intro}
          </p>

          <table class="info-table">
            <tr>
              <td class="info-label">Họ và tên</td>
              <td class="info-value" style="font-weight: 700; font-size: 15px; color: #022B9F;">{clean_display_name}</td>
            </tr>
            <tr>
              <td class="info-label">Số điện thoại</td>
              <td class="info-value">
                <a href="tel:{phone}" style="color: #0284c7; font-weight: 700;">{phone}</a>
              </td>
            </tr>
            <tr>
              <td class="info-label">Địa chỉ Email</td>
              <td class="info-value">
                <a href="mailto:{client_email}">{client_email}</a>
              </td>
            </tr>
            <tr>
              <td class="info-label">Khóa học / Chủ đề</td>
              <td class="info-value">
                <span style="display: inline-block; background: #eff6ff; color: #022B9F; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 14px; border: 1px solid #bfdbfe;">{course_name}</span>
              </td>
            </tr>
            <tr>
              <td class="info-label">Thời gian gửi</td>
              <td class="info-value">{created_vn}</td>
            </tr>
            <tr>
              <td class="info-label">Nội dung lời nhắn</td>
              <td class="info-value">
                <div class="message-box">{message_content}</div>
              </td>
            </tr>
          </table>

          <div class="action-buttons">
            <a href="tel:{phone}" class="btn btn-call">📞 Gọi ngay cho khách ({phone})</a>
            <a href="mailto:{client_email}?subject=ACC%20Academy%20-%20H%E1%BB%93i%20%C4%91%C3%A1p%20y%C3%AAu%20c%E1%BA%A7u%20t%C6%B0%20v%E1%BA%A5n" class="btn btn-email">✉️ Phản hồi qua Email</a>
          </div>
        </div>
        <div class="footer">
          Email này được gửi tự động từ hệ thống website ACC Academy.<br />
          Đăng nhập trang quản trị để xem và theo dõi tình trạng xử lý liên hệ.
        </div>
      </div>
    </body>
    </html>
    """

    # 1. Prioritize Resend if configured
    if has_resend:
        return send_via_resend(subject, html_content, recipient_email)
    
    # 2. Fallback to SMTP
    if has_smtp:
        return send_via_smtp(subject, html_content, recipient_email)

    return False
