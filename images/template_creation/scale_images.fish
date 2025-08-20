#!/usr/bin/env fish

set input_dir "borderless_raw"
set output_dir "templates_borderless"

mkdir -p $output_dir

for img in $input_dir/*.png
    set filename (basename $img)
    magick $img -resize 52% "$output_dir/$filename"
end

echo "✅ All images processed and saved in $output_dir"
