import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

########################################################################

def file_open() :
    filename = filedialog.askopenfilename(
        initialdir = "D:/",
        title = "Open A File",
        filetype = (("xlsx files", "*.xlsx"), ("All Files", "*.*"))
        )
    if filename :
        try :
            filename = r"{}".format(filename)
            df = pd.read_excel(filename)
        except ValueError :
            my_label.config(text = "File couldn't be open")
        except FileNotFoundError :
            my_label.config(text = "File not found")

class StatusBar(tk.Frame):   
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.variable=tk.StringVar()        
        self.label=tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                           textvariable=self.variable,
                           font=('arial',16,'normal'))
        self.variable.set('Status Bar')
        
def read_excel(excel) :
	df = pd.read_excel(excel)
	if 'Unnamed: 0' in df.columns :
		df.drop('Unnamed: 0', axis = 1, inplace = True)

	if 'Unnamed: 0.1' in df.columns :
		df.drop('Unnamed: 0.1', axis = 1, inplace = True)

	return df
		
def newfolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print ('Error: Creating directory. ' +  directory)


def newfolderlist(directory, folderlist):
	for i, names in enumerate(folderlist):
		directory_temp = directory + '\\' + names
		try:
			if not os.path.exists(directory_temp):
				os.makedirs(directory_temp)
		except OSError:
			print ('Error: Creating directory. ' +  directory_temp)
			
class Input_box() :
	def __init__(self, input_dir) :
		self.reload(input_dir)
				
	def reload(self, input_dir) :
		check = 'ready'
		if (len(os.listdir(input_dir)) >= 2) | (len(os.listdir(input_dir)) == 0) :
			check = "place only one excel file in '1_INPUT_HERE' folder"
			
		else :
			os.chdir(input_dir)
			df = read_excel(os.listdir(input_dir)[0])
			self.df = df
			
			self.excel_name = os.listdir(input_dir)[0]
			self.num_of_groups = len(df.loc[:, 'group'].unique())
			self.num_of_variables = len(df.columns) - 1
			self.num_of_profiles = df.shape[0]
			
			self.num_of_groups = str(self.num_of_groups)
			self.num_of_variables = str(self.num_of_variables)
			self.num_of_profiles = str(self.num_of_profiles)
			self.columns = df.columns
			
			if len(df.columns) > 6 :
				self.name_of_variables = str(df.columns.tolist()[1 : 4])[ : -1] + ' ... ' + str(df.columns.tolist()[ -3 :])[1 :]
			else :
				self.name_of_variables = str(df.columns.tolist()[1 : ])

def refresh(input_dir, width_1, height_1, excel_name_frame, info_frame, input_box, label_excel_name, entry_1, entry_2, entry_3, entry_4) :
	print('reloading...')
	input_box.reload(input_dir)
	label_excel_name = ttk.Label(excel_name_frame, text = input_box.excel_name)
	label_excel_name.grid(row = 0, column = 0)
	
	print('excel name reloaded')
	entry_1 = ttk.Entry(info_frame)
	entry_1.insert(0, num_of_groups)
	entry_1.config(state = 'readonly')
	entry_1.grid(row = 0, column = 1, padx = width_1, pady = height_1)

	entry_2 = ttk.Entry(info_frame)
	entry_2.insert(0, num_of_variables)
	entry_2.config(state = 'readonly')
	entry_2.grid(row = 1, column = 1, padx = width_1, pady = height_1)

	entry_3 = ttk.Entry(info_frame)
	entry_3.insert(0, num_of_profiles)
	entry_3.config(state = 'readonly')
	entry_3.grid(row = 2, column = 1, padx = width_1, pady = height_1)

	entry_4 = ttk.Entry(info_frame)
	entry_4.insert(0, name_of_variables)
	entry_4.config(state = 'readonly')
	entry_4.grid(row = 3, column = 1, padx = width_1, pady = height_1)
	print('entries reloaded')
########################################################################

main_dir = os.getcwd()
package_dir = main_dir + '\\package'
theme_dir = package_dir + '\\theme'
input_dir = main_dir + '\\1_INPUT_HERE'



# input box info

input_box = Input_box(input_dir)
excel_name = input_box.excel_name
num_of_groups = input_box.num_of_groups
num_of_variables = input_box.num_of_variables
num_of_profiles = input_box.num_of_profiles
name_of_variables = input_box.name_of_variables

# tk 객체 인스턴스 생성
root = tk.Tk()
root.title("ANOVA(scikit-learn module)_GUI.ver")
root.option_add("*tearOff", False)
root.iconbitmap(package_dir + '\\icon.ico')
root.resizable(0, 0)
#root.geometry('600x500')

# Create a style
style = ttk.Style(root)

# Import the tcl file
os.chdir(theme_dir)
root.tk.call("source", "forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")

# Create control variables
a = tk.BooleanVar()
b = tk.BooleanVar(value=True)
c = tk.BooleanVar()
d = tk.IntVar(value=2)

f = tk.BooleanVar()
g = tk.DoubleVar(value=75.0)
h = tk.BooleanVar()


