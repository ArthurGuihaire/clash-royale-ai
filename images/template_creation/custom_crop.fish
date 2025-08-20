#!/usr/bin/env fish

# Check arguments
if test (count $argv) -ne 6
    echo "Usage: custom_crop.fish <input_image> <output_image> <left> <top> <right> <bottom>"
    exit 1
end

set input_image $argv[1]
set output_image $argv[2]
set left $argv[3]
set top $argv[4]
set right $argv[5]
set bottom $argv[6]

# Validate input file
if not test -f $input_image
    echo "Error: '$input_image' not found."
    exit 1
end

# Get original dimensions
set width (magick identify -format "%w" $input_image)
set height (magick identify -format "%h" $input_image)

# Calculate new dimensions
set new_width (math "$width - $left - $right")
set new_height (math "$height - $top - $bottom")

if test $new_width -le 0 -o $new_height -le 0
    echo "Error: Crop dimensions are invalid."
    exit 1
end

# Perform crop (note: no curly braces in Fish variables)
magick $input_image -crop "$new_width"x"$new_height"+"$left"+"$top" +repage $output_image

if test $status -eq 0
    echo "Image cropped to $new_width x $new_height and saved to '$output_image'"
else
    echo "Error: Failed to crop image."
    exit 1
end
