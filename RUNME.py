import tkinter as tk
from tkinter import ttk, Tk, font
import webbrowser

import os
import sys
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgunbd.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

from scipy import stats
from statsmodels.multivariate.manova import MANOVA

########################################################################

def split_string(string1, string2) :
	string2 = string2.replace("\n", "")
	
	if len(string2) > 100 :
		string2 = string2[ : 36] + ' ...' + string2[-40 :]
	else :
		pass
		
	result_string = ""

	lefthand = 20
	righthand = 20
	
	left_over = lefthand - len(string1)
	result_string += " " * left_over
	result_string += string1 + "   :   "

	if len(string2) > righthand :
		num = 0
		
		row = len(string2) // righthand
		if row == 1 :
			result_string += string2[0 : 20]
			result_string += '\n'
			result_string += ' ' * (lefthand + 11)
			result_string += string2[20 : ]
			
			
		else :
			for i in range(row) :
				if i == 0 :
					result_string += string2[num : num + righthand]
					result_string += "\n"
					num += righthand
				
				elif (i == (row - 1)) :
					result_string += " " * (lefthand + 11)
					result_string += string2[num : ]
					result_string += "\n"
					num += righthand
				
				else :
					result_string += " " * (lefthand + 11)
					result_string += string2[num : num + righthand]
					result_string += "\n"
					num += righthand
				print(i, '\n', result_string, '\n')
	else :
		result_string += string2
		
	return result_string
	
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

def read_excel(excel) :
	df = pd.read_excel(excel)
	if 'Unnamed: 0' in df.columns :
		df.drop('Unnamed: 0', axis = 1, inplace = True)

	if 'Unnamed: 0.1' in df.columns :
		df.drop('Unnamed: 0.1', axis = 1, inplace = True)

	return df


########### input box ###########
def remove(path):
    # """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file

    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
        
    else:
        raise ValueError("file {} is not a file or dir.".format(path))
        
def switch_sample(package_dir, num) :
	
	# 0 : no sample
	# 1 : sample(ANOVA)
	# 2 : sample(MANOVA)
	# 3 : sample(time-series)
	
	remove(package_dir + '\\check.txt')
	os.chdir(package_dir)
	
	f = open(package_dir + '\\check.txt', 'w')
	f.write('{}'.format(num))
	f.close()
	
