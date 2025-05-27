import requests
import argparse
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML

def get_crtsh_common_names(domain):
    """Fetches unique name values from crt.sh for a given domain."""
    url = f"https://crt.sh/json?q={domain}"
    print(f"Fetching certificate data for '{domain}' from {url}...")

    try:
        response = requests.get(url) # Added timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if not data:
            print(f"No certificate data found for '{domain}'.")
            return []

        unique_name_values = set()

        for entry in data:
            nv = entry.get('name_value')
            if nv:
                # Add both the raw name value and a potential wildcard stripped version
                unique_name_values.add(nv)
                if nv.startswith('*.'):
                    unique_name_values.add(nv[2:]) # Add domain without *.

        name_values = sorted(list(unique_name_values))
        return name_values

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from crt.sh: {e}")
        return []
    except ValueError:
        print("Error: Could not decode JSON response from crt.sh. The server might have returned non-JSON data.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during crt.sh fetch: {e}")
        return []

def get_page_title(url):
    """Attempts to visit a URL and extract the page title."""
    try:
        # Try HTTPS first
        full_url = f"https://{url}"
        response = requests.get(full_url, timeout=20, allow_redirects=True) # Added timeout and redirects
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')

        if title_tag:
            return title_tag.string.strip()
        else:
            return None # No title tag found

    except requests.exceptions.RequestException as e:
        # Catch any request-related errors (connection, timeout, HTTP errors, etc.)
        # print(f"Could not visit {url}: {e}") # Optional: uncomment for debugging
        return None
    except Exception as e:
        # Catch any other unexpected errors during parsing
        # print(f"An unexpected error occurred while processing {url}: {e}") # Optional: uncomment for debugging
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch common names from crt.sh and attempt to visit them to get page titles.")
    parser.add_argument("domain", help="The domain to search for on crt.sh (e.g., google.com).", type=str)
    args = parser.parse_args()

    names = get_crtsh_common_names(args.domain)

    if names:
        print(f"\nAttempting to visit found name values for '{args.domain}':")
        visited_count = 0
        for name in names:
            # Avoid trying to visit wildcard domains directly
            if name.startswith('*.'):
                continue

            print(f"  Visiting {name}...", end="")
            title = get_page_title(name) # Pass just the domain name to the function

            if title:
                print(f" Success! Title: '{title}'")
                visited_count += 1
            else:
                print(" Failed or no title found.") # Indicate failure without detailed error

        if visited_count == 0:
             print(f"\nNo reachable common names with titles were found for '{args.domain}'.")
    else:
        print(f"No name values found on crt.sh for '{args.domain}'.")

