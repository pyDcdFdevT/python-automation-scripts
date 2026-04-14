# 📊 CSV Processor

Simple CLI tool to clean CSV files and generate basic statistics.

---

## 🚀 Features

* Removes fully empty rows
* Detects numeric columns automatically
* Calculates:

  * Count
  * Min
  * Max
  * Average
* Generates:

  * Cleaned CSV file
  * Summary report (.txt)

---

## 🧠 How it works

1. Reads input CSV
2. Cleans empty rows
3. Extracts numeric values
4. Computes statistics
5. Outputs results to `/output`

---

## ⚙️ Usage

```bash
python csv_processor.py input.csv
```

Custom output directory:

```bash
python csv_processor.py input.csv --output-dir results
```

---

## 📊 Example

**Input:**

```
name,age,salary
Alice,30,50000
Bob,,
Charlie,25,60000
```

**Output:**

* Cleaned CSV → removes empty rows
* Summary → calculates statistics for numeric columns

See `/examples` folder for full working example.

---

## 📂 Output

```
output/
├── data_cleaned.csv
└── data_summary.txt
```

---

## 🛠️ Tech

* Python 3
* Standard Library only (no dependencies)

---

## 📌 Notes

* Non-numeric values are ignored in statistics
* Input file must be `.csv`

---

## 👨‍💻 Author

Diego