class Input_box() :
	def __init__(self, main_dir) :
		package_dir = main_dir + '\\package'
		self.package_dir = package_dir
		self.theme_dir = package_dir + '\\theme'
		input_dir = main_dir + '\\1_INPUT_HERE'
		self.input_dir = input_dir
		self.result_dir = main_dir + '\\2_RESULT'
		
		os.chdir(package_dir)
		f = open("check.txt", 'r')
		l = f.readline()
		print(list(l))
		l = l.replace(" ", "")
		l = l.replace("\n", "")
		l = int(l)
		f.close()
		
		if l == 0 :
			if len(os.listdir(input_dir)) == 0 :
				self.sample('sample(anova).xlsx')
			else :
				self.reload(main_dir)
		elif l == 1 :
			self.sample('sample(anova).xlsx')
		elif l == 2 :
			self.sample('sample(manova).xlsx')
		elif l == 3 :
			self.sample('sample(manova_time_series).xlsx')
			
	
	def reload(self, main_dir) :
		package_dir = main_dir + '\\package'
		self.package_dir = package_dir
		self.theme_dir = package_dir + '\\theme'
		input_dir = main_dir + '\\1_INPUT_HERE'
		self.input_dir = input_dir
		self.result_dir = main_dir + '\\2_RESULT'
		
		check = 'ready'
		
		if (len(os.listdir(input_dir)) >= 2) | (len(os.listdir(input_dir)) == 0) :
			check = "place only one excel file in '1_INPUT_HERE' folder"
			
			
		else :
			os.chdir(input_dir)
			df = read_excel(os.listdir(input_dir)[0])
					
			# simple adjustments to dataframe
			dc =[]
			for c in df.columns :
				if 'drop_' in c :
					dc.append(c)
					
			df = df.drop(dc, axis = 1)
			df.dropna(axis = 0, inplace = True)
			df.reset_index(drop = True, inplace = True)
			
			column_order_1 = []
			column_order_2 = []
			for c in df.columns :
				if 'group' == c :
					column_order_1.append(c)
				else :
					column_order_2.append(c)
			column_order = column_order_1 + column_order_2
			df = df[column_order]
			self.df = df
			
			
			
			# make string for MANOVA
			self.string = 'None'
			
			if len(column_order_2) > 1 :
				string = '{}'.format(column_order_2[0])
				for i in range(1, len(column_order_2)) :
					string += '+ {}'.format(column_order[i])
					
				string += ' ~ group'
				self.string = string
			
			
			
			# set self.variables
			
			self.excel_name = os.listdir(input_dir)[0]
			self.num_of_groups = len(df.loc[:, 'group'].unique())
			self.num_of_variables = len(df.columns) - 1
			self.num_of_profiles = df.shape[0]
			
			if self.num_of_variables >= 2 :
				self.MA = 'MANOVA'
			elif self.num_of_variables == 1 :
				self.MA = 'ANOVA'
			
			self.num_of_groups = str(self.num_of_groups)
			self.num_of_variables = str(self.num_of_variables)
			self.num_of_profiles = str(self.num_of_profiles)
			self.columns = df.columns

			
			if len(df.columns) > 6 :
				self.name_of_variables = str(df.columns.tolist()[1 : 4])[ : -1] + ' ... ' + str(df.columns.tolist()[ -3 :])[1 :]
			else :
				self.name_of_variables = str(df.columns.tolist()[1 : ])

	def sample(self, sample_name) :
		package_dir = self.package_dir
		input_dir = self.input_dir
		
		cwd = package_dir + '\\sample'
		os.chdir(cwd)
		
		check = 0
		
		if check == 0 :
			
			df = read_excel(sample_name)
					
			# simple adjustments to dataframe
			dc =[]
			for c in df.columns :
				if 'drop_' in c :
					dc.append(c)
					
			df = df.drop(dc, axis = 1)
			df.dropna(axis = 0, inplace = True)
			df.reset_index(drop = True, inplace = True)
			
			column_order_1 = []
			column_order_2 = []
			for c in df.columns :
				if 'group' == c :
					column_order_1.append(c)
				else :
					column_order_2.append(c)
			column_order = column_order_1 + column_order_2
			df = df[column_order]
			self.df = df
			
			
			
			# make string for MANOVA
			self.string = 'None'
			
			if len(column_order_2) > 1 :
				string = '{}'.format(column_order_2[0])
				for i in range(1, len(column_order_2)) :
					string += '+ {}'.format(column_order[i])
					
				string += ' ~ group'
				self.string = string
			
			
			
			# set self.variables
			
			self.excel_name = sample_name
			self.num_of_groups = len(df.loc[:, 'group'].unique())
			self.num_of_variables = len(df.columns) - 1
			self.num_of_profiles = df.shape[0]
			
			if self.num_of_variables >= 2 :
				self.MA = 'MANOVA'
			elif self.num_of_variables == 1 :
				self.MA = 'ANOVA'
			
			self.num_of_groups = str(self.num_of_groups)
			self.num_of_variables = str(self.num_of_variables)
			self.num_of_profiles = str(self.num_of_profiles)
			self.columns = df.columns

			
			if len(df.columns) > 6 :
				self.name_of_variables = str(df.columns.tolist()[1 : 4])[ : -1] + ' ... ' + str(df.columns.tolist()[ -3 :])[1 :]
			else :
				self.name_of_variables = str(df.columns.tolist()[1 : ])
		
		package_dir = main_dir + '\\package'
		switch_sample(package_dir, 0)
				
			
	def ANOVA(self, title) :
		smpl = self.df
		unique_list = smpl.loc[:, 'group'].unique()
		result_dir = self.result_dir
		group_list = []
		for t in unique_list :
			group_list.append(t)

		anova_table = pd.DataFrame(columns = group_list, index = group_list)

		for t in group_list :
			for j in group_list :
				if t == j :
					anova_table.loc[t, j] = 0
				else :
					temp1 = smpl[smpl['group'] == t].loc[:, 'var'].tolist()
					temp2 = smpl[smpl['group'] == j].loc[:, 'var'].tolist()

					temp1 = [x for x in temp1 if str(x) != 'nan']
					temp2 = [x for x in temp2 if str(x) != 'nan']

					f_val, p_val = stats.f_oneway(temp1, temp2)
					anova_table.loc[t, j] = p_val
				print('{}, {} done'.format(t, j), end = '\r')
				
		os.chdir(result_dir)
		anova_table.to_excel('{}.xlsx'.format(title))
		print('{}.xlsx saved'.format(title))
		
		
		
	def MANOVA(self, title) :
		smpl = self.df
		unique_list = smpl.loc[:, 'group'].unique()
		result_dir = self.result_dir
		string = self.string
		group_list = []
		for t in unique_list :
			group_list.append(t)

		manova_table = pd.DataFrame(columns = group_list, index = group_list)
		for t in unique_list :
			for j in unique_list :
				if t == j :
					manova_table.loc[t, j] = 0
				else :
					dropindex = []
					temp = smpl.copy()
					for i in range(temp.shape[0]) :
						if (temp.loc[i, 'group'] != t) & (temp.loc[i, 'group'] != j) :
							dropindex.append(i)
					
					temp.drop(dropindex, inplace = True)
					temp.reset_index(drop = True, inplace = True)
					m_all = MANOVA.from_formula(string, data = temp)
					manova_table.loc[t, j] = \
					round(pd.DataFrame(m_all.mv_test().results['group']['stat']).loc['Hotelling-Lawley trace', 'Pr > F'], 4)
					
		os.chdir(result_dir)
		manova_table.to_excel('{}.xlsx'.format(title))
		print('{}.xlsx saved'.format(title))
		
		
		
		
	def MANOVA_specific(self, title) :
		
		all_result = '\n\n# compare groups with MANOVA, statsmodel \n\n'
		
		smpl = self.df
		unique_list = smpl.loc[:, 'group'].unique()
		result_dir = self.result_dir
		string = self.string
		group_list = []
		for t in unique_list :
			group_list.append(t)

		manova_table = pd.DataFrame(columns = group_list, index = group_list)
		for t in unique_list :
			for j in unique_list :
				if t == j :
					pass
				else :
					dropindex = []
					temp = smpl.copy()
					for i in range(temp.shape[0]) :
						if (temp.loc[i, 'group'] != t) & (temp.loc[i, 'group'] != j) :
							dropindex.append(i)
					
					temp.drop(dropindex, inplace = True)
					temp.reset_index(drop = True, inplace = True)
					m_all = MANOVA.from_formula(string, data = temp)
					
					length = 63
					all_result += '#' * length
					all_result += '\n'
					all_result += '< {} & {} | {} >'.format(t, j, input_box.MA)
					
					test_str = str(m_all.mv_test())
					test_str = test_str.replace("===============================================================",\
					 "---------------------------------------------------------------")
					test_str = test_str.replace("Multivariate linear model", "")
					all_result += test_str
					all_result += '\n'
					
		os.chdir(result_dir)
		f = open("{}.txt".format(title), 'w')
		temp = f.write(all_result)
		f.close()
		print('{}.txt saved'.format(title))
		
		

