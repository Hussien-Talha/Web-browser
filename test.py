# Import the PyQt5 modules
from msilib.schema import SelfReg
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QProgressBar, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Define the main window class
class BrowserWindow(QMainWindow):
    # Initialize the window
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Simple Web Browser")
        # Set the window size
        self.resize(800, 600)
        # Create the main widget
        self.main_widget = QWidget()
        # Create the layout for the main widget
        self.main_layout = QVBoxLayout()
        # Create the navigation bar widget
        self.nav_bar = QWidget()
        # Create the layout for the navigation bar
        self.nav_layout = QHBoxLayout()
        # Create the back button
        self.back_button = QPushButton("<")
        # Connect the back button to the go_back method
        self.back_button.clicked.connect(self.go_back)
        # Add the back button to the navigation layout
        self.nav_layout.addWidget(self.back_button)
        # Create the refresh button
        self.refresh_button = QPushButton("Refresh")
        # Connect the refresh button to the reload method
        self.refresh_button.clicked.connect(self.reload)
        # Add the refresh button to the navigation layout
        self.nav_layout.addWidget(self.refresh_button)
        # Create the address bar
        self.address_bar = QLineEdit()
        # Connect the address bar to the load_url method
        self.address_bar.returnPressed.connect(self.load_url)
        # Add the address bar to the navigation layout
        self.nav_layout.addWidget(self.address_bar)
        # Create the go button
        self.go_button = QPushButton("Go")
        # Connect the go button to the load_url method
        self.go_button.clicked.connect(self.load_url)
        # Add the go button to the navigation layout
        self.nav_layout.addWidget(self.go_button)
        # Set the navigation layout for the navigation bar widget
        self.nav_bar.setLayout(self.nav_layout)
        # Add the navigation bar widget to the main layout
        self.main_layout.addWidget(self.nav_bar)
        # Create the web view widget
        self.web_view = QWebEngineView()
        # Load a default URL for testing purposes
        self.web_view.load(QUrl("https://www.bing.com"))
        # Connect the web view to the update_address_bar method
        self.web_view.urlChanged.connect(self.update_address_bar)
        # Add the web view widget to the main layout
        self.main_layout.addWidget(self.web_view)
        # Connect history label to web view's loadStarted signal 
        self.web_view.loadStarted.connect(self.update_history_label)
        # Create a history list to store visited URLs as strings
        self.history = []
        # Create the status bar widget
        self.status_bar = QWidget()
        # Create the layout for the status bar
        self.status_layout = QHBoxLayout()
        # Create the progress bar
        self.progress_bar = QProgressBar()
        # Connect the progress bar to the web view's loadProgress signal
        self.web_view.loadProgress.connect(self.progress_bar.setValue)
        # Add the progress bar to the status layout
        self.status_layout.addWidget(self.progress_bar)
        # Create the URL label
        self.url_label = QLabel()
        # Connect the URL label to the web view's urlChanged signal
        self.web_view.urlChanged.connect(self.update_url_label)
        # Add the URL label to the status layout
        self.status_layout.addWidget(self.url_label)
        # Add the history label to the status layout
        self.status_layout.addWidget(self.history_label)
        # Set the status layout for the status bar widget
        self.status_bar.setLayout(self.status_layout)
        # Add the status bar widget to the main layout
        self.main_layout.addWidget(self.status_bar)
        # Set the main layout for the main widget
        self.main_widget.setLayout(self.main_layout)
        # Set the main widget as the central widget of the window
        self.setCentralWidget(self.main_widget)
        
        


# Create a history feature that allows user to view and access previously visited websites


# Create a history label to display history information on status bar
SelfReg.history_label = QLabel()

# Define a method to update history list and label when a new URL is loaded

def update_history_label(self):
    # Get current URL as string and append it to history list if not already in it 
    current_url = self.web_view.url().toString()
    if current_url not in self.history:
      self.history.append(current_url)
    # Set text for history label as number of visited websites and current URL 
    self.history_label.setText(f"History: {len(self.history)} sites | Current: {current_url}")

# Define a method to show history list in a new window when user presses Ctrl+H

def show_history(self, event):
    # Check if Ctrl+H is pressed 
    if QApplication.keyboardModifiers() == Qt.ControlModifier and event.key() == Qt.Key_H:
      # Create a new window 
      history_window = QWidget()
      # Set window title as "History"
      history_window.setWindowTitle("History")
      # Set window size as 400x300 
      history_window.resize(400, 300)
      # Create a layout for history window 
      history_layout = QVBoxLayout()
      # Loop through history list and create a label for each URL 
      for url in self.history:
          url_label = QLabel(url)
          # Connect url label to load_history_url method 
          url_label.mousePressEvent = lambda event, url=url: self.load_history_url(url)
          # Add url label to history layout 
          history_layout.addWidget(url_label)
      # Set history layout for history window 
      history_window.setLayout(history_layout)
      # Show history window 
      history_window.show()

# Define a method to load a URL from history list when user clicks on it 

def load_history_url(self, url):
    # Load URL in web view 
    self.web_view.load(QUrl(url))
    # Close history window 
    self.close()

# Override the keyPressEvent method to enable show_history method 

def keyPressEvent(self, event): 
    # Call the show_history method 
    self.show_history()
    # Call the parent class's keyPressEvent method 
    super(BrowserWindow, self).keyPressEvent(event)

# Define a method to go back to the previous page
def go_back(self):
    # Check if there is a previous page in history
    if self.web_view.history().canGoBack():
        # Go back to the previous page
        self.web_view.back()

# Define a method to reload the current page
def reload(self):
    # Reload the current page
    self.web_view.reload()

# Define a method to load a URL from the address bar
def load_url(self):
    # Get the text from the address bar
    url = self.address_bar.text()
    # Check if the text is a valid URL
    if QUrl(url).isValid():
        # Load the URL in the web view
        self.web_view.load(QUrl(url))
    else:
        # Display an error message in the address bar
        self.address_bar.setText("Invalid URL")

# Define a method to update the address bar with the current URL
def update_address_bar(self, url):
    # Set the text of the address bar as the current URL
    self.address_bar.setText(url.toString())

# Define a method to update the URL label with the current URL
def update_url_label(self, url):
    # Set the text of the URL label as the current URL
    self.url_label.setText(url.toString())

# Create an instance of QApplication
app = QApplication([])
# Create an instance of BrowserWindow
window = BrowserWindow()
# Show the window
window.show()
# Run the application loop
app.exec_()