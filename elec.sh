#/bin/bash
for i in 554 680 808-4 824 828-2 828-3 936 1048 1152 1296;do
    echo $i;
    python inter.py -1 20200905/D$i > 20200905/D$i.png.log;
done