########### restart GUI ###########
		
def refresh2(main_dir) :
	os.chdir(main_dir)
	os.execl(sys.executable, sys.executable, *sys.argv)

############ ANOVA | MANOVA button ###############

def switcher(input_box, title) :
	if input_box.MA == 'ANOVA' :
		input_box.ANOVA(title)
	elif input_box.MA == 'MANOVA' :
		input_box.MANOVA(title)
		
def window1_button1_cmd(input_box, get_text) : # table result for both ANOVA / MANOVA
	title = get_text.get("1.0","end")
	title = title.replace("\n", "")	
	if len(title) == 0 :
		title = 'result'
		
	switcher(input_box, title)
	print('saved as {}.xlsx'.format(title))
	window_ok()
	
def window1_button2_cmd(input_box, get_text) : # specific result (only for MANOVA)
	title = get_text.get("1.0","end")
	title = title.replace("\n", "")	
	if len(title) == 0 :
		title = 'result'
		
	input_box.MANOVA_specific(title)
	print('saved as {}.xlsx'.format(title))
	window_ok()

def window2_button1_cmd(input_box, get_text, get_text_group) : # table result for both ANOVA / MANOVA
	title = get_text.get("1.0","end")
	title = title.replace("\n", "")	
	
	# adjust self.df of input_box
	new_group = get_text_group.get("1.0","end")
	new_group = new_group.replace("\n", "")
	new_group = eval(new_group)
	
	df = input_box.df
	original_df = df.copy()

	dropindex = []
	for i in range(df.shape[0]) :
		if df.loc[i, 'group'] not in new_group :
			dropindex.append(i)
	df.drop(dropindex, inplace = True)
	df.reset_index(drop = True, inplace = True)
	
	input_box.df = df
	
	switcher(input_box, title)
	input_box.df = original_df
	original_df =  None
	print('saved as {}.xlsx'.format(title))
	window_ok()
	
