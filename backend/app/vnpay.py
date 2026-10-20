import hmac
import hashlib
import urllib.parse
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

def generate_vnpay_url(
    order_id: int,
    amount: int,
    order_info: str,
    ip_addr: str,
    tmn_code: str,
    hash_secret: str,
    payment_url: str,
    return_url: str,
    bank_code: Optional[str] = None
) -> str:
    """
    Generate VNPay payment URL for sandbox/production.
    VNPay expects amount multiplied by 100.
    """
    tz_vn = timezone(timedelta(hours=7))
    now = datetime.now(tz_vn)
    create_date = now.strftime('%Y%m%d%H%M%S')
    expire_date = (now + timedelta(minutes=15)).strftime('%Y%m%d%H%M%S')

    # Normalize ip_addr (ensure valid IPv4, no IPv6 like ::1)
    client_ip = (ip_addr or '').strip()
    if not client_ip or client_ip in ('::1', 'localhost'):
        client_ip = '127.0.0.1'
    elif ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()

    vnp_params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': tmn_code,
        'vnp_Amount': str(int(amount) * 100),
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': str(order_id),
        'vnp_OrderInfo': order_info,
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': return_url,
        'vnp_IpAddr': client_ip,
        'vnp_CreateDate': create_date,
        'vnp_ExpireDate': expire_date,
    }

    if bank_code:
        vnp_params['vnp_BankCode'] = bank_code

    # Sort parameters by key alphabetically
    sorted_params = sorted(vnp_params.items())
    
    # Build query string
    sign_data = urllib.parse.urlencode(sorted_params)
    
    # Hash with HMAC-SHA512
    h = hmac.new(
        hash_secret.encode('utf-8'),
        sign_data.encode('utf-8'),
        hashlib.sha512
    )
    secure_hash = h.hexdigest()

    return f"{payment_url}?{sign_data}&vnp_SecureHash={secure_hash}"


def verify_vnpay_response(params: Dict[str, Any], hash_secret: str) -> bool:
    """
    Verify the return / IPN payload from VNPay.
    """
    vnp_params = dict(params)
    vnp_secure_hash = vnp_params.pop('vnp_SecureHash', None)
    vnp_params.pop('vnp_SecureHashType', None)

    if not vnp_secure_hash:
        return False

    # Filter out empty keys/values
    clean_params = {k: v for k, v in vnp_params.items() if v is not None and str(v) != ''}
    sorted_params = sorted(clean_params.items())

    # Build query string for hashing
    sign_data = urllib.parse.urlencode(sorted_params)

    h = hmac.new(
        hash_secret.encode('utf-8'),
        sign_data.encode('utf-8'),
        hashlib.sha512
    )
    calculated_hash = h.hexdigest()

    return hmac.compare_digest(calculated_hash.lower(), str(vnp_secure_hash).lower())
