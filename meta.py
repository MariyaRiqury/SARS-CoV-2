#скрипт, который соберет файл с ключами для всех X или B

# Собираем из метаданных все панго начинающихся с вводимой буквы и создаем таблицу с количеством образцов для каждой
import os
from collections import Counter

import pandas as pd


def count_words_in_file(input_file_path, output_file_path, output_file_path_100):
    # Открываем файл и читаем содержимое
    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Читаем строки и удаляем лишние пробелы
        # Разбиваем строки на две части по пробелу и берем только первую часть
        words = [line.strip().split()[0] for line in file if line.strip()]

    # Подсчитываем количество вхождений каждого слова
    word_count = Counter(words)

    # Сохраняем результат в отдельный файл
    with open(output_file_path, 'w', encoding='utf-8') as output_file, open(output_file_path_100, 'w', encoding='utf-8') as output_file_100:
        for word, count in word_count.items():
            output_file.write(f"{word};{count}\n")
            if count >= 100:
                output_file_100.write(f"{word};{count}\n")


  # Имя выходного файла
# output_fName1 = 'output_count_metadata_keys_X.txt'
# , open(output_fName1, 'w', encoding="utf-8") as out_f1
def all_names(input_fName,output_fName, point):
    fs = "\t"
    table = str.maketrans('\t', fs)
    with open(input_fName, 'r', encoding="utf-8") as f, open(output_fName, 'w', encoding="utf-8") as out_f1:
        i = 0
        line = f.readline()

        while line:
            i += 1
            a = line.translate(table)
            columns = a.split(fs)

            # Здесь указываем индексы нужных столбцов (например, 0 и 2)
            selected_columns = [columns[13], columns[4], columns[0]]
            # columns[0], columns[4], columns[5], columns[12],
            # columns[13], columns[9]
            # Измените индексы по необходимости
            # print('\t'.join(selected_columns))
            if columns[9] == 'Human':
                if columns[13].startswith(point):
                    # out_f1.write('\t'.join(selected_columns) + '\n')  # Записываем в выходной файл
                    # print(columns[4], columns[5], columns[13])
                    print('\t'.join(selected_columns))
                    out_f1.write('\t'.join(selected_columns) + '\n')

                    # Str = columns[0]
                    # name = Str.split("/")
                    # print(columns[0] + '\t' + name[2])
                    # out_f.write(name[2] + '\n')

            line = f.readline()
    print("первая часть все")

def main():

    print("введите букву панголиний: ")
    p = input()
    point = p.upper()
    input_fName = 'metadata.tsv'
    output_fName = f'./metadata_count/output__metadata_keys_{point}_for_data.txt'
    all_names(input_fName, output_fName, point) #собирает файл с названием панголинии индификационным номером и названием


    # input_file_path = f'./metadata_count/output__metadata_keys_{point}_for_data.txt'
    output_file_path = f'./metadata_count/count_result_{point}.csv'
    output_file_path_100 = f'./metadata_count/count_result_{point}_more_100.csv'
    count_words_in_file(output_fName, output_file_path, output_file_path_100) #считает сколько образцов для каждой панголинии

    # print(f"Подсчет слов завершен. Результаты сохранены в '{output_file_path}'.")

    d_count = pd.read_table(output_file_path_100, sep=';', header=None, low_memory=False,
                           na_values=['NA'])
    d_count.columns = ['Pango lineage', 'count']
    print(d_count)
    # files = os.listdir(folder_for_names)
    # print(files)
    data = pd.read_table(output_fName, sep='\t', header=None, low_memory=False,
                           na_values=['NA'])
    data.columns = ['Pango lineage', 'Accession ID', 'Virus name']
    folder_for_names = f'./for_all_more_100_seq_1000_max_{point}'
    for index, row in d_count.iterrows():
        key = row['Pango lineage']
        count = row['count']
        result_df = pd.DataFrame()
        filtered_data = data[data['Pango lineage'] == key]
        filtered_data1 = filtered_data['Virus name'].drop_duplicates()
        print(f'количество отфильтрованных {filtered_data1.shape[0]}')
        if not filtered_data.empty:
            if count > 1000:
                random_samples = filtered_data1.sample(n=1000)
                result_df = pd.concat([result_df, random_samples], ignore_index=True)
            else:
                result_df = pd.concat([result_df, filtered_data1], ignore_index=True)
            file_name_result = f"{key}.txt"
            output_file_path = os.path.join(folder_for_names, file_name_result)
            result_df.to_csv(output_file_path, index=False, header=False)
            print("создан файл " + key)
        # file_name = f"{folder_for_names}/file{key}.txt"
#сохраняет 100 рандомных названий образцов отдельными файлами для каждой панголинии
if __name__ == "__main__":
    main()

