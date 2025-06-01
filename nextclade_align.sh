#!/bin/bash

# Директории для входных и выходных данных
INPUT_DIR="/run/media/riqury/OneTouch/science/result/new_B/one_line"
OUTPUT_DIR="/run/media/riqury/OneTouch/science/result/new_B/nextclade_output_2"

# Создание выходной директории, если её нет
mkdir -p "$OUTPUT_DIR"

# Обработка каждого файла в INPUT_DIR
for file in "$INPUT_DIR"/*.one_line.fasta; do
    # Проверка, является ли элемент файлом
    if [[ -f "$file" ]]; then
        # Базовое имя файла (без расширения)
        base_name=$(basename "$file" .one_line.fasta)

        # Директория для выходных файлов текущего файла
        output_subdir="$OUTPUT_DIR/$base_name"
        mkdir -p "$output_subdir"

        # Запуск nextclade для текущего файла
        echo "Обработка файла: $file"
        nextclade run \
            --include-reference \
            --input-dataset '/run/media/riqury/OneTouch/science/result/new_X/data/sars-cov-2' \
            --output-all "$output_subdir"/ \
            $file

        # Проверка успешности выполнения
        if [[ $? -eq 0 ]]; then
            echo "Файл успешно обработан: $file"
        else
            echo "Ошибка при обработке файла: $file"
        fi
    fi
done


