import re
import hashlib
from shared.contracts import EvidenceCandidate

def template_fingerprint(text: str) -> str:
    if not text:
        return ""
        
    lines = text.split('\n')
    
    # 1. Heading sequence (lines ending with ":" or starting with "#")
    headings = []
    for line in lines:
        line = line.strip()
        if line.endswith(':') or line.startswith('#'):
            headings.append(line.split(':')[0] if ':' in line else line.split()[0])
            
    # 2. Price-decimal pattern (e.g. $10.00, 0.05 BTC)
    price_pattern = r'(\$|BTC|XMR)?\s*\d+\.\d{2,8}\s*(\$|BTC|XMR)?'
    prices = re.findall(price_pattern, text, re.IGNORECASE)
    has_prices = "Y" if prices else "N"
    
    # 3. Standard fields presence
    std_fields = ["item", "price", "contact", "shipping", "refund"]
    text_lower = text.lower()
    fields_present = [f for f in std_fields if f"{f}:" in text_lower]
    
    # Create fingerprint string
    fp_raw = f"H:{'|'.join(headings)}|P:{has_prices}|F:{'|'.join(fields_present)}"
    
    # Return hash of the structural fingerprint
    return hashlib.sha256(fp_raw.encode('utf-8')).hexdigest()[:16]
