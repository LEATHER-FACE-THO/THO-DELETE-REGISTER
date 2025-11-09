import sys
import os
import shutil
import winreg
import random
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import win32api
import win32con
import win32security
import threading
import webbrowser

class NeuralPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = []
        self.dx = random.uniform(-0.5, 0.5)
        self.dy = random.uniform(-0.5, 0.5)

    def move(self, width, height):
        self.x = (self.x + self.dx) % width
        self.y = (self.y + self.dy) % height

class CleanerPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("THO DELETE REGISTER")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        title_label = QLabel("THO DELETE REGISTER")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI';
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0.8), stop:0.5 rgba(0, 0, 0, 0.9), stop:1 rgba(0, 0, 0, 0.8));
                border-bottom: 2px solid #00ff00;
                letter-spacing: 2px;
                color: #00ff00;
            }
        """)
        title_layout.addWidget(title_label)
        
        min_btn = QPushButton("-")
        close_btn = QPushButton("×")
        for btn in (min_btn, close_btn):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: lime;
                    border: none;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 255, 0, 0.2);
                }
            """)
            title_layout.addWidget(btn)
        
        min_btn.clicked.connect(self.showMinimized)
        close_btn.clicked.connect(self.close)
        
        self.layout.addWidget(self.title_bar)
        
        console_label = QLabel("CONSOLA")
        console_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 14px;
                font-weight: bold;
                margin: 10px 15px 5px 15px;
            }
        """)
        self.layout.addWidget(console_label)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.75);
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 8px;
                font-family: 'Consolas';
                font-size: 12px;
                padding: 10px;
                margin: 0 15px;
                selection-background-color: rgba(0, 255, 0, 0.3);
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.4);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 255, 0, 0.5);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        self.layout.addWidget(self.console)

        buttons_layout = QHBoxLayout()
        
        self.launch_btn = QPushButton("LAUNCHER")
        self.launch_btn.setFixedHeight(40)
        self.launch_btn.setFixedWidth(200)
        self.launch_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 20, 0, 0.8);
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 30px;
            }
            QPushButton:hover {
                background-color: rgba(0, 40, 0, 0.9);
                border-color: #40ff40;
                color: #40ff40;
            }
            QPushButton:pressed {
                background-color: rgba(0, 60, 0, 1);
                border-color: #80ff80;
            }
        """)
        self.launch_btn.clicked.connect(self.start_cleaning)
        buttons_layout.addWidget(self.launch_btn)
        
        support_btn = QPushButton("SOPORTE DISCORD")
        support_btn.setFixedHeight(40)
        support_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(88, 101, 242, 0.8);
                color: white;
                border: 2px solid rgb(88, 101, 242);
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: rgba(88, 101, 242, 0.6);
            }
        """)
        support_btn.clicked.connect(lambda: webbrowser.open('https://discord.gg/Zcq7GD3FFH'))
        buttons_layout.addWidget(support_btn)
        
        self.layout.addLayout(buttons_layout)
        
        self.points = []
        for _ in range(30):
            point = NeuralPoint(
                random.randint(0, self.width()),
                random.randint(0, self.height())
            )
            self.points.append(point)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        
        self.old_pos = None
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        self.old_pos = None
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 200))
        gradient.setColorAt(0.5, QColor(0, 20, 0, 190))
        gradient.setColorAt(1, QColor(0, 0, 0, 200))
        painter.fillRect(self.rect(), gradient)
        
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(20)
        self.setGraphicsEffect(blur_effect)
        
        pen = QPen(QColor(0, 255, 0, 100))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for point in self.points:
            point.move(self.width(), self.height())
            for other in self.points:
                distance = ((point.x - other.x) ** 2 + (point.y - other.y) ** 2) ** 0.5
                if distance < 100:
                    alpha = int(255 * (1 - distance / 100))
                    pen.setColor(QColor(0, 255, 0, alpha))
                    painter.setPen(pen)
                    painter.drawLine(int(point.x), int(point.y), int(other.x), int(other.y))
        
        for point in self.points:
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            painter.drawEllipse(int(point.x) - 2, int(point.y) - 2, 4, 4)
    
    def log(self, message):
        self.console.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        QApplication.processEvents()
    
    def clean_temp_files(self):
        temp_paths = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp')
        ]
        
        for path in temp_paths:
            if path and os.path.exists(path):
                self.log(f"Cleaning temporary files in {path}")
                for item in os.listdir(path):
                    try:
                        item_path = os.path.join(path, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path, ignore_errors=True)
                    except:
                        pass
    
    def clean_registry(self):
        keys_to_clean = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Applets\Regedit"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\FirstFolder"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Search\RecentApps"),
            (winreg.HKEY_CURRENT_USER, r"Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\ShowJumpView"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectInput"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist")
        ]
        
        for root_key, sub_key in keys_to_clean:
            try:
                self.log(f"Cleaning registry key: {sub_key}")
                winreg.DeleteKey(root_key, sub_key)
            except:
                pass
    
    def clean_recent_files(self):
        recent_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')
        if os.path.exists(recent_path):
            self.log("Cleaning recent files")
            for item in os.listdir(recent_path):
                try:
                    os.remove(os.path.join(recent_path, item))
                except:
                    pass
    
    def clean_prefetch(self):
        prefetch_path = os.path.join(os.environ['SYSTEMROOT'], 'Prefetch')
        if os.path.exists(prefetch_path):
            self.log("Cleaning Windows Prefetch files...")
            try:
                for item in os.listdir(prefetch_path):
                    try:
                        os.remove(os.path.join(prefetch_path, item))
                    except:
                        pass
            except:
                pass

    def clean_downloads_history(self):
        self.log("Cleaning downloads history...")
        downloads_paths = [
            os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'INetCache'),
            os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'INetCookies'),
            os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'IEDownloadHistory'),
        ]
        
        for path in downloads_paths:
            if os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        try:
                            full_path = os.path.join(path, item)
                            if os.path.isfile(full_path):
                                os.remove(full_path)
                            elif os.path.isdir(full_path):
                                shutil.rmtree(full_path, ignore_errors=True)
                        except:
                            pass
                except:
                    pass

    def clean_power_history(self):
        self.log("Cleaning power usage history...")
        power_paths = [
            os.path.join(os.environ['SYSTEMROOT'], 'System32', 'winevt', 'Logs', 'Microsoft-Windows-Power-Troubleshooter%4Operational.evtx'),
            os.path.join(os.environ['SYSTEMROOT'], 'System32', 'winevt', 'Logs', 'Microsoft-Windows-Kernel-Power%4Thermal-Operational.evtx'),
        ]
        
        for path in power_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass

    def clean_event_logs(self):
        self.log("Cleaning Windows Event Logs...")
        try:
            os.system('wevtutil.exe cl Application')
            os.system('wevtutil.exe cl Security')
            os.system('wevtutil.exe cl System')
            os.system('wevtutil.exe cl "Windows PowerShell"')
        except:
            pass

    def self_clean(self):
        self.log("Initiating self-cleanup...")
        script_path = os.path.abspath(__file__)
        
        bat_path = os.path.join(os.environ['TEMP'], 'cleanup.bat')
        with open(bat_path, 'w') as f:
            f.write(f'''@echo off
timeout /t 2 /nobreak > nul
del "{script_path}"
del "%~f0"
''')
        
        os.startfile(bat_path)
        sys.exit()
    
    def start_cleaning(self):
        self.launch_btn.setEnabled(False)
        self.log("Starting system cleanup...")
        
        cleaning_thread = threading.Thread(target=self.clean_all)
        cleaning_thread.start()
    
    def create_fake_registry_entries(self):
        self.log("Creating alternative registry entries...")
        fake_entries = [
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.txt\OpenWithList", {"a": "notepad.exe", "b": "wordpad.exe", "c": "vscode.exe"}),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\OpenWithList", {"a": "chrome.exe", "b": "edge.exe", "c": "AcroRd32.exe"}),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run", {
                "WindowsSecurity": "Windows Security",
                "Steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
                "Discord": "C:\\Users\\User\\AppData\\Local\\Discord\\Update.exe",
                "EpicGamesLauncher": "C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe",
                "Spotify": "C:\\Users\\User\\AppData\\Roaming\\Spotify\\Spotify.exe",
                "OneDrive": "C:\\Users\\User\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe",
                "MSEdgeUpdate": "C:\\Program Files (x86)\\Microsoft\\EdgeUpdate\\MicrosoftEdgeUpdate.exe",
                "GoogleUpdate": "C:\\Program Files (x86)\\Google\\Update\\GoogleUpdate.exe"
            }),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.txt", {
                "0": "config.txt", "1": "readme.txt", "2": "notas.txt", "3": "tareas.txt"
            }),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.pdf", {
                "0": "manual_usuario.pdf", "1": "factura_internet.pdf", "2": "contrato.pdf"
            }),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU", {
                "a": "notepad", "b": "calc", "c": "mspaint", "d": "winword", "e": "excel"
            }),
            (r"Software\Microsoft\DirectX", {"Version": "4.09.00.0904"}),
            (r"Software\Microsoft\Windows\CurrentVersion\Uninstall", {
                "Steam": "Steam Client",
                "Discord": "Discord",
                "Chrome": "Google Chrome",
                "VSCode": "Visual Studio Code",
                "Spotify": "Spotify Music"
            }),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.exe", {
                "0": "steam.exe", "1": "discord.exe", "2": "chrome.exe", "3": "code.exe"
            }),
            (r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store", {
                "C:\\Program Files (x86)\\Steam\\steam.exe": "19H2STEAM",
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe": "19H2FF",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe": "19H2CHROME"
            }),
            (r"Software\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage\AppSwitched", {
                "Steam.exe": "3",
                "Discord.exe": "2",
                "Chrome.exe": "5",
                "Code.exe": "1"
            })
        ]

        for subkey_path, values in fake_entries:
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, subkey_path)
                for name, data in values.items():
                    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, data)
                winreg.CloseKey(key)
            except:
                pass

    def clean_python_traces(self):
        self.log("Removing execution traces...")
        try:
            
            history_path = os.path.join(os.environ['USERPROFILE'], '.python_history')
            if os.path.exists(history_path):
                os.remove(history_path)
                
            self.log("Cleaning recycle bin...")
            os.system('rd /s /q %systemdrive%\$Recycle.bin')
            
            exe_name = os.path.basename(sys.executable).upper()
            prefetch_dir = os.path.join(os.environ['SYSTEMROOT'], 'Prefetch')
            if os.path.exists(prefetch_dir):
                for file in os.listdir(prefetch_dir):
                    if exe_name in file.upper():
                        try:
                            os.remove(os.path.join(prefetch_dir, file))
                        except:
                            pass
            
            run_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU", 0, winreg.KEY_ALL_ACCESS)
            try:
                i = 0
                while True:
                    name, value, _ = winreg.EnumValue(run_key, i)
                    if exe_name in value.upper():
                        winreg.DeleteValue(run_key, name)
                    i += 1
            except:
                pass
            winreg.CloseKey(run_key)

            os.system('pip cache purge')
            
            for root, dirs, files in os.walk(os.environ['USERPROFILE']):
                if '__pycache__' in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, '__pycache__'))
                    except:
                        pass

            python_keys = [
                r"Software\Python",
                r"Software\Classes\Python.File",
                r"Software\Classes\Python.CompiledFile",
                r"Software\Classes\Python.NoConFile",
                r"Software\Classes\.py",
                r"Software\Classes\.pyc",
                r"Software\Classes\.pyo",
                r"Software\Classes\.pyw",
            ]
            
            for key in python_keys:
                try:
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key)
                except:
                    pass

        except Exception as e:
            self.log(f"Error cleaning Python traces: {str(e)}")

    def create_extensive_fake_entries(self):
        self.log("Creating extensive system activity traces...")
        common_paths = [
            "C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\EXCEL.EXE",
            "C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.EXE",
            "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
            "C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe",
            "C:\\Windows\\System32\\notepad.exe",
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files\\Internet Explorer\\iexplore.exe",
            "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "C:\\Windows\\System32\\calc.exe",
            "C:\\Windows\\System32\\mspaint.exe",
            "C:\\Program Files\\Windows Media Player\\wmplayer.exe"
        ]

        timestamps = []
        current_time = time.time()
        for i in range(50):  
            timestamps.append(current_time - random.randint(0, 30*24*60*60))

        mru_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")
        for i, path in enumerate(common_paths):
            try:
                winreg.SetValueEx(mru_key, chr(97 + i), 0, winreg.REG_SZ, path)
            except:
                pass

        typed_paths = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths")
        common_folders = [
            "C:\\Users\\User\\Documents",
            "C:\\Users\\User\\Downloads",
            "C:\\Users\\User\\Pictures",
            "C:\\Program Files",
            "C:\\Windows\\System32"
        ]
        for i, path in enumerate(common_folders):
            try:
                winreg.SetValueEx(typed_paths, f"url{i+1}", 0, winreg.REG_SZ, path)
            except:
                pass

        uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
        programs = {
            "Office365": "Microsoft Office 365",
            "Chrome": "Google Chrome",
            "Firefox": "Mozilla Firefox",
            "VLC": "VLC media player",
            "Adobe": "Adobe Acrobat Reader DC",
            "WinRAR": "WinRAR archiver",
            "Notepad++": "Notepad++ text editor",
            "7-Zip": "7-Zip File Manager",
            "CCleaner": "CCleaner",
            "Spotify": "Spotify Music",
            "Steam": "Steam Client",
            "uTorrent": "µTorrent",
            "Skype": "Skype",
            "Teams": "Microsoft Teams"
        }
        
        for prog_id, prog_name in programs.items():
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"{uninstall_key}\\{prog_id}")
                winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, prog_name)
                winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, "20230401")
                winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Microsoft Corporation" if "Microsoft" in prog_name else "Various Publishers")
                winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, f"{random.randint(1,10)}.{random.randint(0,9)}.{random.randint(0,9)}")
            except:
                pass

    def clean_all(self):
        try:
            self.clean_temp_files()
            self.clean_registry()
            self.clean_recent_files()
            self.clean_prefetch()
            self.clean_downloads_history()
            self.clean_power_history()
            self.clean_event_logs()
            self.clean_python_traces()
            self.create_extensive_fake_entries()
            self.log("Cleanup completed successfully!")
            self.self_clean()
        except Exception as e:
            self.log(f"Error during cleanup: {str(e)}")
        finally:
            self.launch_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CleanerPanel()
    window.show()

    sys.exit(app.exec())
