# MoodSync: Emotion-Based YouTube Recommender

Resonate with your mood with MoodSync, an emotion-based YouTube video recommender.

## Overview

MoodSync is a Python application that leverages Deepface and ThreadExecutorPool libraries to detect the user's emotion in real-time. It recommends YouTube videos based on the detected emotion, providing a personalized and engaging content experience.

## Execution Flow

For a detailed execution flow, refer to the Execution Flow Diagram.

![Execution Flow Diagram](https://github.com/AnuragProg/MoodSync/assets/95378716/d309a57f-4ce3-4868-aad6-8ed856dabb5c)

## Project Structure
```bash
├── src
│ ├── data
│ │ ├── models
│ │ │ ├── emotion.py
│ │ │ ├── video.py
│ │ ├── emotion_detector.py
│ │ ├── videos.py
│ │ ├── youtube.py
│ ├── domain
│ │ ├── video_service.py
│ ├── presenter
│ │ ├── init.py
│ │ ├── app.py
│ │ ├── home.py
│ │ ├── request_executor.py
```
## Components

- **Emotion Detector**: Runs on a separate thread to capture frames and detect the user's emotion using Deepface and ThreadExecutorPool.

- **Presenter Layer**: Consists of a UI and a request executor. The UI passes emotion stats to the request executor, which maintains a queue for normalization and ensures smooth UI transitions.

- **Domain Layer - Video Service**: Responsible for querying local SQLite databases for videos based on emotions. If videos are not present, it utilizes the YouTube Data API to fetch relevant content.

## Data Classes

1. **Youtube Client**: Makes calls to YouTube Data API v3, converting received videos into Python classes.
2. **SQLite3 Client**: Performs CRUD operations on the local SQLite database.

## Getting Started

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run `python src/app.py` to launch MoodSync.

## Screenshots

![MoodSync Application](https://github.com/AnuragProg/MoodSync/assets/95378716/5308b89c-0f20-4b08-a4cf-b749f237b69c)

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.



