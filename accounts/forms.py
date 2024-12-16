from django import forms
from django.core.exceptions import ValidationError
import csv

ALLOWED_FILE_TYPE = ["text/csv"]


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
        data = self.convert_csv_to_dict(uploaded_file)
        return data

    def convert_csv_to_dict(self, uploaded_file):
        # Decode and parse the file into a dictionary
        uploaded_file.seek(0)  # Reset file pointer
        decoded_file = uploaded_file.read().decode("utf-8")
        reader = csv.DictReader(decoded_file.splitlines())
        # Convert headers to lowercase
        reader.fieldnames = [field.lower() for field in reader.fieldnames]
        return [row for row in reader]  # Return arr of dict that contain accounts
