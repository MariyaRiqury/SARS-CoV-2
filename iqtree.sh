#!/bin/bash

INPUT_DIR="/run/media/riqury/OneTouch/science/result/new_X/100-1000_X/for_tree_new"
PARTITIONS=PARTITIONS="/run/media/riqury/OneTouch/science/result/new_X/100-1000_X/partitions/partitions.nex"
ALIGNMENT_FILE="concatenated.fasta"
NUM_CORES=4

find "$INPUT_DIR" -type f -name "$ALIGNMENT_FILE" | while read -r alignment; do
    # Извлекаем название подпапки
    subfolder_name=$(basename $(dirname "$alignment"))
    
    # Шаг 1: Строим дерево (можно с AUTO)
    iqtree -s "$alignment" \
           -m MFP \
           -o "MN908947" \
           -T AUTO \
           --prefix "${subfolder_name}"
done

