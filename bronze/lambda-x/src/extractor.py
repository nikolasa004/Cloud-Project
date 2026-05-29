"""
Ekstraktor podataka sa X (Twitter) mreže iz Staging S3 bucketa.
Odvaja logiku čitanja i filtriranja od AWS Lambda handlera.
"""
import csv
import io
import boto3

s3_client = boto3.client("s3")

def extract_x_data_for_date(staging_bucket: str, file_key: str, target_date: str) -> tuple[str, int]:
    """
    Preuzima CSV iz Staging bucketa, filtrira ga po datumu i vraća filtrirani CSV string.
    """

    response = s3_client.get_object(Bucket=staging_bucket, Key=file_key)
    lines = response['Body'].read().decode('utf-8').splitlines()


    reader = csv.DictReader(lines)
    fieldnames = reader.fieldnames


    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    count = 0

    for row in reader:
        if row.get('date', '').startswith(target_date):
            writer.writerow(row)
            count += 1

    return output.getvalue(), count