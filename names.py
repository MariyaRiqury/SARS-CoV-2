
import re
from Bio import SeqIO
from pathlib import Path

def sanitize_id(description):
    """Заменяет все спецсимволы и пробелы на _"""
    return re.sub(r"[^a-zA-Z0-9_]", "_", description)

def process_fasta_file(fasta_path):
    print(f"Обработка файла: {fasta_path}")
    new_records = []

    for record in SeqIO.parse(fasta_path, "fasta"):
        # Берём полный заголовок (description), меняем недопустимые символы на _
        full_description = record.description.strip()
        clean_id = sanitize_id(full_description)

        # Обновляем поля
        record.id = clean_id
        record.name = clean_id
        record.description = ""  # Очищаем, чтобы не дублировались при записи

        new_records.append(record)

    # Сохраняем в новый файл
    output_path = fasta_path.with_suffix(".cleaned.fasta")
    SeqIO.write(new_records, output_path, "fasta")
    print(f"Сохранено: {output_path}")

def main():
    root_folder = "/run/media/riqury/OneTouch/science/result/new_B/nextclade_output_2"
    print("Начинаем обработку...")

    for path in Path(root_folder).rglob("nextclade.aligned.fasta"):
        process_fasta_file(path)

if __name__ == "__main__":
    main()