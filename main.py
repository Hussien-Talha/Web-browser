# Import PyQt5 modules
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTabWidget, QTabBar, QLabel, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

# Define the web browser class
class WebGPT(QMainWindow):
    # Initialize the web browser
    def __init__(self):
        super().__init__()
        # Set the window title and icon
        self.setWindowTitle("WebGPT - The Generative Web Browser")
        self.setWindowIcon(QIcon("wg.png"))
        # Set the default window size
        self.resize(800, 600)
        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # Create the main layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        # Create the address bar
        self.address_bar = QLineEdit()
        self.address_bar.setFixedHeight(30)
        self.address_bar.setStyleSheet("background-color: white; border: 1px solid black;")
        # Connect the address bar to the load_url method
        self.address_bar.returnPressed.connect(self.load_url)
        # Create the navigation buttons
        self.back_button = QPushButton()
        self.back_button.setFixedSize(30, 30)
        self.back_button.setIcon(QIcon("back.png"))
        self.back_button.setEnabled(False)
        # Connect the back button to the go_back method
        self.back_button.clicked.connect(self.go_back)
        self.forward_button = QPushButton()
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.setIcon(QIcon("forward.png"))
        self.forward_button.setEnabled(False)
        # Connect the forward button to the go_forward method
        self.forward_button.clicked.connect(self.go_forward)
        self.refresh_button = QPushButton()
        self.refresh_button.setFixedSize(30, 30)
        self.refresh_button.setIcon(QIcon("refresh.png"))
        # Connect the refresh button to the reload method
        self.refresh_button.clicked.connect(self.reload)
        self.stop_button = QPushButton()
        self.stop_button.setFixedSize(30, 30)
        self.stop_button.setIcon(QIcon("stop.png"))
        # Connect the stop button to the stop method
        self.stop_button.clicked.connect(self.stop)
        # Create the home button
        self.home_button = QPushButton()
        self.home_button.setFixedSize(30, 30)
        self.home_button.setIcon(QIcon("home.png"))
        # Connect the home button to the go_home method
        self.home_button.clicked.connect(self.go_home)
        
# Create the navigation layout
        self.navigation_layout = QHBoxLayout()
        # Add the navigation buttons and the address bar to the navigation layout
        self.navigation_layout.addWidget(self.back_button)
        self.navigation_layout.addWidget(self.forward_button)
        self.navigation_layout.addWidget(self.refresh_button)
        self.navigation_layout.addWidget(self.stop_button)
        self.navigation_layout.addWidget(self.address_bar)
        self.navigation_layout.addWidget(self.home_button)
        # Add the navigation layout to the main layout
        self.main_layout.addLayout(self.navigation_layout)
        # Create the tab widget
        self.tab_widget = QTabWidget()
        # Set the tab widget to fill the remaining space
        self.tab_widget.setSizePolicy(1, 1)
        # Set the tab widget to have no border
        self.tab_widget.setStyleSheet("border: none;")
        # Set the tab widget to have a tab bar below the address bar
        self.tab_widget.setTabPosition(QTabWidget.North)
        # Set the tab widget to allow closing tabs
        self.tab_widget.setTabsClosable(True)
        # Connect the tab widget to the close_tab method
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        # Set the tab widget to allow opening new tabs
        self.tab_widget.setMovable(True)
        # Create a new tab button on the right side of the tab bar
        self.new_tab_button = QPushButton()
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.setIcon(QIcon("new.png"))
        # Connect the new tab button to the new_tab method
        self.new_tab_button.clicked.connect(self.new_tab)
        # Add the new tab button to the tab bar
        self.tab_widget.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)
        # Add the tab widget to the main layout
        self.main_layout.addWidget(self.tab_widget)
        # Create the bookmark bar
        self.bookmark_bar = QWidget()
        self.bookmark_bar.setFixedHeight(30)
        self.bookmark_bar.setStyleSheet("background-color: lightblue;")
        # Create the bookmark layout
        self.bookmark_layout = QHBoxLayout()
        self.bookmark_layout.setContentsMargins(0, 0, 0, 0)
        self.bookmark_bar.setLayout(self.bookmark_layout)
   
# Create a list of bookmarks
        self.bookmarks = []
        # Load the bookmarks from a file
        self.load_bookmarks()
        # Add the bookmarks to the bookmark layout
        for bookmark in self.bookmarks:
            self.add_bookmark(bookmark)
        # Add the bookmark bar to the main layout
        self.main_layout.addWidget(self.bookmark_bar)
        # Create the status bar
        self.status_bar = QLabel()
        self.status_bar.setFixedHeight(20)
        self.status_bar.setStyleSheet("background-color: white; border: 1px solid black;")
        # Add the status bar to the main layout
        self.main_layout.addWidget(self.status_bar)
        # Create a new tab
        self.new_tab()
        
