# F'Prime Calculator

A Python-based function calculator with a modern GUI interface for calculating derivatives, integrals, and visualizing mathematical functions.

## Features

- First derivative calculation
- Nth derivative calculation
- Indefinite integration
- Definite integration
- Real-time function plotting
- Interactive graph visualization
- Support for common mathematical functions and operations

## Installation

1. Download the latest release from the releases page
2. Extract the zip file
3. Run `FPrime_Calculator.exe`

## Development Setup

If you want to run from source:

1. Clone the repository
```bash
git clone https://github.com/markvncent/f-prime_calculator.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python build/gui.py
```

## Building from Source

To create an executable:

1. Install PyInstaller
```bash
pip install pyinstaller
```

2. Build the executable
```bash
cd build
pyinstaller --name "FPrime_Calculator" --windowed --icon=icon.ico --add-data "assets;assets" gui.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 