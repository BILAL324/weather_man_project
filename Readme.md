## 🌤️ Weather Man — Weather Report Generator (CLI)

You are given weather data files ([download from here](https://drive.google.com/file/d/1nu_ufYsrrXZfcPColXSpPYJB7-xIpkE2/view?usp=drive_link))

Your task is to build a Python application that reads these files and generates **weather reports** based on the user’s input.

---

### 📊 Supported Reports:

#### 1. **Yearly Summary Report**

**For a given year, display:**

* the highest temperature and the day it occurred
* the lowest temperature and the day it occurred
* the most humid day and the humidity level

**Command:**

```bash
weatherman.py /path/to/files-dir -e 2002
```

**Example Output:**

```
Highest: 45C on June 23  
Lowest: 01C on December 22  
Humidity: 95% on August 14
```

---

#### 2. **Monthly Averages Report**

**For a given month, display:**

* the average highest temperature
* the average lowest temperature
* the average mean humidity

**Command:**

```bash
weatherman.py /path/to/files-dir -a 2005/6
```

**Example Output:**

```
Highest Average: 39C  
Lowest Average: 18C  
Average Mean Humidity: 71%
```

---

#### 3. **Daily Temperature Chart (Bars)**

**For a given month, draw two horizontal bar charts in the console:**

* One for the highest temperature (in red)
* One for the lowest temperature (in blue)

**Command:**

```bash
weatherman.py /path/to/files-dir -c 2011/03
```

**Example Output:**

```
March 2011  
01 +++++++++++++++++++++++++ 25C  
01 +++++++++++ 11C  
02 ++++++++++++++++++++++ 22C  
02 ++++++++ 08C
```

---

#### 4. **Multiple Reports at Once**

The user can combine multiple report types in one command.

**Command:**

```bash
weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011
```

---

#### 5. **\[BONUS] Combined Daily Bar Chart**

**For a given month, draw one horizontal bar per day combining both the high and low temperatures.**

**Command:**

```bash
weatherman.py /path/to/files-dir -b 2011/3
```

**Example Output:**

```
March 2011  
01 ++++++++++++++++++++++++++++++++++++ 11C - 25C  
02 ++++++++++++++++++++++++++++++ 08C - 22C
```

---

### 📦 Constraints:

* Use **only the Python standard library** — no third-party packages.
* Follow **PEP-8** coding conventions.
* The application should allow users to **request multiple reports at once**.

---

### 🧱 Your application should have the following components:

1. A **data structure** for holding each weather reading.
2. A **parser** for parsing the files and populating the readings data structure with correct data types.
3. A **data structure** for holding the calculations results.
4. A **module** for computing the calculations given the readings.
5. A **report generator** for creating the reports given the computation results.
6. A `main()` function to assemble everything and run the program.

Stick exactly to the requirements above. Structure your code cleanly and use modular design to make your logic clear and maintainable.