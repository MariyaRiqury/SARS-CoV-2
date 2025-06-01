import os
import multiprocessing
#ИСПРАВЛЕННАЯ ВЕРСИЯ ФИЛЬТРА ПОСЛЕДОВАТЕЛЬНОСТЕЙ
# def read_titles_from_file(keys_file):
#     with open(keys_file, 'r', encoding='utf-8', buffering=1024 * 1024) as file1:
#         words = [line.strip() for line in file1]
#         return words

def process_input_file(input_file_path, keys_set, output_folder):
    try:
        with open(input_file_path, 'r', encoding="utf-8") as f:
            # current_file_name = None
            out_f = None
            line = f.readline()
            collecting = False
            while line:
                # print(f"Processing line: {line.strip()}")  # Добавлен вывод
                if line.startswith('>'):
                    if collecting:
                        collecting = False
                        if out_f:
                            out_f.close()
                            out_f = None
                    title_parts = line.split('|')
                    titles_found = title_parts[0][1:]
                    # print(title_parts[0][1:])

                    # Проверка, есть ли titles_found в первом столбце keys_set
                    for word, file_name in keys_set:
                        if titles_found == word:
                            collecting = True
                            print(f"нашли: {titles_found}")
                            keys_set.remove((word, file_name))
                            # current_file_name = file_name
                            output_file_path = os.path.join(output_folder, f'{file_name}.fasta')
                            out_f = open(output_file_path, 'a', encoding="utf-8")
                            break

                if collecting and out_f:
                    out_f.write(line)

                line = f.readline()

            if out_f:
                out_f.close()
                print(f'не найденные ключи {keys_set}')

    except IOError as e:
        print(f"Could not read file: {input_file_path}. Error: {e}")

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

def get_file_name_after_last_underscore(file_name):
    base_name = os.path.basename(file_name)
    name_without_extension = os.path.splitext(base_name)[0]
    return name_without_extension.rsplit('_', 1)[-1]

def process_files_in_directory(directory):
    word_list = set()
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):  # Предположим, что файлы имеют расширение .txt
            file_path = os.path.join(directory, file_name)
            words = read_words_from_file(file_path)

            file_name_after_underscore = get_file_name_after_last_underscore(file_name)
            print(f"name {file_name_after_underscore} count of keys {len(words)}")
            for word in words:
                word_list.add((word, file_name_after_underscore))
    return word_list

# Укажите путь к директории с файлами
directory_path = 'E:/Новая папка/result/for_all_X_more_100_seq_X'
input_file = 'E:/Новая папка/sequences.fasta'  # Входной файл с данными
output_folder = 'E:/Новая папка/result/all_X_from_all'  # Выходной файл

#список ключей
word_list = process_files_in_directory(directory_path)


# Проверяем, существует ли папка для результатов, и создаем её, если нет
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Запуск отбора
process_input_file(input_file, word_list, output_folder)