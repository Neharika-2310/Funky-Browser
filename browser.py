import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Funky Browser")
        self.setWindowIcon(QIcon())  

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.update_title_on_tab_change)

        
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #333;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #222;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                top: -1px;
            }
        """)

        self.setCentralWidget(self.tabs)

        # Navigation bar
        nav = QToolBar()
        self.addToolBar(nav)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        nav.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.go_home)
        nav.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav.addWidget(self.url_bar)

        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        nav.addAction(new_tab_btn)

        # Dark application theme
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(dark_palette)

        self.showMaximized()

        # Initial tab with home.html
        home_path = os.path.abspath("home.html")
        self.add_new_tab(QUrl.fromLocalFile(home_path), "Welcome to Neharika's Browser")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda q, browser=browser: self.update_urlbar(q, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.update_tab_title(i, browser))

    def update_tab_title(self, index, browser):
        title = browser.page().title()
        self.tabs.setTabText(index, title)
        if self.current_browser() == browser:
            self.setWindowTitle(f"My Funky Browser - {title}")

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'https://www.google.com/search?q=' + url
        self.current_browser().setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(q.toString())

    def update_title_on_tab_change(self, index):
        browser = self.tabs.widget(index)
        if isinstance(browser, QWebEngineView):
            title = browser.page().title()
            self.setWindowTitle(f"My Funky Browser - {title}")
            self.url_bar.setText(browser.url().toString())

    def go_home(self):
        home_path = os.path.abspath("home.html")
        self.current_browser().setUrl(QUrl.fromLocalFile(home_path))


app = QApplication(sys.argv)
QApplication.setApplicationName("My Funky Browser")
window = Browser()
app.exec_()
