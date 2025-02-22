import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import * 
from PyQt6.QtGui import *
import configparser
import json



config_path = "./config/config.conf"
config = configparser.ConfigParser()
config.read(config_path)

language = config["Language"]["language"]

with open(f"./public/browser/languages/{language}.json", "r", encoding="UTF-8") as jsonn:
    texts = json.load(jsonn)

tab_name =  texts["tab-name"]
history = "./public/browser/history.txt"
bookmarks = "./public/browser/bookmarks.txt"

if not os.path.exists(history):
    with open(history, 'x') as history_file:
       pass 
if not os.path.exists(config_path):
    with open(config_path, 'w') as cf:
        cf.write("""[Settings]
search_engine = https://google.com

[Appearance]
tab_color = #2aa1b3
not_selected_tab_color = #22818f

[Language]
language = tr-TR
""")
if not os.path.exists(bookmarks):
    with open(bookmarks, 'x') as bf:
        pass



search_engine = config['Settings']['search_engine']
tab_color = config['Appearance']['tab_color']
notselected_tab_color = config["Appearance"]["not_selected_tab_color"]

class AnkaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
           
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""            
        QTabBar::tab{{
             background: {notselected_tab_color};
             min-width:125px;
             max-width:200px;
             height:25px;
             border-radius: 10px;
             padding: 5px;

        
        
        }}
        QTabBar::tab::selected{{
            background: {tab_color};
        }}
