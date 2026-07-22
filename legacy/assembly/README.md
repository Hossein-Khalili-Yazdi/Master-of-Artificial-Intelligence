# 🛒 Store Sales Management System (x86 Assembly)

A legacy console-based **Store Sales Management System** written in **8086 Assembly Language** using the `io.h` macro library for DOS environments.

This program allows users to manage and record daily sales data for various products, retrieve specific sales entries, display all stored records, and calculate statistical insights such as the top-selling day and product.

---

## 📌 Features

1. **Record Sales Data**: Input product code, day, and total sales amount into a 2D array representation.
2. **Search Sales Record**: Retrieve and display sales information based on specific product code and day.
3. **Display All Records**: Print all formatted sales records stored in memory.
4. **Best Sales Day Analytics**: Calculates and identifies the day with the highest total sales.
5. **Top-Selling Product Analytics**: Finds and displays the product code with maximum sales.
6. **Interactive Menu**: User-friendly text menu with seamless options switching and input prompts.

---
## 🛠️ Technical Details & Architecture

Here are the primary specs of the project:

- **Architecture:** x86 Assembly (16-bit real mode / DOS)
- **Data Structures:** 1D Array mapped to simulate a 2D matrix
- **I/O Library:** Uses standard `io.h` macros (`output`, `inputs`, `atoi`, `itoa`)

  
## ⚙️ How to Run & Compile
To compile and run this 16-bit Assembly project on modern operating systems, you need a DOS Emulator (such as **DOSBox**) and an Assembler like **TASM** (Turbo Assembler) or **MASM**.
Prerequisites
- Download and install DOSBox.
- Get **TASM** (Turbo Assembler) or **MASM 6.11**.
- Ensure `io.h` is present in the same directory as the `.asm` file.
Compilation Steps (using TASM in DOSBox)
```
# 1. Mount your workspace folder in DOSBox
mount c C:\path\to\project
c:

# 2. Assemble the source code
tasm store_sales.asm

# 3. Link the object file
tlink store_sales.obj

# 4. Run the executable
store_sales.exe
```
## 🖥️ Menu Interface
```text
1. daryaft kod kala va rooz va mizane froush
2. daryaft kod kala va rooz va namaesh froush
3. namayesh hameye etelaat
4. namayesh porfroushtarin rooz
5. namayesh porfroushtarin kala
6. exit

Please Choose your Number:
```
## 📜 License
This project is open-source and available under the MIT License.
