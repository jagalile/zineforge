# ZineForge

ZineForge is an open-source tool that converts sequential A5 PDFs into A4 landscape format with proper booklet imposition (zine layout). Perfect for creating print-ready zines, booklets, and mini-magazines that can be folded and saddle-stitched.

Perfect for solo RPG creators, fanzine artists, and anyone who loves DIY print media.

## ✂️ What it does

- Takes a sequential A5 PDF as input
- Converts it to A4 landscape format with proper page imposition
- Automatically calculates page ordering for booklet printing
- Handles documents with any number of pages (adds blank pages as needed)
- **Adds a folding guide line** on the first sheet to help with precise folding
- Generates output ready for duplex printing, folding, and saddle-stitching

## 🧰 Basic usage

```bash
python zineforge.py input.pdf
```

This will generate `zine_listo_para_imprimir.pdf` ready to print as a folded zine/booklet.

You can also specify custom parameters:

```bash
python zineforge.py input.pdf -o output.pdf --fill-position before_last
```

## 📋 Command line options

### Required Arguments
- `input_file` - Path to the input PDF file (sequential A5 format)

### Optional Arguments
- `-o, --output` - Output PDF file path (default: `zine_listo_para_imprimir.pdf`)
- `-f, --fill-position` - Where to insert blank pages when needed:
  - `end` (default) - Add blank pages at the end
  - `before_last` - Add blank pages before the last page

### Usage Examples

```bash
# Basic usage with default output
python zineforge.py my_zine.pdf

# Specify output file
python zineforge.py my_zine.pdf -o ready_to_print.pdf

# Control blank page placement
python zineforge.py my_zine.pdf --fill-position before_last
```

## 💡 How it works

ZineForge uses sophisticated page imposition logic:

1. **Calculates required pages**: Rounds up to the nearest multiple of 4 pages
2. **Adds blank pages**: Inserts blank pages where needed based on `--fill-position`
3. **Applies imposition**: Reorders pages for proper booklet layout
4. **Creates A4 landscape**: Places two A5 pages side-by-side on each A4 sheet
5. **Adds folding guide**: Draws a dashed line down the center of the first sheet

### Example: 6-page input becomes 8-page booklet
- Original: Pages 1, 2, 3, 4, 5, 6
- With `--fill-position end`: 1, 2, 3, 4, 5, 6, BLANK, BLANK
- With `--fill-position before_last`: 1, 2, 3, 4, 5, BLANK, BLANK, 6

The output A4 sheets will be arranged so that when printed duplex, folded, and stapled, the pages read in correct order.

## ✨ Features

- **Smart page imposition**: Automatically calculates the correct page order for booklet binding
- **Flexible blank page handling**: Choose where blank pages are inserted when padding is needed
- **Folding guide**: A dashed line on the first sheet shows exactly where to fold
- **Verbose output**: Clear console feedback showing page placement and processing status
- **Error handling**: Informative error messages for common issues

## 🔧 Requirements

- Python 3.6+
- PyMuPDF (fitz) library

Install dependencies:
```bash
pip install PyMuPDF
```

## 🌈 Perfect for

- Designers and artists making zines or mini-books
- RPG creators releasing indie game supplements  
- Publishers creating booklets and pamphlets
- Anyone who loves paper, print, and DIY culture
- Converting digital content to physical booklet format

## 🖨️ Printing Instructions

1. Print the output PDF on A4 paper
2. Use duplex/double-sided printing (flip on long edge)
3. Use the dashed guide line on the first sheet to fold precisely
4. Fold all printed sheets in half along the center line
5. Saddle-stitch (staple) along the fold line
6. Trim edges if desired for a professional finish

## 📐 Technical Details

- **Input format**: Sequential A5 PDF pages
- **Output format**: A4 landscape with 2-up imposition
- **Page calculation**: Automatically rounds up to multiples of 4 pages
- **Folding guide**: 0.5pt dashed line in black on the first sheet center
- **Dimensions**: A4 landscape (842×595 points), A5 equivalent (421×595 points per page)

## 🧷 Project status

ZineForge is under active development.
Contributions, ideas, and PRs are very welcome 💌

## 📜 License

MIT License
