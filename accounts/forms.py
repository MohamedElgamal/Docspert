from django import forms
from django.core.exceptions import ValidationError
import csv

ALLOWED_FILE_TYPE = ["text/csv", "text/plain"]
REQUIRED_HEADERS = ["ID", "Name", "Balance"]


class AccountsUploadForm(forms.Form):
    file = forms.FileField(
        label="Select file that contain accounts details.",
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if uploaded_file.content_type not in ALLOWED_FILE_TYPE:
            raise ValidationError(
                f"your are trying to upload unsupported file ext. allowed ext {', '.join(ALLOWED_FILE_TYPE)}."
            )
        # Add Content validation
        try:
            if uploaded_file.content_type == ALLOWED_FILE_TYPE[0]:
                data = self.convert_csv_to_dict(uploaded_file)
            elif uploaded_file.content_type == ALLOWED_FILE_TYPE[1]:
                data = self.convert_txt_to_dict(uploaded_file)
        except ValidationError:
            raise ValidationError(
                f"File is not valid may be empty or not in correct structure, expected structure: {', '.join(REQUIRED_HEADERS)}"
            )
        return data

    def convert_csv_to_dict(self, uploaded_file):
        """Responsible of converting csv data to dict to return it to view"""
        # Decode and parse the file into a dictionary
        uploaded_file.seek(0)  # Reset file pointer
        decoded_file = uploaded_file.read().decode("utf-8")
        reader = csv.DictReader(decoded_file.splitlines())
        if (
            reader.fieldnames != REQUIRED_HEADERS
        ):  # if csv file not containing the required headers, raise ValidationError
            raise ValidationError("CSV may be empty or not in correct structure.")
        # Convert headers to lowercase
        reader.fieldnames = [field.lower() for field in reader.fieldnames]
        return [row for row in reader]  # Return arr of dict that contain accounts
    
    def convert_txt_to_dict(self, uploaded_file):
        """Responsible of converting text data to dict to return it to view"""
        uploaded_file.seek(0)  # Reset file pointer
        decoded_file = uploaded_file.read().decode("utf-8")
        lines = decoded_file.splitlines()
        if not lines:
            raise ValidationError("TXT file is empty.")
        # Assuming the first line contains headers
        headers = lines[0].split("\t")  # Using tab as the delimiter for TXT
        if set(headers) != set(REQUIRED_HEADERS):
            raise ValidationError("TXT does not have the required headers.")
        # Convert headers to lowercase for consistency
        headers = [header.lower() for header in headers]
        return [
            dict(zip(headers, line.split("\t"))) for line in lines[1:]
        ]  # Parse rows into a list of dicts