########################################################################

# set menubar
menubar = tk.Menu(root)

# menu | HELP tab
filemenu = tk.Menu(menubar)
filemenu.add_command(label="About ANOVA in scikit-learn")
filemenu.add_command(label="HOW TO USE")
filemenu.add_command(label="Exit")
menubar.add_cascade(label="HELP", menu=filemenu)

# menu | LICENSE tab
filemenu2 = tk.Menu(menubar)
filemenu2.add_command(label = "url | Korea.UNIV")
menubar.add_cascade(label = "LICENSE", menu = filemenu2)

root.config(menu=menubar)

########################################################################


# set Frames
excel_name_frame = ttk.LabelFrame(root, text = '< excel >', padding = (20, 10))
info_frame = ttk.LabelFrame(root, text = '< INFO >', padding = (20, 10))
separator = ttk.Separator(root)
button_frame = ttk.LabelFrame(root, text = '< REFRESH & RUN >', padding = (20, 10))
plot_frame = ttk.LabelFrame(root, text = '< PLOT >', padding = (20, 10))

# set Frame grid
excel_name_frame.grid(row = 0, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
info_frame.grid(row = 1, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
separator.grid(row = 2, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
button_frame.grid(row = 3, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
plot_frame.grid(row = 0, column = 1, padx = (20, 20), pady = 10, sticky = 'nsew', rowspan = 4)

########################################################################


# excel_name_frame
label_excel_name = ttk.Label(excel_name_frame, text = input_box.excel_name)
label_excel_name.grid(row = 0, column = 0)


# info_frame

width_1 = 30
height_1 = 10


# info_frame | set labels and entries

#labels
label_1 = ttk.Label(info_frame, text = '# of groups')
label_1.grid(row = 0, column = 0, padx = width_1, pady = height_1)

label_2 = ttk.Label(info_frame, text = '# of variables')
label_2.grid(row = 1, column = 0, padx = width_1, pady = height_1)

label_3 = ttk.Label(info_frame, text = '# of profiles')
label_3.grid(row = 2, column = 0, padx = width_1, pady = height_1)

label_4 = ttk.Label(info_frame, text = 'name of variables')
label_4.grid(row = 3, column = 0, padx = width_1, pady = height_1)

# entries
entry_1 = ttk.Entry(info_frame)
entry_1.insert(0, num_of_groups)
entry_1.config(state = 'readonly')
entry_1.grid(row = 0, column = 1, padx = width_1, pady = height_1)

entry_2 = ttk.Entry(info_frame)
entry_2.insert(0, num_of_variables)
entry_2.config(state = 'readonly')
entry_2.grid(row = 1, column = 1, padx = width_1, pady = height_1)

entry_3 = ttk.Entry(info_frame)
entry_3.insert(0, num_of_profiles)
entry_3.config(state = 'readonly')
entry_3.grid(row = 2, column = 1, padx = width_1, pady = height_1)

entry_4 = ttk.Entry(info_frame)
entry_4.insert(0, name_of_variables)
entry_4.config(state = 'readonly')
entry_4.grid(row = 3, column = 1, padx = width_1, pady = height_1)

# separator_frame

# button_frame
width_2 = 20
height_2 = 10

button_1 = ttk.Button(button_frame, text = "Reload Excel", \
	command = lambda : refresh(input_dir, width_1, height_1, excel_name_frame, info_frame, input_box, label_excel_name, entry_1, entry_2, entry_3, entry_4))
button_1.grid(row = 0, column = 0, padx = width_2, pady = height_2)

button_2 = ttk.Button(button_frame, text = "RUN part", style="Accent.TButton")
button_2.grid(row = 0, column = 1, padx = width_2, pady = height_2)

button_3 = ttk.Button(button_frame, text = "RUN ALL", style="Accent.TButton")
button_3.grid(row = 0, column = 2, padx = width_2, pady = height_2)


# plot_frame

# get from DataFrame
df = input_box.df
fig = plt.figure(figsize = (5, 4))     #figure(도표) 생성
ax = fig.add_subplot(1, 1, 1)

xvalues = []
for i in range(int(num_of_variables)) :
	xvalues.append(i)
xvalues_name = df.columns.tolist()[1 :]

for group in df.loc[:, 'group'].unique() :
	temp = df[df['group'] == group]
	temp.reset_index(drop = True, inplace = True)
	color = np.random.rand(3,)
	for profile in range(temp.shape[0]) :
		startpoint = xvalues_name[1]
		ax.plot(xvalues, temp.iloc[profile, 1 : ])
		
ax.set_xlim([xvalues[0], xvalues[-1]])		
ax.set_xticks(xvalues)
ax.set_xticklabels(xvalues_name, rotation = 90)

# plot to canvas
canvas = FigureCanvasTkAgg(fig, master = plot_frame)
canvas.get_tk_widget().grid(column = 0, row = 1)


# status bar

status_bar = StatusBar(root)
status_bar.variable.set('refreshing...')
# mainloop

root.mainloop()


