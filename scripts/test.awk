BEGIN { sum=0; anon=0 }
/^[0-9a-f]+-[0-9a-f]+/ {
    anon = ($2 ~ /rw-p/ && $4 == "00:00")
    if (anon) print "find anonymous page: "$0
    next
}
anon && /^Rss:/ {
    sum += $2
}
END { print sum }
