# NTDS Password Reuse Analyzer

## Overview
This tool analyzes an NTDS.DIT database file to identify password reuse among users. It provides detailed statistics on password reuse, including the number of users affected, the percentage of users with reused passwords, and the potential "blast radius" if a single account is compromised.

The tool is designed for security analysts and system administrators to assess password hygiene within their organization.

---

## Features
- **Password Reuse Detection**: Identifies users sharing the same or similar passwords.
- **Blast Radius Analysis**: Calculates the worst-case and average blast radius of compromised accounts due to password reuse.
- **Detailed Reporting**: Generates a summary of password reuse and lists users sharing the same passwords.
- **Progress Visualization**: Displays a progress bar during analysis (unless in debug mode).
- **Output File Support**: Saves the analysis results to a specified output file.

---

## Usage

### Command-Line Arguments
```bash
python ntds_analyzer.py -f <file_path> [-de] [-o <output_file>]
```

| Argument | Description |
|----------|-------------|
| `-f`, `--file` | Path to the NTDS.DIT database file (required). |
| `-de`, `--debug` | Enable debug mode to display detailed logs during execution. |
| `-o`, `--output` | Specify an output file to save the analysis results. |
| `-h`, `--help` | Show the help message and exit. |

---

## Example

### Basic Usage
```bash
python ntds_analyzer.py -f ntds.dit
```

### Debug Mode
```bash
python ntds_analyzer.py -f ntds.dit -de
```

### Save Results to File
```bash
python ntds_analyzer.py -f ntds.dit -o results.txt
```

---

## Output

### Console Output
1. **Password Reuse Summary**:
   - Total users analyzed.
   - Number and percentage of users with reused passwords.
   - Number of unique reused passwords.

2. **Blast Radius**:
   - Worst-case blast radius (maximum number of users sharing a single password).
   - Average blast radius (average number of additional accounts compromised).

3. **List of Users Sharing Passwords**:
   - A list of password hashes and the users sharing them.

### Progress Bar
If not in debug mode, a progress bar is displayed during the analysis.

### Time Taken
The total time taken for the analysis is displayed at the end.

---

## Notes
- The tool excludes disabled users and users with empty passwords from the analysis.
- For large files, the analysis may take some time to complete.

---

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---
