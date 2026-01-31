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
    from ui.main_window import LoginDialog, SignupDialog
    
    current_dialog = LoginDialog()
    
    while True:
        result = current_dialog.exec_()
        
        if result == 10: # Switch dialog
            if isinstance(current_dialog, LoginDialog):
                current_dialog = SignupDialog()
            else:
                current_dialog = LoginDialog()
            continue
            
        if result == current_dialog.Accepted:
            if isinstance(current_dialog, LoginDialog):
                username, password = current_dialog.get_credentials()
                if not username or not password:
                    QMessageBox.warning(None, "Invalid Input", "Please enter both username and password.")
                    continue
                try:
                    # Attempt login
                    api_client.login(username, password)
                    break # Success!
                except Exception as e:
                    error_msg = str(e)
                    if 'Unauthorized' in error_msg or '401' in error_msg:
                        QMessageBox.critical(None, "Login Failed", "Invalid username or password.")
                    else:
                        QMessageBox.critical(None, "Connection Error", f"Could not connect to server:\n{error_msg}")
                        # Don't break here, let user try again
                        
            elif isinstance(current_dialog, SignupDialog):
                username, password, email = current_dialog.get_credentials()
                confirm_password = current_dialog.confirm_input.text()
                
                if not username or not password:
                     QMessageBox.warning(None, "Invalid Input", "Username and password are required.")
                     continue
                
                if password != confirm_password:
                    QMessageBox.warning(None, "Password Mismatch", "Passwords do not match.")
                    continue
                    
                try:
                    # Attempt registration
                    api_client.register(username, password, email)
                    QMessageBox.information(None, "Success", "Account created successfully! You are now logged in.")
                    break # Success!
                except Exception as e:
                    QMessageBox.critical(None, "Registration Failed", f"Could not register:\n{str(e)}")

        else:
            # User cancelled
            return

    # Login/Register successful - show main window
    window = MainWindow(api_client)
    window.show()
    
    # Try to load initial data
    try:
        window.load_data()
    except:
        pass  # No data available yet
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
