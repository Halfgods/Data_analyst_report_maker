.PHONY: start dev install clean

# Start both backend and frontend
start:
	@echo "🚀 Starting CSV Analysis App..."
	@./start_dev.sh

# Quick development start (assumes dependencies are installed)
dev:
	@echo "🔧 Starting development servers..."
	@source venv/bin/activate && cd app && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
	@cd dataui-main && npm run dev

# Install all dependencies
install:
	@echo "📦 Installing dependencies..."
	@python -m venv venv
	@source venv/bin/activate && pip install -r requirements.txt
	@cd dataui-main && npm install
	@echo "✅ Dependencies installed!"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf venv
	@cd dataui-main && rm -rf node_modules
	@echo "✅ Cleaned up!"

# Help
help:
	@echo "Available commands:"
	@echo "  make start    - Start both backend and frontend (recommended)"
	@echo "  make dev      - Quick start (assumes dependencies installed)"
	@echo "  make install  - Install all dependencies"
	@echo "  make clean    - Clean up dependencies"
	@echo "  make help     - Show this help"
