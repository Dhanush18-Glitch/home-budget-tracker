import csv
from io import StringIO
from flask import Response


def safe_cell(value):
    text = str(value if value is not None else "")
    return "'" + text if text.startswith(("=", "+", "-", "@")) else text


def csv_response(filename, headers, rows):
    output = StringIO(); writer = csv.writer(output)
    writer.writerow(headers)
    for row in rows: writer.writerow([safe_cell(value) for value in row])
    return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
