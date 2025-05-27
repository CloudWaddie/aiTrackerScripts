import requests
from bs4 import BeautifulSoup
import re

def extract_js_strings():
    # Make the request to get the JavaScript file
    url = "https://www.gstatic.com/_/mss/boq-bard-web/_/js/k=boq-bard-web.BardChatUi.en_US.llcRij4DRZs.es5.O/ck=boq-bard-web.BardChatUi.-NhL9YjEaDQ.L.B1.O/am=zyBI5xH_3Xvv3__vOa8B0AAADA/d=1/exm=_b/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=AL3bBk1oq5wJBsP9AxIvk-3gXk0agwCdDw/ee=DGWCxb:CgYiQ;Pjplud:PoEs9b;QGR0gd:Mlhmy;ScI3Yc:e7Hzgb;Uvc8o:VDovNc;YIZmRd:A1yn5d;cEt90b:ws9Tlc;dowIGb:ebZ3mb;lOO0Vd:OTA3Ae;qafBPd:ovKuLd/m=LQaXg"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # The content is JavaScript, so we'll use BeautifulSoup to parse it as HTML
        # even though it's JS, to handle any HTML entities if present
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Since it's a JS file, we'll work with the text content directly
        js_content = str(soup)
        
        # Check for FAST_TRACK_NOTICE
        if "FAST_TRACK_NOTICE" in js_content:
            print("✓ FAST_TRACK_NOTICE found in the content")
        else:
            print("✗ FAST_TRACK_NOTICE not found in the content")
            
        # Extract case statements using regex (still needed for this specific pattern)
        case_pattern = re.compile(r'case\s+"([^"]+)"\s*:\s*return\s*"([^"]+)";')
        matches = case_pattern.findall(js_content)
        
        if matches:
            print("\nFound case statements:")
            for key, value in matches:
                print(f"Key: {key} => Value: {value}")
        else:
            print("No matching case statements found.")
            
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    extract_js_strings()