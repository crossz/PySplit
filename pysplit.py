# PySplit: A program for snapping windows to corners for Linux
# Copyright (C) 2012 Andrew E Slaughter

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import commands
import os

class WindowControl:
	desktop = []
	monitor = []
	active  = []

	# Class constructor
	def __init__(self):
		self.get_screen_size() # set the screen size
		self.get_active_window_location() # get the current window size
		
	# Gathers and stores the screen size
	def get_screen_size(self):
		
		# Clear variables, allows user to call this multiple times
		self.deskop = []
		self.monitor = []
		
		# Extract the text from the "xrandr" command
		x = commands.getoutput('xrandr').replace(',',' ').split(' ')
		
		# Loop through x and extract the connected monitor(s) dimensions
		for i in range(len(x)):
			if x[i] == 'connected':
				s = x[i+1].replace('x','+').split('+')
				self.monitor.append([int(j) for j in s])
				
			if x[i] == 'current':
				self.desktop.append(int(x[i+1]))
				self.desktop.append(int(x[i+3]))
			
	# Get location of the current window
	def get_active_window_location(self):
		
		# Clear the current window size
		self.active = []
		
		# Collects the id of the current window
		x = commands.getoutput("xwininfo -id $(xdpyinfo | grep focus | grep -E -o 0x[0-9a-f]+)").split('\n')

		# Get the absolute x and y coordinates and width and height
		self.active.append(int(x[3].split(':')[1]))
		self.active.append(int(x[4].split(':')[1]))
		self.active.append(int(x[7].split(':')[1]))
		self.active.append(int(x[8].split(':')[1]))
		
	# More and resize window			
	def move(self, x, y, w, h):
		
		# Determine the active window
		window = "-r" + ":ACTIVE:"
		
		# Compute the position to move to on current screen
		p = self.compute_position(x, y, w, h)
	
		#print p
		# Move the window
		#command = "wmctrl " + window + " -b remove,maximized_vert,maximized_horz"
		#os.system(command)
		
		# resize
		#command = "wmctrl " + window +  " -e 0,-1,-1," + str(p[2]) + "," + str(p[3])
		#os.system(command)
		
		# move
		#command = "wmctrl " + window +  " -e 0," + str(p[0]) + "," + str(p[1])+ ",-1,-1"
		#os.system(command)
		
		# set properties
		#command = "wmctrl " + window + " -b remove,hidden,shaded"
		#os.system(command)
		
	def compute_position(self, x, y, w, h):
		
		# Get the active window position and screen size
		a = self.active
		S = self.monitor
		
		# Determine the monitor
		for i in range(len(S)):
			s = S[i]
			if a[0] >= s[2] and a[0] <= (s[2] + s[0]) and a[1] >= s[3] and a[1] <= (s[3] + s[1]):
				idx = i
				
		# Compute the position given the relative position
		p = []
		p.append(int(x*S[idx][0]) + S[idx][2])
		p.append(int(y*S[idx][1]) + S[idx][3])
		p.append(int(w*S[idx][0]))
		p.append(int(h*S[idx][1]))
		
		# Return the position
		return p

def main():
	print "WinSplit.py Demo"
	
	w = WindowControl()
	#print w.desktop
	#print w.monitor
	print w.active
	
	# Move to upper-right of active monitor
	w.move(0.5,0,0.5,0.5)

if __name__ == "__main__":
	main()
