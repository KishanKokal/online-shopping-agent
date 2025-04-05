# Online Shopping Agent

## Project Structure

- `server/` - Python Django backend
- `client/` - React frontend

## Server Setup

### 1. Create a Virtual Environment

There are multiple ways to create a Python virtual environment:

#### Using `uv` (Recommended for macOS/Linux)
```bash
uv venv --python 3.11
```

#### Alternative Method
- Using `venv` (Built-in Python module):
  ```bash
  python -m venv .venv
  ```

### 2. Activate the Virtual Environment

#### On Windows:
```bash
.venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
cd server

# Using uv pip (faster)
uv pip install -r requirements.txt

# OR using regular pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Configure Environment Variables

1. Navigate to the `server` directory
2. Create a new `.env` file
3. Copy the contents from `.env.example` to `.env`
4. Replace the placeholder values with your actual API keys:
   ```
   OPENAI_API_KEY=your_actual_api_key
   ```

### 6. Run the Server
```bash
python manage.py runserver
```
The server will start running at `http://localhost:8000`

## Client Setup

### 1. Install Dependencies

Navigate to the client directory and install dependencies using your preferred package manager:

```bash
cd client

# Using pnpm
pnpm install

# OR using npm
npm install

# OR using yarn
yarn install
```

### 2. Run the Development Server

```bash
# Using pnpm
pnpm run dev

# OR using npm
npm run dev

# OR using yarn
yarn dev
```

The client application will start running at `http://localhost:5173`
