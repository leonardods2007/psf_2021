 #!/bin/bash
 while true;
 do
    date=$(stat -c %y "$1")
    while sleep 0.2; do date2=$(stat -c %y "$1")
      if [[ $date2 != $date ]]; then
         p3.sh $1
         break;
      fi
      # possibly exit [status] instead of break
      # or if you want to watch for another change, date=$date2
   done
done
