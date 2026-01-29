#!/usr/bin/env python3
"""
Chemical Equipment Parameter Visualizer - Desktop Application
Main entry point.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from api_client import APIClient
from ui.main_window import MainWindow, LoginDialog


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setStyle('Fusion')
    
    # Create API client
    api_client = APIClient()
    
    # Show login dialog
    login_dialog = LoginDialog()
    
    while True:
        if login_dialog.exec_() == login_dialog.Accepted:
            username, password = login_dialog.get_credentials()
            
            if not username or not password:
                QMessageBox.warning(
                    None,
                    "Invalid Input",
                    "Please enter both username and password."
                )
                continue
            
            try:
                # Attempt login
                api_client.login(username, password)
                
                # Login successful - show main window
                window = MainWindow(api_client)
                window.show()
                
                # Try to load initial data
                try:
                    window.load_data()
                except:
                    pass  # No data available yet
                
                sys.exit(app.exec_())
                
            except Exception as e:
                error_msg = str(e)
                if 'Unauthorized' in error_msg or '401' in error_msg:
                    QMessageBox.critical(
                        None,
                        "Login Failed",
                        "Invalid username or password."
                    )
                else:
                    QMessageBox.critical(
                        None,
                        "Connection Error",
                        f"Could not connect to server:\n{error_msg}\n\n"
                        "Please ensure the Django backend is running on http://127.0.0.1:8000"
                    )
                    break
        else:
            # User cancelled login
            break


if __name__ == '__main__':
    main()
