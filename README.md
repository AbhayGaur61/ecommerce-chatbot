# E-Commerce Chatbot

A modern, full-stack chatbot application for e-commerce support. This project provides a web-based chatbot that can answer questions about top-selling products, order statuses, and inventory stock levels, using data from CSV files. It is built with a Python Flask backend and two frontend options: a simple HTML/CSS/JavaScript frontend and an alternative React frontend (with Vite).

---

## 🚀 Features
- **Top Products Query:** Find the most sold products
- **Order Status Tracking:** Check the status of any order by ID
- **Stock Level Monitoring:** See current inventory for any product
- **Real-time Chat Interface:** Modern, responsive web UI
- **RESTful API:** Clean endpoints for data retrieval
- **Docker Support:** Easy containerized deployment
- **Two Frontend Options:** Choose between a vanilla JS frontend or a modern React frontend

---

## 🏗️ Architecture
- **Backend:** Python Flask API
- **Frontend:**
  - **Vanilla JS:** HTML, CSS, JavaScript (in `frontend/`)
  - **React:** React + Vite (in `react-frontend/`)
- **Data:** CSV files (products, orders, inventory, users)
- **Containerization:** Dockerfile for backend, Dockerfile for React frontend

---

## 📁 Project Structure
```
ecommerce-chatbot/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend Docker configuration
│   └── data/                  # CSV data files
│       ├── products.csv
│       ├── orders.csv
│       ├── order_items.csv
│       ├── inventory_items.csv
│       ├── users.csv
│       └── distribution_centers.csv
├── frontend/
│   ├── index.html             # Vanilla JS main HTML page
│   ├── script.js              # Vanilla JS frontend logic
│   └── style.css              # Styling
├── react-frontend/
│   ├── src/                   # React source code
│   ├── public/                # Static assets
│   ├── package.json           # React dependencies
│   ├── Dockerfile             # React frontend Docker config
│   └── ...                    # Other React/Vite config files
└── ...
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Node.js & npm (for React frontend)
- Docker (optional)

### Backend (Flask API)
1. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run the backend**
   ```bash
   python app.py
   ```
   The API will be available at [http://localhost:5000](http://localhost:5000)

### Frontend Options

#### 1. Vanilla JS Frontend
- No build step required. Just ensure the backend is running, then open [http://localhost:5000](http://localhost:5000) in your browser. The Flask backend serves the static files from `frontend/`.

#### 2. React Frontend (Vite)
1. **Set up the React frontend**
   ```bash
   cd react-frontend
   npm install
   ```
2. **Run the React development server**
   ```bash
   npm run dev
   ```
   By default, this runs at [http://localhost:5173](http://localhost:5173)
3. **Connect to the backend**
   - Make sure the Flask backend is running on port 5000.
   - The React app will make API requests to the backend (update API URLs in the React code if needed).

#### 3. Docker Deployment
- Both the backend and React frontend have Dockerfiles for containerized deployment. You can build and run them separately, or use a `docker-compose.yml` for orchestration.

---

## 💬 Chatbot Usage
The chatbot understands natural language queries such as:
- "What are the top products?"
- "What's the status of order 12345?"
- "How many iPhones are left in stock?"

---

## 📡 API Endpoints

### 1. Get Top Products
- **GET /top_products**
- Returns the top 5 most sold products
- **Response:**
  ```json
  [
    { "name": "Product Name", "sales_count": 150 }
  ]
  ```

### 2. Get Order Status
- **GET /order_status/<order_id>**
- Returns the status of a specific order
- **Response:**
  ```json
  { "order_id": 12345, "status": "shipped" }
  ```

### 3. Get Stock Level
- **GET /stock_level?product=<product_name>**
- Returns the current stock level for a product
- **Response:**
  ```json
  { "product_name": "Product Name", "stock_level": 25 }
  ```

---

## 🗃️ Data Files
The backend expects the following CSV files in `backend/data/`:
- `products.csv`: Product information
- `orders.csv`: Order details
- `order_items.csv`: Order line items
- `inventory_items.csv`: Inventory tracking
- `users.csv`: User information
- `distribution_centers.csv`: (if used)

**Note:**
- The file `backend/data/inventory_items.csv` is very large (>50MB). If you push this repo to GitHub, use [Git Large File Storage (LFS)](https://git-lfs.github.com/) for large files.

---

## 🎨 Frontend Features
- **Vanilla JS Frontend:**
  - Responsive design (desktop & mobile)
  - Real-time chat with instant responses
  - Auto-scroll to latest message
  - Clean, modern UI
  - Error handling for API issues
- **React Frontend:**
  - Modern React component structure
  - Fast refresh with Vite
  - Easily extensible for new features
  - (See `react-frontend/README.md` for more details)

---

## 🔧 Configuration
- **Environment Variables:**
  - `FLASK_APP=backend/app.py`
  - `FLASK_RUN_HOST=0.0.0.0` (for Docker)
- **Docker Compose (optional):**
  ```yaml
  version: '3.8'
  services:
    backend:
      build: ./backend
      ports:
        - "5000:5000"
      volumes:
        - ./backend/data:/app/backend/data
    react-frontend:
      build: ./react-frontend
      ports:
        - "5173:5173"
  ```

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🆘 Support
If you encounter issues or have questions:
1. Check existing issues
2. Create a new issue with details
3. Include error messages and steps to reproduce

---

