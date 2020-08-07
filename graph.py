import curses as cs
from config import app
import sys

# local data
vals = []
win = app()

# read given file by path
def read (path):
	global vals
	vals = []

	handler = open(path)
	for val in handler:
		vals.append(float(val))

	handler.close()

# reinitialization	
def reinit (scr):
	global win
	
	win.hei, win.wei = scr.getmaxyx()
	scr.addstr(win.hei - 1, 0, win.mes, cs.color_pair(1)) 

# graph painter
def show (scr, minv, maxv, switch):
	global win
	global vals

	try:
		if win.shift < 0: win.shift = len(vals) - win.zoom + 1
		if win.shift > len(vals): win.shift = 0

		reinit(scr)

		# sample generation
		buf = vals[win.shift : min(win.shift + win.zoom, len(vals))]
		lst = max(1, round(len(buf) / (win.wei - 2)))
		accum = 0
		out = []

		ave = sum(i for i in buf) / len(buf)

		for val in range(len(buf)):
			accum += buf[val]
			
			if not (val + 1) % lst:
				out.append(accum / lst)
				accum = 0

		scr.box()
	   
		if (switch):
			minv = min(out) 
			maxv = max(out)
		# ----------------

		for el in range(0, win.wei - 2):
			for lev in range(1, win.hei - 2): 
				scr.addstr(lev, el + 1, " ", cs.color_pair(3))

			size = win.hei - round((win.hei - 2) * (out[int(el / (win.wei - 2) * len(out))] - minv) / (maxv - minv)) - 1
			if size < 1: size = 1
			elif size > win.hei - 2: size = win.hei - 2

			for lev in range(win.hei - 2, size, -1):
				scr.addstr(lev, el + 1, win.fill, cs.color_pair(3))
			scr.addstr(size, el + 1, win.fillend, cs.color_pair(3))

		scr.addstr(0, win.wei // 2 - 9, " graph - all done ", cs.color_pair(2))
		scr.addstr(1, win.wei // 2 - 9, " " + str(max(win.shift, 0)) + " ~ " + str(min(win.shift + win.zoom, len(vals))) + " ", cs.color_pair(2))

		scr.addstr(1, 1, " %4.2f " % (maxv), cs.color_pair(2))
		scr.addstr(win.hei - 2, 1, " %4.2f " % (minv), cs.color_pair(2))
		scr.addstr(1, win.wei - 8, " %4.2f " % (ave), cs.color_pair(2))
	except:
		scr.box()
		
		try:
			scr.addstr(0, win.wei // 2 - 16, " graph - here are some troubles ", cs.color_pair(2))
			scr.addstr(win.hei - 1, 1, " " + str(win.shift) + " ~ " + str(min(win.shift + win.zoom, len(vals))) + " ", cs.color_pair(2))
		except:
			pass

	scr.refresh()

# command listener
def cmd (scr):
	global vals
	global win

	reinit(scr)
	win.mes = " " * (win.wei - 1)
	buf = ""

	while True:
		reinit(scr)

		try:
			scr.addstr(win.hei - 1, 0, ":" + buf, cs.color_pair(1))
		except:
			pass

		if not len(buf) or buf[len(buf) - 1] != '\n':
			buf += chr(scr.getch())
			if ord(buf[len(buf) - 1]) == 263:
				buf = buf[:len(buf) - 2]
		else:
			try:
				cmds = list(buf.split())
				if cmds[0] == "set":
					if cmds[1] == "shift":
						win.shift = int(cmds[2])
						win.mes = "window postion changed"
					elif cmds[1] == "zoom":
						win.zoom = int(cmds[2])
						win.mes = "zoom changed"
					elif cmds[1] == "floor":
						win.floor = int(cmds[2])
						win.mes = "floor changed"
					elif cmds[1] == "ceil":
						win.ceil = int(cmds[2])
						win.mes = "ceiling changed"
					elif cmds[1] == "autosize":
						win.auto ^= True
						win.mes = "autosize switched"
					else:
						win.mes = "parameter doesn't found"
				elif cmds[0] == "get":
					if cmds[1] == "shift":
						win.mes = str(win.shift)
					elif cmds[1] == "zoom":
						win.mes = str(win.zoom)
					elif cmds[1] == "floor":
						win.mes = str(win.floor)
					elif cmds[1] == "ceil":
						win.mes = str(win.ceil)
					elif cmds[1] == "autosize":
						win.mes = str(win.auto)
					elif cmds[1] == "datasize":
						win.mes = str(len(vals))
					else:
						win.mes = "parameter doesn't found"
					win.mes += " : " + cmds[1]
				elif cmds[0] == "update":
					read(win.path) 
				elif cmds[0] == "q":
					win.status = 0
					exit() 
				else: 
					win.mes = "option doesn't exist"

			except:
				win.mes = "incorrect request"
			
			win.mes += " " * (win.wei - len(win.mes) - 1)
			break

		scr.refresh()

# application runner, also main loop
def main (scr, path):
	global win
	win.path = path
	
	scr.clear()

	for pair in win.colorsets:
		cs.init_pair(pair[0], pair[1], pair[2])

	reinit(scr)
	pad = cs.newwin(win.hei - 1, win.wei, 0, 0) 
	read(win.path)
	
	while win.status:
		reinit(scr)
		key = scr.getkey()

		if key in win.control and win.control[key] == "cmd":
			cmd(scr) 
		else:
			if key in win.control and win.control[key] == "left": win.shift += win.zoom
			elif key in win.control and win.control[key] == "right": win.shift -= win.zoom
			show(pad, win.floor, win.ceil, win.auto) 

if __name__ == "__main__":
	try:
		cs.wrapper(main, sys.argv[1])
	except:
		print("fault: missed path")