def window2_button2_cmd(input_box, get_text, get_text_group) : # specific result (only for MANOVA)
	title = get_text.get("1.0","end")
	title = title.replace("\n", "")	
	
	# adjust self.df of input_box
	new_group = get_text_group.get("1.0","end")
	new_group = new_group.replace("\n", "")
	new_group = eval(new_group)
	
	df = input_box.df
	original_df = df.copy()

	dropindex = []
	for i in range(df.shape[0]) :
		if df.loc[i, 'group'] not in new_group :
			dropindex.append(i)
	df.drop(dropindex, inplace = True)
	df.reset_index(drop = True, inplace = True)
	
	input_box.df = df
	
	# MANOVA
	
	input_box.MANOVA_specific(title)
	
	input_box.df = original_df
	original_df =  None
	print('saved as {}.xlsx'.format(title))
	window_ok()
	
############ popup menu ###############

def window_ok() : # show ' done ! ' message when .xlsx is made
	window_pop = tk.Toplevel(root)
	window_pop.title("message")
	
	window_pop.option_add("*tearOff", False)
	window_pop.iconbitmap(package_dir + '\\icon.ico')
	window_pop.geometry("150x30")
	window_pop.resizable(0, 0)

	window_pop_label = ttk.Label(window_pop, text = 'DONE !')
	window_pop_label.place(relx=0.5, rely=0.5, anchor = 'center')
	window_pop.mainloop()

def window_message(string) : # show ' done ! ' message when .xlsx is made
	window_pop = tk.Toplevel(root)
	window_pop.title("message")
	
	window_pop.option_add("*tearOff", False)
	window_pop.iconbitmap(package_dir + '\\icon.ico')
	window_pop.geometry("150x30")
	window_pop.resizable(0, 0)

	window_pop_label = ttk.Label(window_pop, text = string)
	window_pop_label.place(relx=0.5, rely=0.5, anchor = 'center')
	window_pop.mainloop()

############ window_1 (RUN ALL) ###############
	
