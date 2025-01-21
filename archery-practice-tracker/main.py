from utils import log_practice_session, calculate_statistics
from weather_utils import view_current_weather

if __name__ == "__main__":
    while True:
        print("\n--- Archery Practice Tracker ---")
        print("1. Log a new practice session")
        print("2. View practice statistics")
        print("3. View current weather")
        print("4. Quit")
        
        choice = input("Enter your choice (1/2/3/4): ").strip()
        if choice == "1":
            log_practice_session()
        elif choice == "2":
            calculate_statistics()
        elif choice == "3":
            view_current_weather()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")