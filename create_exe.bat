set name="Property Tracker"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole run_property_tracker.py
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"

set name="Analyze Properties"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole --noconsole run_analyses.py
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"

set name="Refresh Listings & Analyses"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole --noconsole run_refresh_listings_and_analyses.py
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"

set name="Print Single Property Analysis"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole --noconsole run_single_property_analysis_print_only.py
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"