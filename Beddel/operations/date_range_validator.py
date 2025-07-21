import re
from datetime import datetime
import dateparser
import os

def process(doc, input_path=None, out_dir=None, start_date=None, end_date=None, **kwargs):
    out_of_range_dates = []
    date_pattern = r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\w+ \d{4}\b|\b\d{4}-\d{2}-\d{2}\b)"

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for para in doc.paragraphs:
        matches = re.findall(date_pattern, para.text)
        for match in matches:
            parsed = dateparser.parse(match)
            if parsed:
                if parsed < start or parsed > end:
                    out_of_range_dates.append((match, parsed.date()))

    if not input_path:
        input_path = doc._part.package.package.filename
    if not out_dir:
        out_dir = os.path.dirname(input_path)

    if out_of_range_dates:
        report_path = os.path.join(out_dir, "date_validation_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"📄 {os.path.basename(input_path)} — Out-of-range dates found:\n")
            for match, date in out_of_range_dates:
                f.write(f"❌ '{match}' → {date} is OUTSIDE the range {start_date} to {end_date}\n")
        print(f"📄 Written validation report to {report_path}")
    else:
        print(f"✅ No out-of-range dates found in {os.path.basename(input_path)}")
