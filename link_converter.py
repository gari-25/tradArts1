import os
import re

def convert_all_links(templates_dir="templates", static_dir="static"):
    """
    Finds all HTML files in a directory and converts all internal links
    (HTML pages, CSS, JS, and images) to Flask's url_for() format.

    Args:
        templates_dir (str): The path to the directory containing your HTML files.
        static_dir (str): The path to the directory containing your static assets.
    """
    print(f"Starting to convert links in directory: {templates_dir}")

    if not os.path.exists(templates_dir):
        print(f"Error: The directory '{templates_dir}' was not found.")
        return

    # Regex patterns for different link types
    # Finds links to other .html files
    html_link_regex = re.compile(r'href="([^"]+\.html)"')

    # Finds links to CSS files in the static root
    css_link_regex = re.compile(r'href="([^/]+\.css)"')

    # Finds links to JS files in the static root
    js_link_regex = re.compile(r'src="([^/]+\.js)"')

    # Finds links to images (handles common extensions) in the images subfolder
    img_link_regex = re.compile(r'src="([^"]+\.(?:jpg|jpeg|png|gif|svg|webp))"')

    # Walk through the templates directory
    for root, _, files in os.walk(templates_dir):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                print(f"\nProcessing file: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # --- Convert HTML links ---
                    new_content = content
                    # Use a set to avoid processing the same link multiple times
                    html_links = set(html_link_regex.findall(content))
                    for old_link in html_links:
                        # e.g., "artist-dashboard.html" -> "artist_dashboard"
                        route_name = old_link.replace('-', '_').replace('.html', '')
                        new_link = f'{{{{ url_for(\'{route_name}\') }}}}'
                        new_content = re.sub(
                            re.escape(f'href="{old_link}"'),
                            f'href="{new_link}"',
                            new_content
                        )
                        print(f"  Converted HTML link '{old_link}' to '{new_link}'")

                    # --- Convert CSS links ---
                    temp_content = new_content
                    css_links = set(css_link_regex.findall(temp_content))
                    for old_link in css_links:
                        # e.g., "styles.css" -> url_for('static', filename='styles.css')
                        new_link = f'{{{{ url_for(\'static\', filename=\'{old_link}\') }}}}'
                        new_content = re.sub(
                            re.escape(f'href="{old_link}"'),
                            f'href="{new_link}"',
                            new_content
                        )
                        print(f"  Converted CSS link '{old_link}' to '{new_link}'")

                    # --- Convert JS links ---
                    temp_content = new_content
                    js_links = set(js_link_regex.findall(temp_content))
                    for old_link in js_links:
                        # e.g., "scripts.js" -> url_for('static', filename='scripts.js')
                        new_link = f'{{{{ url_for(\'static\', filename=\'{old_link}\') }}}}'
                        new_content = re.sub(
                            re.escape(f'src="{old_link}"'),
                            f'src="{new_link}"',
                            new_content
                        )
                        print(f"  Converted JS link '{old_link}' to '{new_link}'")

                    # --- Convert Image links ---
                    temp_content = new_content
                    img_links = set(img_link_regex.findall(temp_content))
                    for old_link in img_links:
                        # Assumes images are in 'static/images'
                        new_link = f'{{{{ url_for(\'static\', filename=\'images/{os.path.basename(old_link)}\') }}}}'
                        new_content = re.sub(
                            re.escape(f'src="{old_link}"'),
                            f'src="{new_link}"',
                            new_content
                        )
                        print(f"  Converted Image link '{old_link}' to '{new_link}'")


                    # Write the modified content back to the file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"  Conversion complete for {filename}.")

                except Exception as e:
                    print(f"  Error processing file {filepath}: {e}")

    print("\nAll files processed. Please review the changes and ensure your Flask routes match the converted names.")


if __name__ == '__main__':
    # Make sure to set the correct directories if they are different
    # from the default "templates" and "static"
    convert_all_links(templates_dir="templates", static_dir="static")
