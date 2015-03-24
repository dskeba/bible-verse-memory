
__version__ = '1.0.0'

import kivy
kivy.require('1.7.2')

from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'multisamples', '2')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.core.window import Window

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.graphics.instructions import Canvas, Instruction
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.relativelayout import RelativeLayout
from  kivy.uix.popup import Popup

import time
import json
import urllib2
from random import randint

class BibleVerse():
	def __init__(self, title, text):
		self.title = title
		self.text = text
		self.orig_text = text
		self.memorize = False
		self.words_removed = []
		
	def get_display_text(self, word_wrap = 5):
		display_text = ''
		i = 1
		first_word = True
		for word in self.text.split():
			if not first_word:
				display_text = display_text + " "
			else:
				first_word = False
			display_text = display_text + word
			if i >= word_wrap:
				display_text = display_text + '\n'
				i = 1
			else:
				i = i + 1
		return display_text
		
	def remove_word(self):
		words = self.text.split()
		total_words = len(words)
		if len(self.words_removed) >= total_words:
			return
		num = randint(0, (total_words-1))
		while num in self.words_removed:
			num = randint(0, (total_words-1))
		self.words_removed.append(num)
		total_letters = len(words[num])
		words[num] = ''
		for i in range(0, total_letters):
			words[num] = words[num] + "_"
		self.text = ''
		for i in range(0, total_words):
			if i > 0:
				self.text = self.text + " "
			self.text = self.text + words[i]
			
	def add_word(self):
		if len(self.words_removed) == 0:
			return
		words = self.text.split()
		total_words = len(words)
		orig_words = self.orig_text.split()
		idx = self.words_removed.pop()
		words[idx] = orig_words[idx]
		self.text = ''
		for i in range(0, total_words):
			if i > 0:
				self.text = self.text + " "
			self.text = self.text + words[i]
		
class MenuWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		
	def init_child_widgets(self):
		self.menu_scroll_widget = ScrollView()
		self.menu_layout = BoxLayout(orientation = 'vertical', padding = [50, 10, 50, 10], spacing = 10)
		wimg = Image(source = 'logo.png', size_hint_y = None)
		self.menu_layout.add_widget(wimg)
		self.menu_button_memorize = Button(text = 'Memorize', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button_memorize.bind(on_press = self.on_press)
		self.menu_layout.add_widget(self.menu_button_memorize)
		print("font-size: " + str(self.app.font_size))
		self.menu_button_verses = Button(text = 'Verses', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button_verses.bind(on_press = self.on_press)
		self.menu_layout.add_widget(self.menu_button_verses)
		self.menu_button_options = Button(text = 'Options', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button_options.bind(on_press = self.on_press)
		self.menu_layout.add_widget(self.menu_button_options)
		self.menu_button_quit = Button(text = 'Quit', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button_quit.bind(on_press = self.on_press)
		self.menu_layout.add_widget(self.menu_button_quit)
		self.menu_scroll_widget.add_widget(self.menu_layout)
		self.add_widget(self.menu_scroll_widget)
		
	def on_press(self, button):
		if button.text == 'Verses':
			print("Verses")
			self.app.set_widget(KivyApp.WID_VERSES)
		elif button.text == 'Memorize':
			print("Memorize")
			self.app.set_widget(KivyApp.WID_MEMORIZE)
		elif button.text == 'Options':
			print("Options")
			self.app.set_widget(KivyApp.WID_OPTIONS)
		elif button.text == 'Quit':
			print("Quit")
			exit()

class AddVerseWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		
	def init_child_widgets(self):
		self.scroll_layout = ScrollView()
		self.root_layout = GridLayout( cols = 2, padding = [50, 10, 50, 10], spacing = 10)
		self.book_label = Label(text = 'Book', font_size = self.app.font_size)
		self.root_layout.add_widget(self.book_label)
		self.book_spinner = Spinner(text='Genesis',background_color = (1,0,1),font_size = self.app.font_size,values=('Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalm','Proverbs','Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter','1 John','2 John','3 John','Jude','Revelation'))
		self.root_layout.add_widget(self.book_spinner)
		self.chapter_label = Label(text = 'Chapter', font_size = self.app.font_size)
		self.root_layout.add_widget(self.chapter_label)
		self.chapter_spinner = Spinner(text='1',background_color = (1,0,1),font_size = self.app.font_size,values=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'))             
		self.root_layout.add_widget(self.chapter_spinner)
		self.verse_label = Label(text = 'Verse', font_size = self.app.font_size)
		self.root_layout.add_widget(self.verse_label)
		self.verse_spinner = Spinner(text='1',background_color = (1,0,1),font_size = self.app.font_size,values=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'))
		self.root_layout.add_widget(self.verse_spinner)
		self.back_button = Button(text = 'Back', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.back_button.bind(on_press = self.on_press)
		self.add_button = Button(text = 'Add', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.add_button.bind(on_press = self.on_press)
		self.root_layout.add_widget(self.back_button)
		self.root_layout.add_widget(self.add_button)
		self.scroll_layout.add_widget(self.root_layout)
		self.add_widget(self.scroll_layout)
		
	def on_press(self, button):
		if button.text == 'Back':
			print("Back")
			self.app.set_widget(KivyApp.WID_VERSES)
		elif button.text == 'Add':
			print("Add")
			self.app.add_verse(self.book_spinner.text, self.chapter_spinner.text, self.verse_spinner.text)
			self.app.set_widget(KivyApp.WID_VERSES)
			
class OptionsWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		
	def init_child_widgets(self):
		self.root_layout = GridLayout(cols = 1, padding = [50, 10, 50, 10], spacing = 10)
		self.add_button = Button(text = 'Save',background_normal = 'buttongold.jpg',font_size = self.app.font_size)
		self.root_layout.add_widget(self.add_button)
		self.menu_button = Button(text = 'Back To Menu',background_normal = 'buttongold.jpg',font_size = self.app.font_size)
		self.menu_button.bind(on_press = self.on_press)
		self.root_layout.add_widget(self.menu_button)
		self.add_widget(self.root_layout)
		
	def on_press(self, button):
		if button.text == 'Back To Menu':
			print("Back To Menu")
			self.app.set_widget(KivyApp.WID_MENU)
	
class MemorizeWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		
	def init_child_widgets(self):
		self.root_layout = GridLayout(cols = 1, pos = (0,0), padding = [50, 10, 50, 10], spacing = 10)
		self.select_label = Label(text = "Select the verses you want to memorize:", font_size = 42, size_hint_y = 0.15)
		self.root_layout.add_widget(self.select_label)
		self.scroll_widget = ScrollView()
		self.scroll_layout = GridLayout(size_hint_y = None, cols = 1, spacing = 10)
		self.button_layout = GridLayout(cols = 1, spacing = 10, pos = (0,0))
		self.scroll_widget.add_widget(self.scroll_layout)
		self.root_layout.add_widget(self.scroll_widget)
		self.start_button = Button(text = 'Start', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.start_button.bind(on_press = self.on_press)
		self.button_layout.add_widget(self.start_button)
		self.menu_button = Button(text = 'Back To Menu', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button.bind(on_press = self.on_press)
		self.button_layout.add_widget(self.menu_button)
		self.root_layout.add_widget(self.button_layout)
		self.add_widget(self.root_layout)
	
	def refresh(self):
		self.scroll_layout.clear_widgets()
		self.verse_list = []
		self.scroll_layout.height = 0
		for verse in self.app.get_verses():
			self.scroll_layout.height = self.scroll_layout.height + 110
			verse_dict = {}
			verse_dict['verse'] = verse
			verse_dict['checkbox'] = CheckBox()
			self.verse_list.append(verse_dict)
			verse_layout = GridLayout(cols = 2,spacing = 10)
			verse_layout.add_widget(verse_dict['checkbox'])
			verse_label = Label(text = verse.title, font_size = self.app.font_size)
			verse_layout.add_widget(verse_label)
			self.scroll_layout.add_widget(verse_layout)
			
	def update_verses(self):
		for verse_dict in self.verse_list:
			if verse_dict['checkbox'].active:
				verse_dict['verse'].memorize = True
			else:
				verse_dict['verse'].memorize = False
			
	def on_press(self, button):
		if button.text == 'Start':
			print("Start")
			self.update_verses()
			self.app.set_widget(KivyApp.WID_VERSE)
		elif button.text == 'Back To Menu':
			print("Back To Menu")
			self.app.set_widget(KivyApp.WID_MENU)

class VerseWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		self.current_verse = 0
		
	def init_child_widgets(self):
		self.root_layout = GridLayout(cols = 1, padding = [50, 10, 50, 10], spacing = 10)
		self.title_label = Label(text = '', font_size = self.app.font_size, size_hint_y = 0.1)
		self.root_layout.add_widget(self.title_label)
		self.verse_label = Label(text = '', font_size = self.app.font_size, size_hint_y = 0.5)
		self.root_layout.add_widget(self.verse_label)
		self.add_remove_layout = GridLayout(cols = 2, spacing = 10, size_hint_y = 0.1)
		self.remove_word_button = Button(text = 'Remove Word',background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.remove_word_button.bind(on_press = self.on_press)
		self.add_remove_layout.add_widget(self.remove_word_button)
		self.add_word_button = Button(text = 'Add Word',background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.add_word_button.bind(on_press = self.on_press)
		self.add_remove_layout.add_widget(self.add_word_button)
		self.root_layout.add_widget(self.add_remove_layout)
		self.back_next_layout = GridLayout(cols = 2, spacing = 10, size_hint_y = 0.1)
		self.menu_button = Button(text = 'Back To Menu',background_normal = 'buttongold.jpg', font_size = self.app.font_size, size_hint_y = 0.1)
		self.menu_button.bind(on_press = self.on_press)
		self.back_next_layout.add_widget(self.menu_button)
		self.next_button = Button(text = 'Next',background_normal = 'buttongold.jpg', font_size = self.app.font_size, size_hint_y = 0.1)
		self.next_button.bind(on_press = self.on_press)
		self.back_next_layout.add_widget(self.next_button)
		self.root_layout.add_widget(self.back_next_layout)
		self.add_widget(self.root_layout)
		
	def next_verse(self):
		total_verses = len(self.verse_list)
		self.current_verse += 1
		if self.current_verse == total_verses:
			self.current_verse = 0
		
	def refresh(self):
		self.verse_list = []
		for verse in self.app.get_verses():
			if verse.memorize:
				self.verse_list.append(verse)
		self.update_verse(self.verse_list[self.current_verse])
		
	def update_verse(self, bible_verse):
		self.title_label.text = bible_verse.title
		self.verse_label.text = bible_verse.get_display_text(self.app.word_wrap)
		
	def on_press(self, button):
		if button.text == 'Next':
			print("Next")
			self.next_verse()
			self.refresh()
		elif button.text == 'Remove Word':
			print("Remove Word")
			self.verse_list[self.current_verse].remove_word()
			self.refresh()
		elif button.text == 'Add Word':
			print("Add Word")
			self.verse_list[self.current_verse].add_word()
			self.refresh()
		elif button.text == 'Back To Menu':
			print("Back To Menu")
			self.app.set_widget(KivyApp.WID_MENU)
			
class VersesWidget(RelativeLayout):
	def __init__(self, app):
		RelativeLayout.__init__(self)
		self.app = app
		self.init_child_widgets()
		
	def init_child_widgets(self):
		self.root_layout = GridLayout(cols = 1, pos = (0,0), padding = [50, 10, 50, 10], spacing = 10)
		self.scroll_widget = ScrollView()
		self.scroll_layout = GridLayout(size_hint_y = None, cols = 1, spacing = 5)
		self.button_layout = GridLayout(cols = 1, spacing = 10, pos = (0,0))
		self.scroll_widget.add_widget(self.scroll_layout)
		self.root_layout.add_widget(self.scroll_widget)
		self.add_button = Button(text = 'Add', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.add_button.bind(on_press = self.on_press)
		self.button_layout.add_widget(self.add_button)
		self.remove_button = Button(text = 'Remove', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.remove_button.bind(on_press = self.on_press)
		self.button_layout.add_widget(self.remove_button)
		self.menu_button = Button(text = 'Back To Menu', background_normal = 'buttongold.jpg', font_size = self.app.font_size)
		self.menu_button.bind(on_press = self.on_press)
		self.button_layout.add_widget(self.menu_button)
		self.root_layout.add_widget(self.button_layout)
		self.add_widget(self.root_layout)
		
	def refresh(self):
		self.scroll_layout.clear_widgets()
		self.verse_list = []
		self.scroll_layout.height = 0 
		for verse in self.app.get_verses():
			self.scroll_layout.height = self.scroll_layout.height + 90
			verse_dict = {}
			verse_dict['verse'] = verse
			verse_dict['checkbox'] = CheckBox()
			self.verse_list.append(verse_dict)
			verse_layout = GridLayout(size_hint_y = None, cols = 2,spacing = 10)
			verse_layout.add_widget(verse_dict['checkbox'])
			verse_label = Label(text = verse.title, font_size = self.app.font_size)
			verse_layout.add_widget(verse_label)
			self.scroll_layout.add_widget(verse_layout)
			
	def remove_verses(self):
		verses_to_remove = []
		for verse_dict in self.verse_list:
			if verse_dict['checkbox'].active:
				verses_to_remove.append(verse_dict)
		for verse_dict in verses_to_remove:
			self.app.remove_verse(verse_dict['verse'])
		
	def on_press(self, button):
		if button.text == 'Add':
			print("Add")
			self.app.set_widget(KivyApp.WID_ADD_VERSE)
			self.refresh()
		elif button.text == 'Remove':
			print("Remove")
			self.remove_verses()
			self.refresh()
		elif button.text == 'Back To Menu':
			print("Back To Menu")
			self.app.set_widget(KivyApp.WID_MENU)
			
class KivyApp(App):
		
	WID_MENU = 0
	WID_MEMORIZE = 1
	WID_VERSES = 2
	WID_OPTIONS = 3
	WID_ADD_VERSE = 4
	WID_VERSE = 5
		
	def __init__(self):
		App.__init__(self)
		self.root_widget = RelativeLayout()
		self.bg_texture = CoreImage('bg.jpg').texture
		self.bg_rect = Rectangle(texture = self.bg_texture, pos = self.root_widget.pos, size = Window.size)
		self.root_widget.canvas.add(self.bg_rect)
		Window.bind(size = self.on_size)
		self.determine_font_size()
		self.menu_widget = MenuWidget(self)
		self.verses = []
		self.verses_widget = VersesWidget(self)
		self.options_widget = OptionsWidget(self)
		self.add_verse_widget = AddVerseWidget(self)
		self.memorize_widget = MemorizeWidget(self)
		self.verse_widget = VerseWidget(self)
		self.add_verse_popup = Popup(title = 'Add Verse', content=Label(text='Fetching verse...'))
	
	def on_pause(self):
		return True
		
	def on_resume(self):
		pass
	
	def on_size(self, width, height):
		self.bg_rect.size = Window.size
	
	def determine_font_size(self):
		pixel_count = Window.size[0] * Window.size[1]
		if pixel_count < 921600:
			self.font_size = 42
			self.word_wrap = 5
		elif pixel_count < 1440000:
			self.font_size = 57
			self.word_wrap = 6
		else:
			self.font_size = 72
			self.word_wrap = 7
	
	def get_verses(self):
		return self.verses
	
	def add_verse(self, book, chapter, verse):
		self.add_verse_popup.open()
		data = urllib2.urlopen('http://labs.bible.org/api/?type=json&passage=' + str(book) + '%20' + str(chapter) + ':' + str(verse))
		json_data = json.load(data)
		self.verses.append(BibleVerse(str(book) + ' ' + str(chapter) + ': ' + str(verse), json_data[0]['text']))
		self.add_verse_popup.dismiss()
	
	def remove_verse(self, verse):
		self.verses.remove(verse)
	
	def set_widget(self, widget):
		self.root_widget.clear_widgets()
		if widget == self.WID_VERSES:
			self.verses_widget.refresh()
			self.root_widget.add_widget(self.verses_widget)
		elif widget == self.WID_MENU:
			self.root_widget.add_widget(self.menu_widget)
		elif widget == self.WID_OPTIONS:
			self.root_widget.add_widget(self.options_widget)
		elif widget == self.WID_ADD_VERSE:
			self.root_widget.add_widget(self.add_verse_widget)
		elif widget == self.WID_MEMORIZE:
			self.memorize_widget.refresh()
			self.root_widget.add_widget(self.memorize_widget)
		elif widget == self.WID_VERSE:
			self.verse_widget.current_verse = 0
			self.verse_widget.refresh()
			self.root_widget.add_widget(self.verse_widget)
		
	def build(self):
		self.title = 'Bible Verse Memory'
		self.set_widget(self.WID_MENU)
		return self.root_widget

if __name__ == '__main__':
    KivyApp().run()