# Define the method to load a URL or a search query
    def load_url(self):
        # Get the text from the address bar
        url = self.address_bar.text()
        # Check if the text is empty or invalid
        if not url or not QUrl(url).isValid():
            # Show an error message below the address bar
            self.status_bar.setText("Error: Invalid URL or empty input")
            self.status_bar.setStyleSheet("color: red;")
            return
        # Check if the text is a search query
        if not url.startswith("http://") and not url.startswith("https://"):
            # Use Bing as the default search engine
            url = "https://www.bing.com/search?q=" + url
        # Load the URL in the current web view
        self.current_web_view().load(QUrl(url))
        
# Define the method to go back in the browsing history
    def go_back(self):
        # Go back in the current web view
        self.current_web_view().back()
        
    # Define the method to go forward in the browsing history
    def go_forward(self):
        # Go forward in the current web view
        self.current_web_view().forward()
        
    # Define the method to reload the current web page
    def reload(self):
        # Reload the current web view
        self.current_web_view().reload()
        
    # Define the method to stop loading the current web page
    def stop(self):
        # Stop loading the current web view
        self.current_web_view().stop()
        
    # Define the method to go to the home page
    def go_home(self):
        # Load the home page in the current web view
        self.current_web_view().load(QUrl(self.home_page))
        
# Define the method to create a new tab
    def new_tab(self):
        # Create a new web view
        web_view = QWebEngineView()
        # Connect the web view to the update_title method
        web_view.titleChanged.connect(self.update_title)
        # Connect the web view to the update_icon method
        web_view.iconChanged.connect(self.update_icon)
        # Connect the web view to the update_url method
        web_view.urlChanged.connect(self.update_url)
        # Connect the web view to the update_status method
        web_view.loadStarted.connect(self.update_status)
        web_view.loadProgress.connect(self.update_status)
        web_view.loadFinished.connect(self.update_status)
        # Connect the web view to the update_link method
        web_view.linkHovered.connect(self.update_link)
        # Add the web view to the tab widget
        self.tab_widget.addTab(web_view, "New Tab")
        # Set the current tab to the new tab
        self.tab_widget.setCurrentWidget(web_view)
        # Go to the home page in the new tab
        self.go_home()
        
# Define the method to close a tab
    def close_tab(self, index):
        # Get the web view at the given index
        web_view = self.tab_widget.widget(index)
        # Delete the web view
        web_view.deleteLater()
        # Remove the tab at the given index
        self.tab_widget.removeTab(index)
        
    # Define the method to update the title of a tab
    def update_title(self, title):
        # Get the current web view
        web_view = self.current_web_view()
        # Get the current tab index
        index = self.tab_widget.currentIndex()
        # Set the tab text to the title or "New Tab" if no title is available
        self.tab_widget.setTabText(index, title or "New Tab")
        
    # Define the method to update the icon of a tab
    def update_icon(self, icon):
        # Get the current web view
        web_view = self.current_web_view()
        # Get the current tab index
        index = self.tab_widget.currentIndex()
        # Set the tab icon to the icon or a default icon if no icon is available
        self.tab_widget.setTabIcon(index, icon or QIcon("default.png"))
        
# Define the method to update the URL of the address bar
    def update_url(self, url):
        # Get the current web view
        web_view = self.current_web_view()
        # Set the address bar text to the URL
        self.address_bar.setText(url.toString())
        
    # Define the method to update the status of the status bar
    def update_status(self, value=None):
        # Get the current web view
        web_view = self.current_web_view()
        # Check if the web view is loading
        if web_view.isLoading():
            # Set the status bar text to "Loading..." and the progress value
            self.status_bar.setText(f"Loading... {value}%")
            self.status_bar.setStyleSheet("color: black;")
            # Disable the refresh button and enable the stop button
            self.refresh_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            # Set the status bar text to "Done" or "Error" depending on the load status
            if web_view.loadStatus() == QWebEngineView.LoadSucceededStatus:
                self.status_bar.setText("Done")
                self.status_bar.setStyleSheet("color: black;")
            else:
                self.status_bar.setText("Error")
                self.status_bar.setStyleSheet("color: red;")
            # Enable the refresh button and disable the stop button
            self.refresh_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        
# Define the method to update the link of the status bar
    def update_link(self, link):
        # Set the status bar text to the link or an empty string if no link is hovered
        self.status_bar.setText(link or "")
        
    # Define the method to get the current web view
    def current_web_view(self):
        # Return the current widget of the tab widget
        return self.tab_widget.currentWidget()
        
    # Define the method to load the bookmarks from a file
    def load_bookmarks(self):
        # Try to open the bookmarks file
        try:
            with open("bookmarks.txt", "r") as file:
                # Read each line of the file
                for line in file:
                    # Split the line by a comma
                    url, title = line.split(",")
                    # Strip the whitespace and newline characters
                    url = url.strip()
                    title = title.strip()
                    # Create a bookmark dictionary with the url and title
                    bookmark = {"url": url, "title": title}
                    # Append the bookmark to the bookmarks list
                    self.bookmarks.append(bookmark)
        # Handle the exception if the file does not exist or is corrupted
        except Exception as e:
            # Print the error message
            print(e)
            
