import requests
import argparse
import json
import csv
import xlsxwriter
import os

# Banner
BANNER = """
----------------------------------------------------------------------------
             Clickjacking Vulnerability Checker & PoC Generator

 Description: This tool checks for X-Frame-Options and Content-Security-Policy 
              headers to identify Clickjacking vulnerabilities.

 Author: Afif Hidayatullah
 Organization: ITSEC Asia
----------------------------------------------------------------------------
"""

# Function to check headers for vulnerabilities
def check_headers(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        x_frame_options = headers.get('X-Frame-Options', 'Not Set')
        content_security_policy = headers.get('Content-Security-Policy', 'Not Set')
        
        is_vulnerable = x_frame_options == 'Not Set' and content_security_policy == 'Not Set'

        return {
            "url": url,
            "x_frame_options": x_frame_options,
            "content_security_policy": content_security_policy,
            "vulnerable": is_vulnerable
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

# Generate PoC HTML for Clickjacking
def generate_poc(url, output_dir="poc.html"):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clickjacking PoC</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                display: inline-block;
                width: 800px;
                height: 600px;
                overflow: hidden;
                border: 2px solid #333;
                border-radius: 8px;
                background-color: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }}
            iframe {{
                width: 100%;
                height: 100%;
                border: none;
            }}
        </style>
    </head>
    <body>
        <h1>Clickjacking Proof of Concept</h1>
        <p>The content of the target URL is displayed below:</p>
        <div class="container">
            <iframe src="{url}"></iframe>
        </div>
    </body>
    </html>
    """
    with open(output_dir, "w") as file:
        file.write(html_content)
    print(f"[INFO] PoC HTML saved to {output_dir}")

# Export results to various formats
def export_results(results, output_file, format):
    if format == "json":
        with open(output_file, "w") as file:
            json.dump(results, file, indent=4)
    elif format == "csv":
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    elif format == "txt":
        with open(output_file, "w") as file:
            for result in results:
                file.write(json.dumps(result) + "\n")
    elif format == "xlsx":
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet()
        headers = results[0].keys()
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        for row, result in enumerate(results, start=1):
            for col, key in enumerate(result):
                worksheet.write(row, col, str(result[key]))
        workbook.close()
    print(f"[INFO] Results exported to {output_file}")

# Main function
def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Clickjacking Vulnerability Checker & PoC Generator")
    parser.add_argument("--url", help="Single URL to check", type=str)
    parser.add_argument("--bulk", help="File containing multiple URLs", type=str)
    parser.add_argument("--poc", help="Generate PoC for a specific URL", type=str)
    parser.add_argument("--output", help="Output file name", type=str)
    parser.add_argument("--format", help="Output format (json, csv, txt, xlsx)", type=str, default="json")
    args = parser.parse_args()

    results = []

    # Check a single URL
    if args.url:
        print(f"[INFO] Checking {args.url}")
        result = check_headers(args.url)
        results.append(result)

    # Bulk check URLs
    if args.bulk:
        if not os.path.exists(args.bulk):
            print(f"[ERROR] File not found: {args.bulk}")
            return
        with open(args.bulk, "r") as file:
            urls = file.read().splitlines()
        for url in urls:
            print(f"[INFO] Checking {url}")
            result = check_headers(url)
            results.append(result)

    # Export results
    if args.output:
        export_results(results, args.output, args.format)
    else:
        print(json.dumps(results, indent=4))

    # Generate PoC
    if args.poc:
        print(f"[INFO] Generating PoC for {args.poc}")
        generate_poc(args.poc)

if __name__ == "__main__":
    main()
