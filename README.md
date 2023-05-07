# Django Chat App

Custom chat application built with Django channel that allow user to create chat room and share chat link with other user to exchange messages in real-time

## Prerequisites

To run this project, you will need the following installed on your system:

- Python
- Django
- Channels
- Redis Server
- DRF

## Getting Started

1. Clone the repository to your local machine
2. Open your terminal and navigate to the project directory
3. Create a virtual environment and activate it:
```
python3 -m venv env
source env/bin/activate
```
4. Install the project dependencies:
```
pip install -r requirements.txt
```
5. Start the Redis server:
```
redis-server
```
6. Run the Django migrations command:
```
python manage.py migrate
```
7. Run the Django development server:
```
python manage.py runserver
```
8. Open your browser and go to http://localhost:8000 to view the application

## Demo loom video

https://www.loom.com/share/3724ccac565f4325bd7d7b9e8b6e00c6
