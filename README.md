# Clickjacking Vulnerability Checker & PoC Generator

## Overview
This tool is designed to identify **Clickjacking vulnerabilities** in websites by checking the presence of `X-Frame-Options` and `Content-Security-Policy` headers. It also generates a **Proof of Concept (PoC)** HTML file for vulnerable URLs to demonstrate how the website can be embedded in an iframe.

---

## Features
- **Single URL Check:** Scan a specific URL for Clickjacking vulnerabilities.
- **Bulk URL Check:** Check multiple URLs from a file.
- **Generate PoC HTML:** Create a PoC HTML file to demonstrate the vulnerability.
- **Export Results:** Save the output in various formats, including JSON, CSV, TXT, and XLSX.
- **Customizable Output:** Specify file names and formats for exported results.

---

## Installation
1. Clone this repository or copy the script.
2. Install required dependencies:
   ```bash
   pip install requests xlsxwriter
   ```

---

## Usage
The script supports multiple arguments for flexibility. Below are the available options:

### Arguments
| Argument          | Description                                                      | Example                                      |
|--------------------|------------------------------------------------------------------|----------------------------------------------|
| `--url`           | Check a single URL for vulnerabilities.                         | `--url https://example.com`                  |
| `--bulk`          | File containing multiple URLs to check (one URL per line).       | `--bulk urls.txt`                            |
| `--poc`           | Generate a PoC HTML file for a specific URL.                    | `--poc https://example.com`                  |
| `--output`        | Specify the output file name for results.                       | `--output results.json`                      |
| `--format`        | Specify the output format (json, csv, txt, xlsx). Default: json.| `--format csv`                               |

### Examples
#### Check a Single URL
```bash
python clickjacking_checker.py --url https://example.com
```

#### Check Multiple URLs from a File
```bash
python clickjacking_checker.py --bulk urls.txt --output results.csv --format csv
```

#### Generate a PoC for a Vulnerable URL
```bash
python clickjacking_checker.py --poc https://example.com
```

#### Export Results in XLSX Format
```bash
python clickjacking_checker.py --bulk urls.txt --output results.xlsx --format xlsx
```

---

## Output Example

### **Console Output**
For a single URL, the result is displayed in the console:
```json
[
    {
        "url": "https://example.com",
        "x_frame_options": "Not Set",
        "content_security_policy": "Not Set",
        "vulnerable": true
    }
]
```

### **Exported File (CSV Example)**
| URL               | X-Frame-Options | Content-Security-Policy | Vulnerable |
|--------------------|-----------------|--------------------------|------------|
| https://example.com | Not Set        | Not Set                 | True       |

### **Generated PoC HTML**
The PoC HTML file (`poc.html`) will include the following structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clickjacking PoC</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            display: inline-block;
            width: 800px;
            height: 600px;
            overflow: hidden;
            border: 2px solid #333;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>
    <h1>Clickjacking Proof of Concept</h1>
    <p>The content of the target URL is displayed below:</p>
    <div class="container">
        <iframe src="https://example.com"></iframe>
    </div>
</body>
</html>
```

---

## Notes
- Ensure you have the necessary permissions to test the target URLs.
- This tool is for educational purposes and ethical security testing only.

---

## Author
- **Afif Hidayatullah**
- Organization: ITSEC Asia
- Contact: [Linkedin](https://www.linkedin.com/in/afif-hidayatullah/)
