import os

import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read(10000)  # Анализируем первые 10КБ
    return chardet.detect(rawdata)['encoding']



def filtering(fasta_input_dir, nextclade_dir_path, fasta_output_dir):
    fasta_non_filtered = os.listdir(fasta_input_dir)
    good = []

    for file in fasta_non_filtered:
        name = os.path.splitext(file)[0]
        print(name)

        nextclade = os.path.join(nextclade_dir_path, f'{name}.fasta.csv' )
        print(nextclade)
        qc = pd.read_csv(nextclade, sep=';', header=0, low_memory=False)
        qc1 = (
            # data[data['qc.overallStatus'] != 'bad']  # Фильтрация
            qc[(qc['qc.overallStatus'] == 'good') & (qc['Nextclade_pango'] == name)] # Фильтрация
            .assign(seqName=lambda x: x['seqName'].str.strip())  # Преобразование столбца
        )

        good.append((name, qc1.shape[0]))
        duplicate_counts = qc1.duplicated().sum()
        print(f"Количество дубликатов: {duplicate_counts}")
        if len(qc1)>100:
            result = qc1.sample(n = 100)
        else:
            result = qc1
        print(len(result))
        out_f_path = os.path.join(fasta_output_dir, f'{name}.fasta')


        if len(result) >= 80:
            out_f = open(out_f_path, 'w', encoding='utf-8')

            file_path = os.path.join(fasta_input_dir, file)
            encoding = detect_encoding(file_path)
            lines = []
            with open(file_path, 'r', encoding=encoding) as f:
                line = f.readline()
                collecting = False
                while line:
                    if line.startswith('>'):
                        collecting = False
                        line1 = line[1:].strip()
                        if result['seqName'].isin([line1]).any() and line not in lines:
                            collecting = True
                            lines.append(line)
                            # print('нашли')
                    if collecting:
                        out_f.write(line)
                    line = f.readline()
            print(len(lines))
            if out_f:
                out_f.close()
                # print("закончили")

    # print(f' хорошие образцы: {good}')
    df = pd.DataFrame(good)
    print(df)
    df.to_csv('output.csv', index=False, header=False)

def main():

    nextclade= '/run/media/riqury/OneTouch/science/result/new_B/nextclade_output'
    fasta_input_dir = '/run/media/riqury/OneTouch/science/result/all_B_from_all'
    output_folder = '/run/media/riqury/OneTouch/science/result/new_B/fasta_good_filtered_by_nextclade_B_3'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filtering(fasta_input_dir, nextclade, output_folder)



if __name__=='__main__':
    main()