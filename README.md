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

