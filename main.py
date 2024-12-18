import zipfile
import os
import re  # Importing the regex module
import sys

file_path = sys.argv[1]

print(f"File path received: {file_path}")


def add_clear_to_filename(file_path):
    # Split the file path into the base and extension
    base, ext = os.path.splitext(file_path)

    # Add '_clear' to the base name and join with the extension
    new_file_path = f"{base}_clear{ext}"

    return new_file_path


def is_encrypted(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Check if the file is encrypted by trying to read a file from it
            zip_ref.testzip()  # Will return None if no errors, or the first bad file
            return False
    except RuntimeError as e:
        if 'encrypted' in str(e).lower():
            return True
        else:
            raise


def rename_files_in_zip(zip_path, output_zip_path, exclude_files=None, pattern_to_remove="[SW.BAND]", password=None):
    if exclude_files is None:
        exclude_files = []

    print(exclude_files)

    # Check if the zip file is encrypted and open accordingly
    if is_encrypted(zip_path):
        print(f"The file {zip_path} is encrypted. Trying to use a password.")
        with zipfile.ZipFile(zip_path, 'r') as src_zip:
            src_zip.setpassword(password.encode())
            # Create a new zip file for the renamed files
            with zipfile.ZipFile(output_zip_path, 'w') as dest_zip:
                for item in src_zip.infolist():
                    file_name = os.path.basename(item.filename)
                    print("Обрабатываем файл: " + file_name)
                    if file_name in exclude_files:
                        print("Пропускаем файл: " + file_name)
                        continue
                    # Remove the [SW.BAND] pattern from the filename
                    new_name = item.filename.replace(pattern_to_remove, "").strip()

                    # Removing space after each slash in the path
                    new_name = re.sub(r'/ ', '/', new_name)
                    new_name = re.sub(r' /', '/', new_name)

                    print(new_name)
                    # Read file content
                    with src_zip.open(item.filename) as file_data:
                        # Write the file with the new name to the destination zip
                        dest_zip.writestr(new_name.strip(), file_data.read())

        print(f"Updated archive saved at {output_zip_path}")
    else:
        print(f"The file {zip_path} is not encrypted. Processing normally.")
        # Proceed with the regular unencrypted zip file processing
        with zipfile.ZipFile(zip_path, 'r') as src_zip:
            with zipfile.ZipFile(output_zip_path, 'w') as dest_zip:
                for item in src_zip.infolist():
                    file_name = os.path.basename(item.filename)
                    print("Обрабатываем файл: " + file_name)
                    if file_name in exclude_files:
                        print("Пропускаем файл: " + file_name)
                        continue
                    # Remove the [SW.BAND] pattern from the filename
                    new_name = item.filename.replace(pattern_to_remove, "").strip()

                    # Removing space after each slash in the path
                    new_name = re.sub(r'/ ', '/', new_name)
                    new_name = re.sub(r' /', '/', new_name)

                    print(new_name)
                    # Read file content
                    with src_zip.open(item.filename) as file_data:
                        # Write the file with the new name to the destination zip
                        dest_zip.writestr(new_name.strip(), file_data.read())

        print(f"Updated archive saved at {output_zip_path}")


# Exclude files from renaming
exclude_files = [
    "[WWW.SW.BAND] 150000 курсов ждут тебя!.url",
    "[WWW.SW.BAND] Прочти перед изучением!.docx",
    "[DMC.RIP] Качай редкие курсы!.url",
    "SHAREWOOD_ZERKALO_COM_90000_курсов_на_нашем_форуме!.url",

]

# Specify the source and output zip paths
zip_path = file_path  # Original archive
output_zip_path = add_clear_to_filename(zip_path)  # New archive

# Password for encrypted zip (if known)
password = 'SW.BAND'  # Replace with your password

print(zip_path)
print(output_zip_path)

rename_files_in_zip(zip_path, output_zip_path, exclude_files, password=password)
