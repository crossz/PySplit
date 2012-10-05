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

	# Class constructor
	def __init__(self):
		self.get_screen_size() # set the screen size
		
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
			
	# More and resize window			
	def move(self, x, y, w, h):
		
		window = "-r" + ":ACTIVE:"
		
		p = self.compute_position(x, y, w, h)
		print p		
		 
		#command = "wmctrl " + window + " -b remove,maximized_vert,maximized_horz"
		#os.system(command)
		# resize
		#command = "wmctrl " + window +  " -e 0,-1,-1," + str(p[2]) + "," + str(p[3])
		#os.system(command)
		# move
		command = "wmctrl " + window +  " -e 0," + str(p[0]) + "," + str(p[1])+ ",-1,-1"
		os.system(command)
		# set properties
		command = "wmctrl " + window + " -b remove,hidden,shaded"
		os.system(command)
		
		#print active
		
		
	def compute_position(self, x, y, w, h):
		
		s = self.monitor[1]
		
		p = []
		p.append(int(x*s[0]))
		p.append(int(y*s[1]))
		p.append(int(w*s[0]))
		p.append(int(h*s[1]))
		
		return p
			
	
def main():
	print "WinSplit.py Demo"
	
	w = WindowControl()
	print w.desktop
	print w.monitor
	
	w.move(0,0,0.33,0.5)


if __name__ == "__main__":
	main()
