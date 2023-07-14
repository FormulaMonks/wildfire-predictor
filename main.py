from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_wildfire_possible(date: str, latitude: float, longitude: float) -> bool:
    # Perform your logic to determine if a wildfire is possible
    # based on the provided date, latitude, and longitude.
    # You can replace this with your own implementation.
    # For demonstration purposes, let's assume wildfires are possible
    # if the month is July, August, or September.

    # Convert the input date string to a datetime object
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    # Extract the month from the date
    month = date_obj.month

    # Check if the month is July, August, or September
    if month in [7, 8, 9]:
        return True
    else:
        return False


@app.get("/wildfire")
def check_wildfire(date: str, latitude: float, longitude: float):
    wildfire_possible = is_wildfire_possible(date, latitude, longitude)

    if wildfire_possible:
        return {"wildfire": "Possible"}
    else:
        return {"wildfire": "Not Possible"}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