def run_all_window(input_box) : # window when you press 'RUN ALL'
	df = input_box.df
	window_1 = tk.Toplevel(root)
	window_1.title("RUN ALL groups with {}".format(str(input_box.MA)))
	
	window_1.option_add("*tearOff", False)
	window_1.iconbitmap(package_dir + '\\icon.ico')
	window_1.resizable(0, 0)
	
	# set Frame
	window1_status_frame = ttk.LabelFrame(window_1, text = '< INFO >', padding = (20, 10))
	window1_separator = ttk.Separator(window_1)
	window1_button_frame = ttk.LabelFrame(window_1, text = '< RESULT >', padding = (20, 10))
	
	
	# set Frame grid
	window1_status_frame.grid(row = 0, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	window1_separator.grid(row = 1, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	window1_button_frame.grid(row = 2, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	
	
	# window1_status_frame
	window1_width = 30
	window1_height = 10
	unique_list = df.loc[:, 'group'].unique() 
	status_text = ''
	
	string1_1 = 'method'
	string1_2 = '{}'.format(input_box.MA)
	
	string2_1 = '# of groups'
	string2_2 = str(len(unique_list))
	
	string3_1 = 'groups'
	string3_2 = '{}'.format(unique_list)
	
	#print(split_string(string3_1, string3_2), '\n\n')
	status_text += split_string(string1_1, string1_2)
	status_text += '\n'
	status_text += split_string(string2_1, string2_2)
	status_text += '\n'
	status_text += split_string(string3_1, string3_2)
	
	status_label_1 = ttk.Label(window1_status_frame, text = status_text)
	status_label_1.grid(row = 0, column = 0, padx = window1_width, pady = window1_height)
	

	# window1_button_frame
	window1_b_width = 8
	window1_b_height = 10
	
	get_label = ttk.Label(window1_button_frame, text = '     save excel as    :', width = 20)
	get_label.grid(row = 0, column = 0, padx = window1_b_width, pady = window1_b_height)
	get_text = tk.Text(window1_button_frame, height = 1.2, width = 30)
	get_text.grid(row = 0, column = 1, padx = window1_b_width, pady = window1_b_height)
	
	window1_button1 = ttk.Button(window1_button_frame, text = "result table",  style="Accent.TButton",\
	command = lambda : window1_button1_cmd(input_box, get_text), width = 20)
	window1_button1.grid(row = 1, column = 0, padx = window1_b_width, pady = window1_b_height)
	
	if input_box.MA == 'ANOVA' :
		window1_button2 = ttk.Button(window1_button_frame, text = "specific result", command = lambda : window1_button2_cmd(input_box, get_text),\
		width = 20)
		window1_button2.grid(row = 1, column = 1, padx = window1_b_width, pady = window1_b_height)
		
		window1_button2["state"] = "disabled"
		
	elif input_box.MA == 'MANOVA' :
		window1_button2 = ttk.Button(window1_button_frame, text = "specific result", style="Accent.TButton",\
		command = lambda : window1_button2_cmd(input_box, get_text), width = 20)
		window1_button2.grid(row = 1, column = 1, padx = window1_b_width, pady = window1_b_height)
		
		window1_button2["state"] = "normal"
	

	
	window_1.mainloop()

############ window_2 (RUN part) ###############


def run_part_window(input_box) :
	df = input_box.df
	window_1 = tk.Toplevel(root)
	window_1.title("RUN part groups with {}".format(str(input_box.MA)))
	
	window_1.option_add("*tearOff", False)
	window_1.iconbitmap(package_dir + '\\icon.ico')
	window_1.resizable(0, 0)
	
	# set Frame
	window1_status_frame = ttk.LabelFrame(window_1, text = '< INFO >', padding = (20, 10))
	window1_separator = ttk.Separator(window_1)
	window1_group = ttk.LabelFrame(window_1, text = '< GROUP >', padding = (20, 10))
	window1_button_frame = ttk.LabelFrame(window_1, text = '< RESULT >', padding = (20, 10))
	
	
	# set Frame grid
	window1_status_frame.grid(row = 0, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	window1_separator.grid(row = 1, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	window1_group.grid(row = 2, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	window1_button_frame.grid(row = 3, column = 0, padx = (20, 20), pady = 10, sticky = 'nsew')
	
	
	# window1_status_frame
	window1_width = 30
	window1_height = 10
	unique_list = df.loc[:, 'group'].unique() 
	status_text = ''
	
	string1_1 = 'method'
	string1_2 = '{}'.format(input_box.MA)
	
	string2_1 = '# of groups'
	string2_2 = str(len(unique_list))
	
	string3_1 = 'groups'
	string3_2 = '{}'.format(unique_list)
	
	#print(split_string(string3_1, string3_2), '\n\n')
	status_text += split_string(string1_1, string1_2)
	status_text += '\n'
	status_text += split_string(string2_1, string2_2)
	status_text += '\n'
	status_text += split_string(string3_1, string3_2)
	
	status_label_1 = ttk.Label(window1_status_frame, text = status_text)
	status_label_1.grid(row = 0, column = 0, padx = window1_width, pady = window1_height)
	
	# window1_group_frame
	window1_g_width = 8
	window1_g_height = 10
	
	get_label_group = ttk.Label(window1_group, text = '     choose groups    :', width = 20)
	get_label_group.grid(row = 0, column = 0, padx = window1_g_width, pady = window1_g_height)
	get_text_group = tk.Text(window1_group, height = 1.2, width = 30)
	get_text_group.grid(row = 0, column = 1, padx = window1_g_width, pady = window1_g_height)
	

	# window1_button_frame
	window1_b_width = 8
	window1_b_height = 10
	
	get_label = ttk.Label(window1_button_frame, text = '     save excel as    :', width = 20)
	get_label.grid(row = 0, column = 0, padx = window1_b_width, pady = window1_b_height)
	get_text = tk.Text(window1_button_frame, height = 1.2, width = 30)
	get_text.grid(row = 0, column = 1, padx = window1_b_width, pady = window1_b_height)
	
	window1_button1 = ttk.Button(window1_button_frame, text = "result table",  style="Accent.TButton",\
	command = lambda : window2_button1_cmd(input_box, get_text, get_text_group), width = 20)
	window1_button1.grid(row = 1, column = 0, padx = window1_b_width, pady = window1_b_height)
	
	if input_box.MA == 'ANOVA' :
		window1_button2 = ttk.Button(window1_button_frame, text = "specific result", command = lambda : window2_button2_cmd(input_box, get_text, get_text_group),\
		width = 20)
		window1_button2.grid(row = 1, column = 1, padx = window1_b_width, pady = window1_b_height)
		
		window1_button2["state"] = "disabled"
		
	elif input_box.MA == 'MANOVA' :
		window1_button2 = ttk.Button(window1_button_frame, text = "specific result", style="Accent.TButton",\
		command = lambda : window2_button2_cmd(input_box, get_text, get_text_group), width = 20)
		window1_button2.grid(row = 1, column = 1, padx = window1_b_width, pady = window1_b_height)
		
		window1_button2["state"] = "normal"
	

	
	window_1.mainloop()
	
def menubar_url(url) :
	  webbrowser.open(url)
  
def menubar_sample_anova(main_dir) :
	package_dir = main_dir + '\\package'
	switch_sample(package_dir, 1)
	os.chdir(main_dir)
	os.execl(sys.executable, sys.executable, *sys.argv)
	
	
def menubar_sample_manova(main_dir) :
	package_dir = main_dir + '\\package'
	switch_sample(package_dir, 2)
	os.chdir(main_dir)
	os.execl(sys.executable, sys.executable, *sys.argv)
	
	
def menubar_sample_time_series(main_dir) :
	package_dir = main_dir + '\\package'
	switch_sample(package_dir, 3)
	os.chdir(main_dir)
	os.execl(sys.executable, sys.executable, *sys.argv)
	
	
########################################################################
############################< MAIN >####################################
########################################################################


main_dir = os.getcwd()

# input box info
print('< status > \nloading DataFrame')
input_box = Input_box(main_dir)

package_dir = input_box.package_dir
theme_dir = input_box.theme_dir
input_dir = input_box.input_dir
result_dir = input_box.result_dir


excel_name = input_box.excel_name
num_of_groups = input_box.num_of_groups
num_of_variables = input_box.num_of_variables
num_of_profiles = input_box.num_of_profiles
name_of_variables = input_box.name_of_variables

MA = input_box.MA

########################################################################

# tk 객체 인스턴스 생성
root = tk.Tk()
root.title("ANOVA | MANOVA")
root.option_add("*tearOff", False)
root.iconbitmap(package_dir + '\\icon.ico')
root.resizable(0, 0)
#root.geometry('600x500')

# Create a style
style = ttk.Style(root)

#default_font = TkFont.nametofont("TkDefaultFont")
#default_font.configure(family = {"Courier New"})
#root.option_add("*Font", default_font)


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

print('DataFrame loaded')

########################################################################

# set menubar
menubar = tk.Menu(root)

# menu | HELP tab
filemenu = tk.Menu(menubar)
filemenu.add_command(label="About ANOVA in scipy",\
	command = lambda : menubar_url('https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html'))
	
filemenu.add_command(label="About MANOVA in statsmodels",\
	command = lambda : menubar_url('https://www.statsmodels.org/dev/generated/statsmodels.multivariate.manova.MANOVA.html'))
	
filemenu.add_command(label="HOW TO USE",\
	command = lambda : menubar_url('https://github.com/suhyuuk/ANOVA_GUI'))
filemenu.add_command(label="Exit", command = root.destroy)

menubar.add_cascade(label="HELP", menu=filemenu)

# menu | LICENSE tab
filemenu2 = tk.Menu(menubar)
filemenu2.add_command(label = "Theme | Forest-ttk-theme by rdbende (MIT license)",\
	command = lambda : menubar_url('https://github.com/rdbende/Forest-ttk-theme'))
	
filemenu2.add_command(label = "GitHub",\
	command = lambda : menubar_url('https://github.com/suhyuuk/ANOVA_GUI'))
	
filemenu2.add_command(label = "Korea.UNIV | Urban Energy and Environment", \
	command = lambda : menubar_url('http://urbane-squared.korea.ac.kr/'))
menubar.add_cascade(label = "LICENSE", menu = filemenu2)

# menu | sample tab
filemenu3 = tk.Menu(menubar)

filemenu3.add_command(label = "ANOVA sample", \
	command = lambda : menubar_sample_anova(main_dir))
	
filemenu3.add_command(label = "MANOVA sample (default)", \
	command = lambda : menubar_sample_manova(main_dir))
	
filemenu3.add_command(label = "MANOVA sample (time-series)", \
	command = lambda : menubar_sample_time_series(main_dir))

menubar.add_cascade(label = "SAMPLE", menu = filemenu3)

root.config(menu=menubar)

########################################################################


# set Frames
excel_name_frame = ttk.LabelFrame(root, text = '< EXCEL >', padding = (20, 10))
info_frame = ttk.LabelFrame(root, text = '< INFO >', padding = (20, 10))
separator = ttk.Separator(root)
button_frame = ttk.LabelFrame(root, text = '< REFRESH & RUN >', padding = (20, 10))
plot_frame = ttk.LabelFrame(root, text = '< VISUALIZATION >', padding = (20, 10))

# set Frame grid
excel_name_frame.grid(row = 0, column = 1, padx = (20, 20), pady = 10, sticky = 'nsew')
info_frame.grid(row = 1, column = 1, padx = (20, 20), pady = 10, sticky = 'nsew')
separator.grid(row = 2, column = 1, padx = (20, 20), pady = 10, sticky = 'nsew')
button_frame.grid(row = 3, column = 1, padx = (20, 20), pady = 10, sticky = 'nsew')
plot_frame.grid(row = 0, column = 0, padx = (20, 20), pady = 8, sticky = 'nsew', rowspan = 4)

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
entry_2.insert(0, '{} ({})'.format(num_of_variables, MA))
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


########################################################################
# separator_frame


########################################################################
# button_frame
width_2 = 20
height_2 = 10

button_1 = ttk.Button(button_frame, text = "Reload Excel", \
	command = lambda : refresh2(main_dir))
#	command = lambda : refresh(input_dir, width_1, height_1, excel_name_frame, info_frame, input_box, label_excel_name, entry_1, entry_2, entry_3, entry_4))
button_1.grid(row = 0, column = 0, padx = width_2, pady = height_2)

button_2 = ttk.Button(button_frame, text = "RUN part", style="Accent.TButton", \
	command = lambda : run_part_window(input_box))
button_2.grid(row = 0, column = 1, padx = width_2, pady = height_2)

button_3 = ttk.Button(button_frame, text = "RUN ALL", style="Accent.TButton", \
	command = lambda : run_all_window(input_box))
button_3.grid(row = 0, column = 2, padx = width_2, pady = height_2)


########################################################################
# plot_frame

# get from DataFrame
df = input_box.df


plt.rcParams.update({'font.size': 9})

if len(df.columns) > 2 :
	
	xvalues = []
	for i in range(int(num_of_variables)) :
		xvalues.append(i)
	xvalues_name = df.columns.tolist()[1 :]
	cmap = matplotlib.cm.get_cmap('summer')
	
	if len(xvalues) < 5 :
		fig_width = len(xvalues)
	elif (len(xvalues) >= 5) & (len(xvalues) < 10) :
		fig_width = len(xvalues) * 0.5
	elif (len(xvalues) >= 10) & (len(xvalues) < 15) :
		fig_width = len(xvalues) * 0.35
	elif (len(xvalues) >= 15) & (len(xvalues) < 30) :
		fig_width = len(xvalues) * 0.2
	elif (len(xvalues) >= 30) :
		fig_width = len(xvalues) * 0.18
	
	fig = plt.figure(figsize = (fig_width, 4))	 #figure(도표) 생성
	ax = fig.add_subplot(1, 1, 1)
	
	for group in df.loc[:, 'group'].unique() :
		temp = df[df['group'] == group]
		temp.reset_index(drop = True, inplace = True)
		color_ylgn = cmap(0.5 * np.random.rand())
		for profile in range(temp.shape[0]) :
			startpoint = xvalues_name[1]
			ax.plot(xvalues, temp.iloc[profile, 1 : ], c = color_ylgn)
			
	ax.set_xlim([xvalues[0], xvalues[-1]])		
	ax.set_xticks(xvalues)
	ax.set_xticklabels(xvalues_name, rotation = 90)
	plt.xlabel('variables', fontsize = 10)
	plt.ylabel('values', fontsize = 10)
	plt.tight_layout()
	
else :
	
	fig = plt.figure(figsize = (5, 4))
	ax = fig.add_subplot(1, 1, 1)
	
	unique_group = df.loc[:, 'group'].unique()
	xvalues = []
	for i in range(len(unique_group)) :
		xvalues.append(i)
	
	
	for i, group in enumerate(unique_group):
		temp = df[df['group'] == group]
		temp_list = temp.loc[:, 'var'].tolist()
		temp_list = list(map(float, temp_list))
		ax.boxplot(temp_list, positions = [i])
		
	ax.set_xticks(xvalues)
	ax.set_xticklabels(unique_group, rotation = 90)
	plt.xlabel('groups')
	plt.ylabel('values')
	plt.tight_layout()
		
	
# plot to canvas
canvas = FigureCanvasTkAgg(fig, master = plot_frame)
canvas.get_tk_widget().grid(column = 0, row = 1)

########################################################################


# status bar

#status_bar = StatusBar(root)
#status_bar.variable.set('refreshing...')
# mainloop

root.mainloop()
mainloop()

