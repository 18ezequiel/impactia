import csv

with open('output.csv', newline='', encoding='utf-8') as f_in, open('archivo_etl.csv', 'w', newline='', encoding='utf-8') as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    header = next(reader)
    writer.writerow(header)
    for row in reader:
        if row != header:
            writer.writerow(row)