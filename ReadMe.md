# Battery Monitor

## Installation

Run the following command in your terminal to install all required libraries:

```sh
pip install psutil
pip install pygame
pip install plyer
```

Alternatively, install all dependencies in one command:

```sh
pip install psutil pygame plyer
```

Ensure you're using Python 3.6 or later. You can check your Python version with:

```sh
python --version
```

PyInstaller is the primary tool used for creating executables. Install it with:

```sh
pip install pyinstaller
```

Additionally, `win10toast` may be required for Windows notifications. Install it with:

```sh
pip install win10toast
```

## Project Structure

Ensure your folder looks like this:

```
/your_project_folder
├── battery_monitor.py
├── warning.wav
├── battery_icon.ico
```

## Creating an Executable

Run the following command to generate the `.exe` file:

```sh
pyinstaller --onefile --windowed --add-data "warning.wav;." --icon=battery_icon.ico --hidden-import=plyer.platforms.win.notification --hidden-import=win10toast battery_monitor.py
```

After PyInstaller completes, you'll find the `.exe` file in the `dist` folder:

```
/your_project_folder
├── dist/
│   └── battery_monitor.exe
├── build/
├── battery_monitor.spec
```

### Linux/macOS Users
If you're on Linux or macOS, adjust the `--add-data` syntax to use `:` instead of `;`:

```sh
--add-data "warning.wav:."
```

