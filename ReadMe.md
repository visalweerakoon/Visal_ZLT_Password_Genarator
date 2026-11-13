# Visal ZLT Password Generator v1.0

A desktop application for generating ZLT router passwords using IMEI and MAC address information.

**Made by Visal**

## Features

- Generate Test Password using IMEI.
- Generate Operator Password using IMEI.
- Generate User Password using MAC address.
- Validate IMEI and MAC address inputs.
- Copy generated passwords to the clipboard.
- Export results as TXT or PDF.
- Dark themed graphical user interface.
- Standalone Windows executable.

## Requirements

For running the Python version,

- Windows 10 or Windows 11
- Python 3.10 or later
- Internet connection for the initial requirements installation

The `requirements.bat` file automatically installs the required Python packages and starts the application.

## How to Run

### Method 1: Run using requirements.bat

1. Download or clone this repository.
2. Make sure Python is installed on your computer.
3. Open the downloaded project folder.
4. Double click `requirements.bat`.
5. The script will install the required packages.
6. After installation, it will automatically launch `Visal_ZLT_Password_Genarator_1.0.py`.

You only need to run `requirements.bat` for the initial setup or when dependencies need to be installed again.

### Method 2: Run using run.bat

1. Make sure the requirements have already been installed.
2. Double click `run.bat`.
3. The application will start.

### Method 3: Standalone EXE Application

You can also use the standalone Windows executable:

`Visal_ZLT_Password_Genarator.exe`

1. Download the EXE file.
2. Double click it to launch the application.
3. No separate Python installation or manual package installation is required.

The standalone executable includes the required application dependencies.

## Repository Files

Only the following four files are included in this repository:

| File                                  | Description                                                                       |
| ------------------------------------- | --------------------------------------------------------------------------------- |
| `run.bat`                             | Starts the Python application.                                                    |
| `requirements.bat`                    | Installs the required packages and automatically launches the Python application. |
| `Visal_ZLT_Password_Genarator_1.0.py` | Main Python application source code.                                              |
| `Visal_ZLT_Password_Genarator.exe`    | Standalone Windows executable.                                                    |

## Usage

1. Open the application.
2. Enter a 15-digit IMEI number, a MAC address, or both.
3. Click **GENERATE PASSWORDS**.
4. View the generated Test, Operator, and User passwords.
5. Use the **COPY** buttons to copy individual passwords.
6. Select TXT or PDF to export the results.
7. Click **DOWNLOAD** to save the generated results.

## Important Notes

- IMEI must contain exactly 15 numeric digits.
- MAC address must contain exactly 12 hexadecimal characters. Separators such as `:` and `-` are accepted.
- You can enter either an IMEI, a MAC address, or both.
- The standalone EXE is intended for Windows.

## Developer

**Made by Visal Weerakoon**

