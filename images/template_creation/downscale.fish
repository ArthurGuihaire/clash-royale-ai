#!/usr/bin/env fish

set input_dir "templates_borderless"
set output_dir "templates_tiny"

mkdir -p $output_dir

for img in $input_dir/*.png
    set filename (basename $img)
    magick $img -resize 50% "$output_dir/$filename"
end