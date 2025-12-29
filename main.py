from src.database.db_manager import init_db

def main():
    init_db()
    print("Fitness database geinitialiseerd")
    
if __name__ == "__main__":
    main()