from visualizations import plot_accuracy_over_time, plot_accuracy_by_distance
from utils import log_practice_session, calculate_statistics, recommend_distances
from weather_utils import fetch_weather

def view_current_weather():
    """Fetch and display current weather data."""
    try:
        # Default coordinates for Timpanogos Archery Club
        latitude, longitude = "40.2837", "-111.635"
        weather = fetch_weather(latitude, longitude)

        print("\n--- Current Weather ---")
        print(f"Temperature: {weather['temperature']}°F")
        print(f"Wind Speed: {weather['wind_speed']} mph")
        print(f"Precipitation Chance: {weather['precipitation']}%")
        print(f"Forecast: {weather['forecast']}")
    except Exception as e:
        print(f"Error fetching weather data: {e}")

def view_statistics():
    """Fetch and display practice statistics."""
    try:
        stats = calculate_statistics()

        print("\n--- Practice Statistics ---")
        print(f"Total arrows shot: {stats['total_arrows']}")
        print(f"Overall accuracy: {stats['overall_accuracy']:.2f}%")
        print(f"Most practiced distances: {', '.join(map(str, stats['most_practiced_distances']))}")

        print("\nAccuracy Trends by Date:")
        for trend in stats['accuracy_trends']:
            print(f"  {trend['date']}: {trend['accuracy']:.2f}% accuracy")
            print(f"    Weather - Temp: {trend['temperature']:.1f}°F, Wind: {trend['wind_speed']:.1f} mph, Precip: {trend['precipitation']:.1f} mm")

        print("\nPractice Frequency by Distance:")
        for distance, count in stats['practice_frequency'].items():
            print(f"  {distance} yards: {count} sessions")

        print("\nAccuracy by Distance:")
        for distance, details in stats['accuracy_by_distance'].items():
            print(f"  {distance} yards:")
            print(f"    Most Recent Best: {details['most_recent_best'][0]:.2f}% on {details['most_recent_best'][1]}")
            for year, avg in details['average_by_year'].items():
                print(f"    Average for {year}: {avg:.2f}%")

        print(f"\nConsistency score (lower is better): {stats['consistency_score']:.2f}")
    except FileNotFoundError:
        print("Session log file not found. Please log a session first.")
    except RuntimeError as e:
        print(f"Error: {e}")

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
            view_statistics()
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
