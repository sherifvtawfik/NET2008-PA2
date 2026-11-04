\# NET2008 Practical Assessment 2



\*\*Student Name:\*\* Sherif Tawfik

\*\*Student ID:\*\* 041268020



\## Project Description

This project is a Python network compliance auditor.



The program reads network devices from an XML inventory, checks them against a YAML policy, and generates a JSON report.



\## Requirements

\- Python 3

\- PyYAML



\## Installation

python -m pip install PyYAML



\## Usage

python pa2.py PA2\_sample1.xml PA2\_policy.yaml



\## Output

The program generates audit.json containing:

\- Total devices

\- Skipped devices

\- Device roles

\- Interface counts

\- Compliance violations

\- Compliant devices



\## Error Handling

The program handles missing command-line arguments, missing input files, and invalid XML or YAML data.





\## Testing



I tested the program using the provided XML inventory and YAML policy.



\### Successful Audit

Command:

python pa2.py PA2\_sample1.xml PA2\_policy.yaml



Result:

\- 5 valid devices

\- 1 skipped device

\- 4 compliance violations

\- audit.json generated successfully



\### Missing Arguments

Command:

python pa2.py



Result:

The program displays a usage message and exits with code 2.



\### Missing XML File

Command:

python pa2.py missing.xml PA2\_policy.yaml



Result:

The program displays an error message and exits with code 1.





\## How OS Version Comparison Works



The auditor compares operating system versions by splitting them into numeric components.



For example, version 15.10 becomes (15, 10), while version 15.2 becomes (15, 2).



This is important because software versions should not be compared as decimal numbers.



The program checks whether each device's OS version meets the minimum version specified in the YAML policy.





