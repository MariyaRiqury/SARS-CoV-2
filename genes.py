import json
import os

import pandas as pd
from Bio import AlignIO

from pathlib import Path

from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from numpy.ma.core import concatenate

# Список папок, где нужно убрать дубликаты
# FOLDERS_TO_DEDUPLICATE = {"XY", "XBB.1.6", "XBB.6.1", "XBB.2.5", "XBB.1.15", "XBB.1.5.11", "XBB.1.5.32", "XBB.1.5.55"}  # можно изменить под ваши нужды


# def remove_duplicate_sequences(alignment):
#     """Удаляет полностью идентичные последовательности"""
#     seen = set()
#     unique_records = []
#
#     for record in alignment:
#         seq_str = str(record.seq)
#         if seq_str not in seen:
#             seen.add(seq_str)
#             unique_records.append(record)
#
#     print(f"Удалено дубликатов: {len(alignment) - len(unique_records)}")
#     return MultipleSeqAlignment(unique_records)

def ref (reference_fasta, reference_gff3):
    alignment = AlignIO.read(reference_fasta, "fasta")
    reference_genes = []
    with open(reference_gff3) as gff:
        for line in gff:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) < 5 or parts[2] not in ['gene', 'CDS']:
                continue
            start = int(parts[3]) - 1
            # end = int(parts[4])
            end = int(parts[4])
            length = end-start
            print(f"длина гена {parts}: {length}")
            sub_alignment = alignment[:,start:end]

            gene_seq = str(sub_alignment[0].seq)  # Фиксируем последовательность
            gene_id = sub_alignment[0].id  # Фиксируем ID
            gene_info = parts[8]  # Фиксируем аннотацию

            reference_genes.append([gene_seq, gene_id, gene_info, start, end])
    # print(reference_genes)
    ref_gen = sorted(reference_genes, key=lambda x: x[4]) #сортировка относительно позиций в геноме
    for i in range (0, len(reference_genes)):
        print(ref_gen[i])
    return ref_gen




# функция, переделывает аннотацию референса согласно новым позициям в выравнивании
def ref_in_alignment(reference_genes, alignment_file):
    parent = alignment_file.parent.name
    output_folder = f"/run/media/riqury/OneTouch/science/result/new_B/for_tree_new/{parent}"

    # # Загружаем список ID последовательностей со стоп-кодонами
    # stop_codon_ids = set()
    # stop_codon_path = "stop_codon_sequences.txt"
    # if Path(stop_codon_path).exists():
    #     with open(stop_codon_path, "r") as f:
    #         for line in f:
    #             stop_id = line.strip()
    #             if stop_id:
    #                 stop_codon_ids.add(stop_id)
    #     print(f"Загружено {len(stop_codon_ids)} последовательностей со стоп-кодонами для исключения.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Обрабатываем папку: {parent}")

    alignment = AlignIO.read(alignment_file, "fasta")

    # # Убираем дубликаты только для нужных папок
    # if parent in FOLDERS_TO_DEDUPLICATE:
    #     print(f"Удаляем дубликаты для папки '{parent}'")
    #     alignment = remove_duplicate_sequences(alignment)



    coordinates = []
    start = reference_genes[0][3]
    end = reference_genes[0][4]
    concatenated = alignment[:, start:end]
    coordinates.append(concatenated.get_alignment_length())

    for i in range(1, len(reference_genes)):
        start = reference_genes[i][3]
        end = reference_genes[i][4]


        sub_alignment = alignment[:, start:end]

        strat = concatenated.get_alignment_length()
        concatenated += sub_alignment
        coord_str = f"{reference_genes[i][2]}: start {strat + 1} end {concatenated.get_alignment_length()} length {concatenated.get_alignment_length() - strat}"
        print(coord_str)

        # Сохраняем только отфильтрованные последовательности
        # AlignIO.write(sub_alignment, f"{output_folder}/{reference_genes[i][2].split("=")[1]}.fasta", "fasta")

    # concatenation
    AlignIO.write(concatenated, f"{output_folder}/concatenated.fasta", "fasta")





def main():
    reference_fasta = "/run/media/riqury/OneTouch/science/result/new_X/data/sars-cov-2/reference.fasta"

    reference_gff3 = "/run/media/riqury/OneTouch/science/result/new_X/data/sars-cov-2/ref.gff"
    reference_genes = ref(reference_fasta, reference_gff3)

    # orf_file = "/run/media/riqury/OneTouch/science/result/new_X/100-1000_X/partitions/ORF1ab.txt"
    # ORF1a(reference_fasta, orf_file)
    align_dir = "/run/media/riqury/OneTouch/science/result/new_B/nextclade_output_2/"
    nextclade_aligned = "nextclade.aligned.cleaned.fasta"

    for file_path in Path(align_dir).rglob(nextclade_aligned):
        ref_in_alignment(reference_genes, file_path)




if __name__ == "__main__":
    main()