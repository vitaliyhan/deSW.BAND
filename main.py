import zipfile
import os
import re  # Importing the regex module


def rename_files_in_zip(zip_path, output_zip_path, exclude_files=None, pattern_to_remove="[SW.BAND]"):
    if exclude_files is None:
        exclude_files = []

    print(exclude_files)
    # Открываем исходный ZIP-архив
    with zipfile.ZipFile(zip_path, 'r') as src_zip:
        # Создаем новый ZIP-архив для обновленных файлов
        with zipfile.ZipFile(output_zip_path, 'w') as dest_zip:
            for item in src_zip.infolist():
                file_name = os.path.basename(item.filename)
                print("Обрабатываем файл: " + file_name)
                if file_name in exclude_files:
                    print("Пропускаем файл: " + file_name)
                    continue
                # Убираем [SW.BAND] из имени файла
                new_name = item.filename.replace(pattern_to_remove, "").strip()

                # Removing space after each slash in the path
                new_name = re.sub(r'/ ', '/', new_name)
                new_name = re.sub(r' /', '/', new_name)

                print(new_name)
                # Читаем содержимое файла
                with src_zip.open(item.filename) as file_data:
                    # Записываем файл с новым именем
                    dest_zip.writestr(new_name.strip(), file_data.read())

    print(f"Обновленный архив сохранен в {output_zip_path}")


exclude_files = [
    "[WWW.SW.BAND] 150000 курсов ждут тебя!.url",
    "[WWW.SW.BAND] Прочти перед изучением!.docx",
    "[DMC.RIP] Качай редкие курсы!.url"
]

# Укажите путь к исходному архиву и путь для сохранения нового архива
zip_path = "input.zip"  # Исходный архив
output_zip_path = "output.zip"  # Новый архив

rename_files_in_zip(zip_path, output_zip_path, exclude_files)
