RESULTS="res1"

algorithms1="\
dc_bes_200_0 \
dc_ran_200_0 \
dc_dishaumin_200_400 \
dc_dishausum_200_400 \
dc_dismsemin_200_400 \
dc_dismsesum_200_400 \
dc_discli_200_400 \
dc_bes_400_0 \
dc_ran_400_0 \
dc_dishaumin_400_600 \
dc_dishausum_400_600 \
dc_dismsemin_400_600 \
dc_dismsesum_400_600 \
dc_discli_400_600 \
dc_bes_1000_0 \
dc_ran_1000_0 \
"

algorithms2="\
dc_dishaumin_50_100 \
dc_dishausum_50_100 \
dc_dismsemin_50_100 \
dc_dismsesum_50_100 \
dc_discli_50_100 \
dc_bes_200_0 \
dc_ran_200_0 \
dc_bes_400_0 \
dc_ran_400_0 \
dc_bes_1000_0 \
dc_ran_1000_0 \
"

TABLEFILES="temp_tables.tex"
echo "" > "$TABLEFILES"


print_table_opt () {
    cat tools/table_opt_top.txt
    first=1
    for alg in $2; do
        # Line to output summary
        python tools/summary.py "$1"/ "$RESULTS"/"$alg"/"$1"/ > temp.txt
        if [ "$first" -eq 1 ]; then
            cat temp.txt | grep "TOTALS:" -A2
            first=0
        else
            cat temp.txt | grep "TOTALS:" -A2 | tail -n 1
        fi

        # Line to final tables
        echo "Results on $1 with known optima for $(echo $alg | sed -r 's/_/\\_/g')"'\hfill' >> "$TABLEFILES"
        cat tools/table_known_top.txt >> "$TABLEFILES" 
        limit1=$(cat temp.txt | grep -n "BEGINTABLE_KNOWN" | cut -d':' -f1)
        limit2=$(cat temp.txt | grep -n "ENDTABLE_KNOWN" | cut -d':' -f1)
        limit1=$((limit1+1))
        limit2=$((limit2-1))
        x=$(( $limit2 - $limit1 + 1 ))
        tail -n +$limit1 temp.txt | head -${x} >> "$TABLEFILES"
        cat tools/table_bottom.txt >> "$TABLEFILES"
    done
    cat tools/table_bottom.txt
    rm temp.txt
}

print_table_bub () {
    cat tools/table_bub_top.txt
    first=1
    for alg in $2; do
        python tools/summary.py $1/ "$RESULTS"/"$alg"/$1/ > temp.txt
        if [ "$first" -eq 1 ]; then
            cat temp.txt | grep "BUB:" -A2
            first=0
        else
            cat temp.txt | grep "BUB:" -A2 | tail -n 1
        fi
        echo "Results on $1 with \textbf{unknown} optima for $(echo $alg | sed -r 's/_/\\_/g')"'\hfill' >> "$TABLEFILES"
        cat tools/table_unknown_top.txt >> "$TABLEFILES" 
        limit1=$(cat temp.txt | grep -n "BEGINTABLE_UNKNOWN" | cut -d':' -f1)
        limit2=$(cat temp.txt | grep -n "ENDTABLE_UNKNOWN" | cut -d':' -f1)
        limit1=$((limit1+1))
        limit2=$((limit2-1))
        x=$(( $limit2 - $limit1 + 1 ))
        tail -n +$limit1 temp.txt | head -${x} >> "$TABLEFILES"
        cat tools/table_bottom.txt >> "$TABLEFILES"
        echo "$limit1" "$limit2"
    done
    cat tools/table_bottom.txt
    rm temp.txt
}


echo "Table SPLP opt"'\hfill'
print_table_opt "splp" "$algorithms1"
echo '\newpage'

echo "Table SPLP bub"'\hfill'
print_table_bub "splp" "$algorithms1"
echo '\newpage'

echo "Table p-median normal opt"'\hfill'
print_table_opt "pmedian" "$algorithms1"
echo '\newpage'

echo "Table p-median large opt"'\hfill'
print_table_opt "pmedianlarge" "$algorithms2"
echo '\newpage'
