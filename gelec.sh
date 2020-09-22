#/bin/bash
for i in 546 707 869 1026 1026-2 1026-3 1026-4 1191 1358 1509;do
    echo $i;
    python ginter.py -1 20200905gtem/B$i > 20200905gtem/B$i.log;
done