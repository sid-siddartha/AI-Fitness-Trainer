
# AI Fitness Trainer

AI Fitness Trainer is an intelligent platform designed to help users achieve their fitness goals through personalized workout plans, real-time feedback, and progress tracking. Leveraging advanced AI and computer vision technologies, it ensures users maintain proper form and stay motivated throughout their fitness journey.

## Features

- **Personalized Workout Plans:** AI generates routines based on user goals such as weight loss, muscle building, or endurance improvement.
- **Real-Time Form Correction:** Computer vision analyzes exercise movements and provides instant feedback to improve technique.
- **Voice Command Support:** Control workouts and receive feedback hands-free using voice commands.
- **Progress Tracking:** Monitor your fitness journey and visualize improvements over time.

## Technology Stack

- **Frontend:** React
- **Backend:** Node.js, Express, Flask
- **Database:** MongoDB
- **AI/ML:** Mediapipe, OpenAI API, custom computer vision models

## Installation & Setup

1. **Clone the Repository**
	```bash
	git clone https://github.com/sid-siddartha/ai-fitness-trainer.git
	cd ai-fitness-trainer
	```

2. **Install Frontend Dependencies**
	```bash
	cd Frontend
	npm install
	npm run dev
	```

3. **Start the Python AI Service**
	```bash
	cd ../Backend_flask
	python main.py
	```

4. **Start the Node.js Server**
	```bash
	cd ../Backend_node
	npm install
	node server.js
	```

## Folder Structure

- `Frontend/` - React-based user interface
- `Backend_flask/` - Python AI service for pose estimation and feedback
- `Backend_node/` - Node.js server for user management and data handling

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
