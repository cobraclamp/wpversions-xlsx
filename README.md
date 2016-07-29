# wpversions-xlsx
Scans a list of domains to determine WordPress version number.

### FEATURES
- Uses domains in a .txt to scan
- Determines current stable release
- Calculates difference in days between releases
- Sorts the list and saves in colour coded xlsx

### INSTALL

Requires:
- Python >= 2.7
- openpyxl>=2.3.5
- lxml>=2.9.2
- beautifulsoup4
- requests

#### Installing
    git clone https://github.com/cobraclamp/wpversions-xlsx.git
    cd wpversions-xlsx
    touch sites.txt

*touch not required, you may pass domain file as arg

### USAGE

`python wpversions.py`

    -- domains  | -d <domains list> Path to file containing list of domains

#### Examples

`python wpversions.py -d sites.txt`

## TO DO

-[ ] add argument for destination xlsx
