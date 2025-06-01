#!/bin/bash

INPUT_DIR_genes="/run/media/riqury/OneTouch/science/result/new_X/100-1000_X/for_hyphy"
INPUT_DIR_tree="/run/media/riqury/OneTouch/science/trees_nwk_X"
OUTPUT_DIR="/run/media/riqury/OneTouch/science/result/new_X/100-1000_X/for_result_log_fel"

for tree_file in $INPUT_DIR_tree/*.nwk;do
	echo "Processing $tree_file..."
	#выделяем название панголинии из названия древесных файлов
	prefix=$(basename "$tree_file")
	pre="${prefix#tree_}"
        suffix="${pre%.nwk}"
	echo "pango lineage: $suffix"

	LOG_FILE="$OUTPUT_DIR/${suffix}_hyphy_log.txt"
	{
        	echo "=========================================="
        	echo "Processing pango lineage: $suffix"
        	echo "Tree file: $tree_file"
                echo "=========================================="
	} >> "$LOG_FILE"

	
	#запускаем цикл по генам
	find "$INPUT_DIR_genes" -type d -name "$suffix" | while read -r dir; do
    		#ищем в подпапке все фасты и запускаем к ним hyphy
		find "$dir" -type f -name "*.fasta" | while read -r genes; do
			echo "$genes"
			{
                		echo "--------------------------------------------------"
                		echo "Processing gene file: $genes"
                		echo "FEL analysis started at: $(date)"
                		echo "--------------------------------------------------"
				hyphy fel --alignment "$genes" --tree "$tree_file" 
				if [ -f "errors.log" ]; then
      					 cp errors.log "$OUTPUT_DIR/${suffix}_errors.log"
       					 rm errors.log
   				fi 
			        #echo "FUBAR analysis started "
                		#echo "--------------------------------------------------"
				#hyphy fubar --alignment "$genes" --tree "$tree_file" 
				# echo "--------------------------------------------------"
			 } >> "$LOG_FILE"

		done 
	done
	
done
