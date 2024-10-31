- Clone the repository:
   ```bash
   git clone https://github.com/pedro-coelho-dr/event-manager.git
   ```
   ```bash
   cd event-manager
   ```

- Create a virtual environment:   
  
    Linux:
   ```bash
   python3 -m venv venv
   ```
   ```bash
   source venv/bin/activate
   ```
    Windows:
   ```bash
   python -m venv venv
   ```
   ```bash
   .\venv\Scripts\activate
   ```
   If ExecutionPolicy is restricted:
   ```bash
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

- Install dependecies:
   ```bash
   pip install -r requirements.txt
   ```
