.PHONY: help install run analysis report slide clean lint format test all

# Default target
help:
	@echo "Available targets:"
	@echo "  make install    - Install dependencies using uv"
	@echo "  make run        - Run the complete analysis pipeline"
	@echo "  make analysis   - Run analysis only (no report compilation)"
	@echo "  make report     - Compile LaTeX report to PDF"
	@echo "  make slide      - Compile Beamer presentation to PDF"
	@echo "  make all        - Run analysis and compile report & slides"
	@echo "  make clean      - Remove generated files (output/, LaTeX aux files)"
	@echo "  make lint       - Run code linting with ruff"
	@echo "  make format     - Format code with ruff"
	@echo "  make test       - Run tests (if available)"

# Install dependencies
install:
	@echo "📦 Installing dependencies with uv..."
	uv sync

# Run the complete analysis pipeline
run: analysis

# Run analysis only
analysis:
	@echo "⚡ Running financial analysis pipeline..."
	uv run python main.py

# Compile LaTeX report
report:
	@echo "📄 Compiling LaTeX report..."
	cd docs && xelatex -interaction=nonstopmode report.tex
	@echo "🔄 Running second pass for cross-references..."
	cd docs && xelatex -interaction=nonstopmode report.tex
	@echo "✅ Report compiled: docs/report.pdf"

# Compile Beamer slides
slide:
	@echo "📊 Compiling Beamer presentation..."
	cd docs && xelatex -interaction=nonstopmode slide.tex
	@echo "🔄 Running second pass for table of contents..."
	cd docs && xelatex -interaction=nonstopmode slide.tex
	@echo "✅ Slides compiled: docs/slide.pdf"

# Run everything
all: analysis report slide
	@echo "✅ Complete pipeline finished!"
	@echo "📊 Results: output/tables/ and output/images/"
	@echo "📄 Report: docs/report.pdf"
	@echo "📊 Slides: docs/slide.pdf"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf output/tables/*.tex output/images/*.png
	rm -f docs/*.aux docs/*.log docs/*.out docs/*.fls docs/*.fdb_latexmk docs/*.synctex.gz docs/*.xdv docs/*.nav docs/*.snm docs/*.toc
	@echo "✅ Cleaned (kept docs/report.pdf and docs/slide.pdf)"

# Deep clean (including PDFs)
clean-all: clean
	rm -f docs/report.pdf docs/slide.pdf
	@echo "✅ Deep clean complete"

# Lint code
lint:
	@echo "🔍 Running ruff linter..."
	uv run ruff check .

# Format code
format:
	@echo "🎨 Formatting code with ruff..."
	uv run ruff format .
	uv run ruff check --fix .

# Run tests (placeholder)
test:
	@echo "🧪 Running tests..."
	uv run pytest

# Development workflow
dev: format lint analysis
	@echo "✅ Development checks passed!"
