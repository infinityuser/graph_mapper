import curses as cs

class app:
	# session configuration
	status = 1
	shift = 0
	zoom = 4000
	hei = 0
	wei = 0
	ceil = 100
	floor = 0
	mes = ""
	path = ""
	auto = False

	# chart theme 
	fillend = "▄"
	fill = "█"
	
	colorsets = [
		(1, cs.COLOR_BLACK, cs.COLOR_WHITE),
		(2, cs.COLOR_BLACK, cs.COLOR_WHITE),
		(3, cs.COLOR_WHITE, cs.COLOR_BLACK),
	]

	# key bindings 
	control = {
		":" : "cmd",
		"l" : "left",
		"h" : "right",
	}
