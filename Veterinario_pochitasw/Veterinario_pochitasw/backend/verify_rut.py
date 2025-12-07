import re

rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
regex = re.compile(rut_pattern)

def check_rut(rut_input):
    print(f"\n--- Testing: '{rut_input}' ---")
    rut_clean = rut_input.replace('.', '').replace('-', '')
    if len(rut_clean) > 1:
        body, dv = rut_clean[:-1], rut_clean[-1].upper()
        try:
            reversed_body = body[::-1]
            dotted = '.'.join(reversed_body[i:i+3] for i in range(0, len(reversed_body), 3))[::-1]
            rut_formatted = f"{dotted}-{dv}"
            print(f"Formatted: '{rut_formatted}'")
            
            if regex.match(rut_formatted):
                print("✅ Valid Regex Match")
            else:
                print("❌ Invalid Regex Match")
        except Exception as e:
            print(f"Format Error: {e}")
    else:
        print("Too short")

# Test cases
check_rut("123456789")
check_rut("12.345.678-9")
check_rut("98765432") # 8 digits (common 10m range)
check_rut("1111111-1") # 7 digits (1 million range)
check_rut("11111k") # Short?
