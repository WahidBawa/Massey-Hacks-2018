from random import *
vals = [1,14,96]
width, height = 30, 17
with (open("Maps/64.tmx", 'w')) as f:
	f.write('''<?xml version="1.0" encoding="UTF-8"?>
<map version="1.0" tiledversion="1.1.2" orientation="orthogonal" renderorder="right-down" width="30" height="17" tilewidth="64" tileheight="64" infinite="0" nextobjectid="1">
 <tileset firstgid="1" name="t1" tilewidth="64" tileheight="64" spacing="10" tilecount="540" columns="27">
  <image source="../Sprites/Spritesheet/spritesheet_tiles.png" width="1988" height="1470"/>
 </tileset>
 <layer name="Tile Layer 1" width="30" height="17">
  <data encoding="csv">
''')
	c = choice(vals)
	grid = ""
	for y in range(height):
		for x in range(width):
			grid += "%d," % c
		grid += "\n"

	grid = grid[:-2] + "\n"
	# print(grid)
	f.write(grid)

	f.write("</data>\n </layer></map>\n")