""")
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.setWindowIcon(QIcon("public/img/logo.ico"))

        self.add_new_tab(QUrl(search_engine), tab_name)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.url_bar.setPlaceholderText(texts["url_bar_placeholder"])
        self.url_bar.setFont(QFont("Lexend"))
        self.url_bar.setFixedHeight(25)
        self.url_bar.setStyleSheet("white-space: nowrap;")
       

        self.back_button = QPushButton()
        self.back_button.clicked.connect(self.browser_back)
        self.back_button.setIcon(QIcon("./public/img/back.png"))
        self.back_button.setFixedSize(QSize(20, 20))
        self.back_button.setIconSize(QSize(20, 20))
        self.back_button.setStyleSheet("background-color: transparent; border: none;")
        self.back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.forward_button = QPushButton()
        self.forward_button.clicked.connect(self.browser_forward)
        self.forward_button.setIcon(QIcon("public/img/forward.png"))
        self.forward_button.setFixedSize(QSize(20, 20))
        self.forward_button.setIconSize(QSize(20, 20))
        self.forward_button.setStyleSheet("background-color: transparent; border: none;")
        self.forward_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.new_tab_button = QPushButton()
        self.new_tab_button.clicked.connect(self.add_new_tab_button)
        self.new_tab_button.setIcon(QIcon("public/img/newtab.png"))
        self.new_tab_button.setFixedSize(QSize(20, 20))
        self.new_tab_button.setIconSize(QSize(20, 20))
        self.new_tab_button.setStyleSheet("background-color: transparent; border: none;")
        self.new_tab_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.reload_button = QPushButton()
        self.reload_button.clicked.connect(self.browser_reload)
        self.reload_button.setIcon(QIcon("public/img/reload.png"))
        self.reload_button.setFixedSize(QSize(20, 20))
        self.reload_button.setIconSize(QSize(20, 20))
        self.reload_button.setStyleSheet("background-color: transparent; border: none;")
        self.reload_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.bookmark_button = QPushButton() 
        self.bookmark_button.clicked.connect(self.bookmark)
        self.bookmark_button.setIcon(QIcon("public/img/bookmark-regular.png"))
        self.bookmark_button.setFixedSize(QSize(20,20))
        self.bookmark_button.setIconSize(QSize(20,20))
        self.bookmark_button.setStyleSheet("background-color: transparent; border: none;")
        self.bookmark_button.setCursor(Qt.CursorShape.PointingHandCursor)

        
        self.settings_button = QPushButton()
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setIcon(QIcon("public/img/settingsbar.png"))
        self.settings_button.setFixedSize(QSize(20, 20))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setStyleSheet("background-color: transparent; border: none; margin-right: 8px;")
        self.settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0,0,0,0)
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.forward_button)
        top_layout.addWidget(self.new_tab_button)
        top_layout.addWidget(self.reload_button)
        top_layout.addWidget(self.bookmark_button)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.settings_button)

        bookmarks_layout = QHBoxLayout()
        bookmarks_layout.setContentsMargins(0,0,0,0)

        self.load_bookmarks(bookmarks_layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bookmarks_layout)
          
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Anka")
        self.showMaximized()  
        self.setWindowIcon(QIcon("public/img/logo.ico"))
        self.resize(1920, 1080)

        self.tabs.currentChanged.connect(self.update_url_from_tab)

        
    def add_new_tab(self, url, label):
        new_browser = QWebEngineView()
        new_browser.setUrl(QUrl(search_engine))
        self.tabs.addTab(new_browser, label)
        self.tabs.setCurrentWidget(new_browser)
        
        self.close_tab_button = QPushButton()
        self.close_tab_button.clicked.connect(lambda: self.close_tab(self.tabs.indexOf(new_browser)))
        self.close_tab_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        new_browser.titleChanged.connect(lambda title: self.update_title(new_browser, title))
        new_browser.urlChanged.connect(lambda q: self.update_url(q))
        new_browser.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        new_browser.customContextMenuRequested.connect(self.show_context_menu)
    def close_tab(self, index):
        if self.tabs.count() == 1:
            exit()
        else:
            self.tabs.removeTab(index)
 
    def update_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, title if title else tab_name)

    def add_new_tab_button(self):
        self.add_new_tab(search_engine, tab_name)

    def update_url(self, url):
        if isinstance(url, QUrl):
            self.url_bar.setText(url.toString())
        else:
            self.url_bar.clear()
        current_browser = self.tabs.currentWidget()
        current_browser.setUrl(QUrl(url))
        with open(history, 'r', encoding="utf-8") as file:
            old_history = file.read()
            new_history = current_browser.url().toString() + "\n" + old_history
        with open(history, 'w', encoding="utf-8") as file:
            file.write(new_history)


    def update_url_from_tab(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_url = current_browser.url()
            self.url_bar.setText(current_url.toString())

    def load_url(self):
        url = self.url_bar.text()
        if url.startswith("http://") or url.startswith("https://"):
            url = url
        else:
            if search_engine == "https://duckduckgo.com":
                url = search_engine + "/?q=" + url
            else:
                url = search_engine + "/search?q=" + url
        
        
        self.update_url(url)        
           

    def browser_back(self):
        current_browser = self.tabs.currentWidget()
        current_browser.back()

    def browser_forward(self):
        current_browser = self.tabs.currentWidget()
        current_browser.forward()
    
    def browser_reload(self):
        current_browser = self.tabs.currentWidget()
        current_browser.reload() 

    def show_context_menu(self, position):
        context_menu = QMenu(self)

        context_menu.addAction(texts["right-click-copy"], self.browser_copy)
        context_menu.addAction(texts["right-click-paste"], self.browser_paste)
        context_menu.addAction(texts["right-click-save"], self.browser_save)
        context_menu.addAction(texts["right-click-back"], self.browser_back)
        context_menu.addAction(texts["right-click-forward"], self.browser_forward)
        context_menu.addAction(texts["right-click-reload"], self.browser_reload)
        

        context_menu.exec(self.tabs.currentWidget().mapToGlobal(position))

    def browser_copy(self):
        current_browser = self.tabs.currentWidget()
        current_browser.page().runJavaScript("window.getSelection().toString();", self.set_clipboard)

    def set_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def browser_paste(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        current_browser = self.tabs.currentWidget()
        current_browser.page().runJavaScript(f"document.execCommand('insertText', false, '{text}');")
    


    def browser_save(self):
        current_browser = self.tabs.currentWidget()
        current_browser.page().toHtml(self.save_html)

    def save_html(self, html):
        file_name, _ = QFileDialog.getSaveFileName(self, "Kaydet", "", "HTML Dosyası (*.html);;WEBP Dosyası(*.webp);;Tüm Dosyalar (*)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(html)
    def open_settings(self):
        settings = AnkaBrowserSettings(self)
        settings.exec()
    def bookmark(self):
      current_browser = self.tabs.currentWidget()
      current_url = current_browser.url().toString()

      with open(bookmarks, 'r+', encoding="utf-8") as bookmarks_file:
        bookmarks_content = bookmarks_file.read()
        if current_url not in bookmarks_content:
            bookmarks_file.write(current_url + "\n")
                    
    def load_bookmarks(self, top_layout):
        with open(bookmarks, 'r', encoding="utf-8") as bookmarks_file:
            urls = bookmarks_file.readlines()

            for url in urls:
                url = url.strip()
                if url:

                    bookmark_button = QPushButton(url)
                    bookmark_button.setFixedWidth(150)
                    bookmark_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    bookmark_button.clicked.connect(lambda checked, url=url: self.add_new_tab(QUrl(url), url))
                    top_layout.addWidget(bookmark_button)   
                

     

       
class AnkaBrowserSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(texts["settings-title"])
        self.setFixedSize(QSize(500,300))
        

        layout = QVBoxLayout()
 
        self.search_engine_label = QLabel(texts["settings-search-engine"])
        layout.addWidget(self.search_engine_label)
    
        self.search_engine = QComboBox()
        self.search_engine.setFixedSize(QSize(450,25))
        self.search_engine.addItem("Google")
        self.search_engine.addItem("DuckDuckGo")
        self.search_engine.addItem("Bing")
        self.search_engine.addItem("Brave")
        self.search_engine.addItem("Startpage")
        
        self.language_label = QLabel("Dil / Language")
        layout.addWidget(self.language_label)

        if search_engine == "https://google.com":
            self.search_engine.setCurrentIndex(0)
        elif search_engine == "https://duckduckgo.com":
            self.search_engine.setCurrentIndex(1)
        elif search_engine == "https://bing.com":
            self.search_engine.setCurrentIndex(2)
        elif search_engine == "https://search.brave.com":
            self.search_engine.setCurrentIndex(3)
        elif search_engine == "https://startpage.com":
            self.search_engine.setCurrentIndex(4)

        layout.addWidget(self.search_engine)
        
        self.language = QComboBox()
        self.language.setFixedSize(450,25)
        self.language.addItem("tr-TR")
        self.language.addItem("en-EN")
      
        if language == "tr-TR":
           self.language.setCurrentIndex(0)
        else:
            self.language.setCurrentIndex(1)
        
        layout.addWidget(self.language)

        self.tab_color_button_label = QLabel(texts["settings-tab-color-label"])
        layout.addWidget(self.tab_color_button_label)

        self.tab_color_button = QPushButton(texts["settings-tab-color-button"])
        self.tab_color_button.setFixedSize(QSize(450,25))
        self.tab_color_button.clicked.connect(self.open_tab_color_dialog)
        layout.addWidget(self.tab_color_button)
        
        self.delete_history_button = QPushButton(texts["settings-history"])
        self.delete_history_button.setFixedSize(QSize(450,25))
        self.delete_history_button.clicked.connect(self.delete_history)
        layout.addWidget(self.delete_history_button)

        self.note_label = QLabel(texts["settings-info-msg"])
        self.note_label.setStyleSheet("padding-top: 5px;")
        layout.addWidget(self.note_label)
         
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.button(QDialogButtonBox.StandardButton.Cancel).setText(texts["settings-button-cancel"])
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setText(texts["settings-button-ok"])
        self.buttons.accepted.connect(self.ok)
        self.buttons.rejected.connect(self.cancel)
        layout.addWidget(self.buttons)
        
        self.setLayout(layout)
    def ok(self):
        s_engine = self.search_engine.currentText()
        if s_engine == "Google":
            config["Settings"]["search_engine"] = "https://google.com"
        elif s_engine == "DuckDuckGo":
            config["Settings"]["search_engine"] = "https://duckduckgo.com"
        elif s_engine == "Bing":
            config["Settings"]["search_engine"] = "https://bing.com"
        elif s_engine == "Brave":
            config["Settings"]["search_engine"] = "https://search.brave.com"
        elif s_engine == "StartPage":
            config["Settings"]["search_engine"] = "https://startpage.com"

        lan = self.language.currentText()
        match lan:
           case "tr-TR":
             config["Language"]["language"] = "tr-TR"
           case "en-EN":
             config["Language"]["language"] = "en-EN"
        
        with open('config/config.conf', 'w' ) as configfile:
            config.write(configfile)
        self.accept()
        
    def cancel(self):
        self.reject()
    
    
    def open_tab_color_dialog(self):
        tab_color_dialog = Tab_Color_Dialog()
        tab_color_dialog.exec()
    
    def delete_history(self):
        with open(history, 'w', encoding="utf-8") as file:
            file.write(" ")

class Tab_Color_Dialog(QColorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(texts["tab-color-dialog-title"])
        self.setFixedSize(QSize(500,159))

        tabColor = Tab_Color_Dialog.getColor()     
        not_selected_tab_color = tabColor.darker(125)
        tabColor = tabColor.name()
        not_selected_tab_color = not_selected_tab_color.name()

        
        config["Appearance"]["tab_color"] = str(tabColor)
        config["Appearance"]["not_selected_tab_color"] = str(not_selected_tab_color)

        with open('config/config.conf', 'w' ) as configfile:
            config.write(configfile)
     
 
if __name__ == "__main__":
    app = QApplication(sys.argv)      
    anka_browser_window = AnkaBrowser()
    anka_browser_window.show()  
    sys.exit(app.exec())
