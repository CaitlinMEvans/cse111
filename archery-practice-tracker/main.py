from visualizations import plot_accuracy_over_time, plot_accuracy_by_distance

if __name__ == "__main__":
    while True:
        print("\n--- Archery Practice Tracker ---")
        print("1. Log a new practice session")
        print("2. View practice statistics")
        print("3. View current weather")
        print("4. View distance-based recommendations")
        print("5. Plot accuracy over time")
        print("6. Plot accuracy by distance")
        print("7. Quit")

        choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()
        if choice == "1":
            log_practice_session()
        elif choice == "2":
            calculate_statistics()
        elif choice == "3":
            view_current_weather()
        elif choice == "4":
            recommend_distances()
        elif choice == "5":
            export = input("Would you like to export the chart? (y/n): ").strip().lower() == "y"
            plot_accuracy_over_time(export)
        elif choice == "6":
            export = input("Would you like to export the chart? (y/n): ").strip().lower() == "y"
            plot_accuracy_by_distance(export)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")