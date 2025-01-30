# Archery Practice Tracker: Project Narrative
Welcome to the Archery Practice Tracker—a labor of love inspired by my personal connection to the sport of archery. As an archer, I've experienced firsthand how practice sessions can blend together, making it hard to pinpoint progress or identify areas for improvement. Whether you're training for competition, practicing before hunting season, or just enjoying the sport recreationally, tracking your progress can be transformative. That’s where the Evans Archery Practice Tracker comes in—a simple yet powerful tool designed to bring clarity to anyones archery journey.

## The Inspiration
Archery has always held a special place in my heart. There’s something profoundly calming about standing at the line, bow in hand, focused on the target. It’s a sport that demands both mental and physical discipline, and it teaches patience like nothing else. But as any archer knows, improving requires more than just shooting arrow after arrow. It takes reflection and a little bit of data to see where you're excelling and where you might need more work. Over a year and a half ago, my husband and I moved to Provo, and there is a dedicated archery club up Provo Canyon. We joined and have loved every chance to shoot we have gotten outdoors. 

This project was born out of a desire to streamline the process to identify areas of improvement, blending my love for coding with my passion for archery. The goal? To create a user-friendly program that could help archers—myself included—track their practice sessions, evaluate their progress, and stay motivated while being customizable if the shooter was not at the artchery club and wanted stats logged based on their location.

## The Features
The Archery Practice Tracker is a tool for both archery enthusiasts and data lovers alike. Whether you prefer a terminal-based interaction or a more visual graphical user interface, the program offers features designed with flexibility and usability in mind:

- Log Practice Sessions:
Easily record details of your practice, such as date, distance, total arrows shot, hits on target, and accuracy. The program even integrates live weather data to give context to your session—because we all know how wind or temperature can impact performance!

- View Statistics:
Want to see how you’re doing? The program calculates total arrows shot, overall accuracy, consistency scores, and even breaks down your performance by distance. It gives insights into trends over time, so you can celebrate progress and adjust your training plan.

- Visual Insights:
Sometimes numbers aren’t enough. With built-in visualizations, you can plot your accuracy trends over time or view a bar chart of your performance by distance. These visuals bring the data to life and provide a deeper understanding of your progress.

- Export Reports:
Need to share or review your stats later? The program allows you to export your data as JSON or PDF reports. These exports are perfect for tracking long-term progress or even bringing to a coach.

- Weather Integration:
Practicing at the Timpanogos Archery Club or elsewhere? The weather feature provides real-time conditions, helping you account for external factors that could influence your practice. The statistics cover wind so if you see a dip in performance you can determine if it was just an off day or if the weather had any impact. 

## Why I Built This:
This wasn’t just a project—it was personal. Archery taught me patience, focus, and the importance of incremental growth, lessons I wanted to translate into code. The project was also an opportunity to push myself as a developer, tackling challenges like integrating live weather data, managing CSV files, and creating both terminal and graphical interfaces that work seamlessly.

At its core, this tracker is about empowerment. It’s about giving archers a way to understand their progress and take control of their improvement. As someone who’s spent hours at the range, often wondering if I was truly making progress, I wanted a solution that I could trust—and I hope others will too. I built this for my husband and I to use regularly but I also built it in a way I could share it with the archery club. 

The best part is I made it interactive with 2 options. Running main.py will give you all the features through the terminal with a main menu and outputs based on your selections. Running gui.py gives you all the same functionality while using an interface and the only change is it does not display the statistics in on the screen like the terminal but still offers a way to export via JSON or PDF. 

### What I Learned Along the Way:
This project was as much a journey of learning as it was a passion project. Building this program taught me how to balance user needs with technical implementation, how to ensure smooth integration between terminal and GUI interfaces, and the importance of making software intuitive and accessible. I encountered bugs and challenges along the way, but they became opportunities to grow both my technical and problem-solving skills.

README.md file has a breakdown of the project and its uses, installs needed, etc. including function design. 
I had issues with having the test files in a test directory so they are in the main directory. 

### test files:
---------------
test_utils.py (7 tests)
test_visualizations.py (4 tests)
test_weather_inegration.py (8 tests)