# Define the method to add a bookmark to the bookmark layout
    def add_bookmark(self, bookmark):
        # Create a bookmark button
        bookmark_button = QPushButton()
        bookmark_button.setFixedSize(100, 30)
        # Set the bookmark button text to the title or "No Title" if no title is available
        bookmark_button.setText(bookmark["title"] or "No Title")
        # Set the bookmark button icon to the favicon or a default icon if no favicon is available
        bookmark_button.setIcon(QIcon(bookmark["url"] + "/favicon.ico") or QIcon("default.png"))
        # Set the bookmark button tooltip to the url
        bookmark_button.setToolTip(bookmark["url"])
        # Connect the bookmark button to the load_bookmark method
        bookmark_button.clicked.connect(lambda: self.load_bookmark(bookmark["url"]))
        # Connect the bookmark button to the show_bookmark_menu method
        bookmark_button.setContextMenuPolicy(Qt.CustomContextMenu)
        bookmark_button.customContextMenuRequested.connect(lambda: self.show_bookmark_menu(bookmark))
        # Add the bookmark button to the bookmark layout
        self.bookmark_layout.addWidget(bookmark_button)
        
# Define the method to load a bookmarked web page
    def load_bookmark(self, url):
        # Load the url in the current web view
        self.current_web_view().load(QUrl(url))
        
    # Define the method to show a bookmark context menu
    def show_bookmark_menu(self, bookmark):
        # Create a bookmark menu
        bookmark_menu = QMenu()
        # Create an edit action
        edit_action = QAction("Edit")
        # Connect the edit action to the edit_bookmark method
        edit_action.triggered.connect(lambda: self.edit_bookmark(bookmark))
        # Add the edit action to the bookmark menu
        bookmark_menu.addAction(edit_action)
        # Create a delete action
        delete_action = QAction("Delete")
        # Connect the delete action to the delete_bookmark method
        delete_action.triggered.connect(lambda: self.delete_bookmark(bookmark))
        # Add the delete action to the bookmark menu
        bookmark_menu.addAction(delete_action)
        # Show the bookmark menu at the cursor position
        bookmark_menu.exec_(QCursor.pos())
        
# Define the method to edit a bookmark
    def edit_bookmark(self, bookmark):
        # Get the bookmark button from the bookmark layout
        bookmark_button = self.bookmark_layout.itemAt(self.bookmarks.index(bookmark)).widget()
        # Get the new url and title from the user input
        new_url, ok1 = QInputDialog.getText(self, "Edit Bookmark", "Enter the new URL:")
        new_title, ok2 = QInputDialog.getText(self, "Edit Bookmark", "Enter the new title:")
        # Check if the user input is valid and not empty
        if ok1 and ok2 and new_url and new_title:
            # Update the bookmark dictionary with the new url and title
            bookmark["url"] = new_url
            bookmark["title"] = new_title
            # Update the bookmark button text to the new title or "No Title" if no title is available
            bookmark_button.setText(new_title or "No Title")
            # Update the bookmark button icon to the new favicon or a default icon if no favicon is available
            bookmark_button.setIcon(QIcon(new_url + "/favicon.ico") or QIcon("default.png"))
            # Update the bookmark button tooltip to the new url
            bookmark_button.setToolTip(new_url)
            # Save the bookmarks to a file
            self.save_bookmarks()
            
    # Define the method to delete a bookmark
    def delete_bookmark(self, bookmark):
        # Get the bookmark button from the bookmark layout
        bookmark_button = self.bookmark_layout.itemAt(self.bookmarks.index(bookmark)).widget()
        # Delete the bookmark button
        bookmark_button.deleteLater()
        # Remove the bookmark from the bookmarks list
        self.bookmarks.remove(bookmark)
        # Save the bookmarks to a file
        self.save_bookmarks()
        
    # Define the method to save the bookmarks to a file
    def save_bookmarks(self):
        # Try to open the bookmarks file
        try:
            with open("bookmarks.txt", "w") as file:
                # Write each bookmark to the file as a line with a comma separator
                for bookmark in self.bookmarks:
                    file.write(f"{bookmark['url']},{bookmark['title']}\n")
        # Handle the exception if the file cannot be opened or written
        except Exception as e:
            # Print the error message
            print(e)
            
# Create an application instance
app = QApplication(sys.argv)
# Create a web browser instance
browser = WebGPT()
# Show the web browser window
browser.show()
# Execute the application loop
sys.exit(app.exec_())