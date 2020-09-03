convert icon.svg -define icon:auto-resize=16,32,48,128,256 -alpha on -background transparent -transparent white -compress zip icon.ico

convert -size 256x256 icon.svg icon256.png
convert -size 128x128 icon.svg icon128.png
convert -size 48x48 icon.svg icon48.png
convert -size 32x32 icon.svg icon32.png
convert -size 16x16 icon.svg icon16.png

pause