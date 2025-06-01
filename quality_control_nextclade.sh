#!/bin/bash

# Активация окружения Conda
eval "$(conda shell.bash hook)"
conda activate nextclade

# Проверка, акти./вировано ли окружение
if [[ -z "$CONDA_DEFAULT_ENV" ]]; then
    echo "Ошибка: окружение Conda не активировано."
    exit 1
fi

# Путь к директории с файлами
INPUT_DIR="/run/media/riqury/OneTouch/science/result/pupu1"
OUTPUT_DIR="/run/media/riqury/OneTouch/science/result/new_B/nextclade_output"
BAD_FILES_DIR="/run/media/riqury/OneTouch/science/result/new_B/NON_UTF-8"

# Проверка, существует ли директория
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Ошибка: директория $INPUT_DIR не существует."
    exit 1
fi

# Проверка, есть ли файлы в директории
if [[ -z "$(ls -A "$INPUT_DIR")" ]]; then
    echo "Ошибка: директория $INPUT_DIR пуста."
    exit 1
fi

# Создание выходной директории, если её нет
mkdir -p "$OUTPUT_DIR"
mkdir -p "$BAD_FILES_DIR"

# Цикл по всем файлам в директории
for file in "$INPUT_DIR"/*; do
    # Проверка, является ли элемент файлом
    if [[ -f "$file" ]]; then
        # Имя выходного файла
        output_csv="$OUTPUT_DIR/$(basename "$file").csv"
	
	encoding=$(file -b --mime-encoding "$file")
	 if [[ "$encoding" != "utf-8" && "$encoding" != "us-ascii" ]]; then
            echo "Найден файл не в UTF-8: $file (кодировка: $encoding)"
            # Перемещаем в папку non_utf8_files
            mv "$file" "$BAD_FILES_DIR/"
            echo "Файл перемещён в $BAD_FILES_DIR/"
        else
            echo "Файл в UTF-8/ASCII: $file"
        fi



        # Запуск nextclade для текущего файла
        echo "Обработка файла: $file"
        nextclade run \
            --input-dataset '/run/media/riqury/OneTouch/science/result/new_X/data/sars-cov-2' \
            --output-csv "$output_csv" \
            "$file"

        # Проверка успешности выполнения
        if [[ $? -eq 0 ]]; then
            echo "Файл успешно обработан: $file"
        else
            echo "Ошибка при обработке файла: $file"
        fi
    fi
done

# Деактивация окружения Conda
conda deactivate
