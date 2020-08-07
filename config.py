import curses as cs

class app:
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

	fillend = "▄"
	fill = "█"

	colorsets = [
		(1, cs.COLOR_BLACK, cs.COLOR_WHITE),
		(2, cs.COLOR_BLACK, cs.COLOR_WHITE),
		(3, cs.COLOR_WHITE, cs.COLOR_BLACK),
	]

	control = {
		":" : "cmd",
		"l" : "left",
		"h" : "right",
	}
