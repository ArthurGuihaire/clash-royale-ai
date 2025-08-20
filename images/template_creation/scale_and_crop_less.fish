set input_image $argv[1]
set output_image $argv[2]

# Check if input file exists
if not test -f $input_image
    echo "Error: '$input_image' not found."
    exit 1
end

# Scale image by 50% using ImageMagick
# Normal scale: 150x165
magick "$input_image" -resize 245x -gravity center -crop 170x185+0+10 +repage "$output_image"
