<center><h1>Project Title: WealthWise Portfolio Tracker</h1></center>

* <h3>Project Overview:</h3>
<p>The WealthWise Portfolio Tracker is a simple backend service that allows users to
  record buy/sell transactions and automatically update their investment holdings.
  Using mock market prices, the system calculates each user’s total portfolio value,
  daily gains/losses, and overall returns. Built with FastAPI and PostgreSQL,
  it provides clean and efficient APIs for managing transactions, holdings,
  and portfolio summaries.</p>

  * <h3> Tech Stack:</h3>
    <pre>
    * FastAPI
    * PostgreSQL
    * SQLAlchemy (text queries)
    * Uvicorn
    * Python
    </pre>

  * <h3> Setup Instruction:</h3>
  1. Python Environment:
     - 1. Make Sure using python 3.10+ is installed
       2. Create and activate virtual environment
          <pre>
            # Create virtual environment
              python -m venv myenv
              
            # Activate (macOS / Linux)
              source myenv/bin/activate
              
            # Activate (Windows)
              myenv\Scripts\activate
              </pre>

       3. Install Python Dependencies
          <pre>
            pip install -r requirements.txt
          </pre>
  2. Database Initialization (PostgreSQL)
     - 1. Start PostgreSQL on your system
       2. Create a new database
          <pre>
            CREATE DATABASE portfolio;
          </pre>
       3. Set the database url in .env file
          <pre>
            DATABASE_URL=postgresql://postgres:your_password@localhost:5432/portfolio
          </pre>
  3. Run the Application
      1. Run the Application (main.py)
          <pre>
            uvicorn main:app --reload
          </pre>
* <h3>Folder Structure</h3>
<pre>
  /wealthwise_portfolio_project
│── main.py
│── requirements.txt
│── setup.sql
│── .env .example
│── app/
     ├── database.py
     ├── routers/
     ├── schemas/

</pre>

* <h3>Example API Calls </h3>
1. Add a User
   - 1. URL [/users/]
        <pre>
          {
            "name": "Sahil Jahagirdar",
            "email": "sahil@example.com"
          }
        </pre>
     2. API Response

        <img width="915" height="122" alt="Screenshot 2025-11-22 at 19 12 30" src="https://github.com/user-attachments/assets/28f6d490-8fd1-4ee9-bcd3-2473688c007a" />
2. BUY/SELL Transaction
   - 1. URL [/transactions/]
        <pre>
          {
            "user_id": 1,
            "symbol": "TCS",
            "type": "BUY",
            "units": 10,
            "price": 3200,
            "date": "2025-11-21"
          }
        </pre>
    2. API Response
       <img width="1384" height="193" alt="Screenshot 2025-11-22 at 19 24 58" src="https://github.com/user-attachments/assets/0375a605-79f7-46aa-ae8a-44143b456fe1" />


3. Transaction History
   - 1. URL [/transactions/history?user_id=1]
        <pre>
          "user_id" : 1
        </pre>
     2. API Response
        <img width="1369" height="362" alt="Screenshot 2025-11-22 at 19 20 43" src="https://github.com/user-attachments/assets/7355267e-49f9-4187-bfcb-80e7d8b7f3a1" />


4. Get Portfolio Summary
   - 1. Request URL [/portfolio-summary/?user_id=1]
        <pre>
          "user_id" : 1
        </pre>
     2. Response API
        <img width="1379" height="286" alt="Screenshot 2025-11-22 at 19 23 43" src="https://github.com/user-attachments/assets/06a3bfe6-15c3-42c6-ae10-b063db046bce" />


     3. Calculation Logic:
        <pre>
          Average Cost = (total cost of units bought) / (total units)
          Unrealized P/L = (current_price - avg_cost) * units
          Total Portfolio Value = (units * current_price)

        </pre>

* <h3>Database Schema:</h3>
<img width="1125" height="408" alt="Schema" src="https://github.com/user-attachments/assets/b55c54e7-4ec2-4fa7-99de-7d0bdf14b677" />



