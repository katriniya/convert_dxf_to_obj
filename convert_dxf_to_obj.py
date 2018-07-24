#! /usr/bin/env python
# coding: utf-8

import sys
import dxfgrabber

def convertLines(lines, vertexes, faces, index, height_room):

	resultVertexes = vertexes
	resultFaces = faces
	resultIndex = index

	for item in (lines):
		resultVertexes = resultVertexes + 'v ' + str(item.start[0])+ ' ' + str(item.start[2]) + ' ' + str(item.start[1]) +'\n' 
		resultVertexes = resultVertexes + 'v ' + str(item.end[0])  + ' ' + str(item.end[2])   + ' ' + str(item.end[1]) +'\n'
		resultVertexes = resultVertexes + 'v ' + str(item.end[0])  + ' ' + str(item.end[2]  + height_room )   + ' ' + str(item.end[1]) +'\n'
		resultVertexes = resultVertexes + 'v ' + str(item.start[0])+ ' ' + str(item.start[2] + height_room) + ' ' + str(item.start[1]) +'\n'
		
		resultFaces = resultFaces + 'f '
		for i in range(4): 
			resultIndex +=1
			resultFaces  =resultFaces  +' '  + str(resultIndex)
		resultFaces  = resultFaces + '\n'
	
	return (resultVertexes,resultFaces, resultIndex)

def convertPolylines(polylines, vertexes, faces, index, height_room):

	resultVertexes = vertexes
	resultFaces = faces
	resultIndex = index

	for item in (polylines):

		for point in (item.points):
			resultVertexes += 'v ' + str(point[0]) +' ' + str(point[2] if len(point)==3 else '0.0')+' '+ str(point[1]) + ' ' +  '\n'
			resultVertexes += 'v ' + str(point[0]) +' ' + str(point[2]+height_room if len(point)==3 else height_room)+' '+ str(point[1]) + ' ' +  '\n'

		# add connect first polyline point to last polyline point 
		if (len(item.points)>2):
			resultFaces = resultFaces+ 'f ' +str(resultIndex+1) + ' ' +str(2+resultIndex) + ' ' +str( len(item.points) *2 +resultIndex) + ' ' +str( len(item.points) *2 -1 +resultIndex) + '\n'

		for i in range(len(item.points)-1):
			resultFaces = resultFaces+ 'f ' +str(resultIndex+1) + ' ' +str(2+resultIndex) + ' ' +str(4+resultIndex) + ' ' +str(3+resultIndex) + '\n'
			resultIndex+=2

		resultIndex+=2

	return (resultVertexes,resultFaces, resultIndex)

def main():
	if (len(sys.argv)!=4):
		print ("use with params <input file> <output file> <height room>")
		return

	dxf = dxfgrabber.readfile(sys.argv[1])
	height_room = float(sys.argv[3])
	
	lines = [entity for entity in dxf.entities if entity.dxftype == 'LINE']
	polylines = [entity for entity in dxf.entities if entity.dxftype == 'LWPOLYLINE']

	vertexes  = ''
	faces = ''
	index = 0

	result = convertLines(lines, vertexes, faces, index, height_room)
	vertexes = result[0]
	faces = result[1]
	index = result[2]
	
	result = convertPolylines(polylines, vertexes, faces, index, height_room)
	vertexes = result[0]
	faces = result[1]
	index = result[2]


	file = open(sys.argv[2], 'w+')
	file.write(vertexes)
	file.write(faces)
	file.close()

if __name__== "__main__":
  main()