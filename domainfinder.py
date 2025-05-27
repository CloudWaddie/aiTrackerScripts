import requests
import argparse

def get_crtsh_common_names(domain):
    url = f"https://crt.sh/json?q={domain}"
    print(f"Fetching certificate data for '{domain}' from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"No certificate data found for '{domain}'.")
            return []

        unique_names = set()
        base_domain = domain.lstrip('*.')

        for entry in data:
            # Check both common_name and name_value fields
            for field in ['common_name', 'name_value']:
                name = entry.get(field)
                if not name:
                    continue
                    
                # Handle cases where name might be a string with multiple names
                for subname in str(name).split('\n'):
                    subname = subname.strip()
                    # Only include if it's a subdomain of our target domain
                    if subname.endswith(base_domain) or f'.{base_domain}' in subname:
                        unique_names.add(subname)


        names = sorted(list(unique_names))
        return names

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except ValueError:
        print("Error: Could not decode JSON response. The server might have returned non-JSON data.")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch common names from crt.sh for one or more domains.")
    parser.add_argument("domains", nargs='+', help="One or more domains to search for (e.g., chatgpt.com example.com)", type=str)
    args = parser.parse_args()

    for domain in args.domains:
        names = get_crtsh_common_names(domain)

        if names:
            print(f"\nCommon Names found for '{domain}':")
            for name in names:
                print(f"- {name}")
        else:
            print(f"\nNo common names found for '{domain}'.")