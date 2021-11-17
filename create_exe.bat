@echo off

set name="Property Tracker"
set src="run_property_tracker.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" --distpath ./bin %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Analyze Properties"
set src="run_analyses.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" --distpath ./bin %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Refresh Listings & Analyses"
set src="run_refresh_listings_and_analyses.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" --distpath ./bin %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Print Single Property Analysis"
set src="run_single_property_analysis_print_only.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" --distpath ./bin %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"
