# 📄 PARCOM System Desktop Application

Modern desktop application for parsing technical drawings and validating materials against BOM and Order Manager Excel files.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Features

- 📋 **Parse PDF technical drawings** - Extract components and materials automatically
- ✅ **BOM validation** - Validate against Excel BOM files (Foglio 1-14)
- 🔍 **Material comparison** - Smart material matching with Order Manager
- 💾 **Excel export** - Export results with customizable columns
- 📌 **File pinning** - Pin BOM and Manager files for reuse
- 📊 **Parsing history** - Track all parsing operations
- 🎨 **Modern UI** - Dark/Light theme support

## 🚀 Quick Start (Windows)

### For End Users (Windows 11)

1. **Download the latest release**
   - Go to [Releases](https://github.com/ba-mirza/parcom-system/releases)
   - Download `ParCom_System_Windows.zip`

2. **Extract and Run**
   - Extract the ZIP file to any folder
   - Double-click `ParCom_System.exe`
   - No Python installation required!

3. **Configure**
   - Go to Settings page
   - Enter API endpoint: `https://your-api-endpoint.com`
   - Click "Test Connection"

4. **Start Parsing**
   - Select PDF file
   - Pin your BOM and Manager Excel files
   - Choose BOM sheet (Foglio 1-14)
   - Click "Parse Documents"

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- pip

### Installation
```bash
# Clone the repository
git clone https://github.com/ba-mirza/parcom-system.git
cd parcom-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Building Executable
```bash
# Install build dependencies
pip install -r requirements.txt

# Build Windows executable
python build.py

# Output: dist/ParCom_System.exe
```

## 📦 Project Structure
```
parcom-system/
├── main.py                 # Entry point
├── theme.py               # Theme configuration
├── api/
│   ├── __init__.py
│   └── client.py         # API client
├── ui/
│   ├── __init__.py
│   ├── main_window.py    # Main window
│   ├── home_page.py      # Home page
│   ├── results_page.py   # Results page
│   ├── history_page.py   # History page
│   ├── settings_page.py  # Settings page
│   └── components/       # UI components
│       ├── file_picker.py
│       ├── stats_widget.py
│       └── results_table.py
├── utils/
│   ├── __init__.py
│   ├── config_manager.py  # Configuration
│   └── history_manager.py # History tracking
├── requirements.txt       # Python dependencies
├── build.py              # Build script
└── README.md            # This file
```

## 🔧 Configuration

The application stores configuration in `config.json`:
```json
{
  "api_endpoint": "http://localhost:8000",
  "pinned_files": {
    "bom_excel": "/path/to/BOM.xlsx",
    "manager_excel": "/path/to/order-manager.xlsx"
  },
  "last_bom_sheet_index": 0
}
```

## 📝 Usage

### 1. Pin Excel Files (One-time setup)
- Upload BOM Excel file
- Click "📌 Pin" to save it
- Upload Manager Excel file
- Click "📌 Pin" to save it

### 2. Parse Documents
- Select PDF drawing file
- Choose correct BOM sheet (Foglio 1-14)
- Click "Parse Documents"
- Wait for processing

### 3. Review Results
- Automatically switches to Results page
- View statistics (Equal/Not Equal/New)
- Double-click rows to change status
- Check Material (PDF), Material (BOM), Material (Order) columns

### 4. Export to Excel
- Select columns to export
- Click "Export to Excel"
- Choose save location
- Open the generated Excel file

## 🎨 Themes

The application supports Dark and Light themes:
- Go to Settings → Appearance → Theme
- Choose: Dark / Light / System

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🐛 Bug Reports

If you encounter any issues, please report them on the [Issues](https://github.com/ba-mirza/parcom-system/issues) page.

**Developed by today.development using Python & CustomTkinter**
