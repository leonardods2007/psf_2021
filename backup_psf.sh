rclone sync . gps:psf_2021_material/ -P -L -v  --delete-excluded --exclude=/shared/** --exclude=log.bin --bwlimit="08:00,20 03:00,1M"


