from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import joblib
import sys
import uvicorn
import pandas as pd

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the trained Isolation Forest model
loaded_model = joblib.load('isolation_forest_model.pkl')

def is_wildfire_possible(latitude: float, longitude: float):
    # Assuming the 'latitude_longitude_data' is already loaded and preprocessed
    input_data = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})
    
    # Predict using the loaded Isolation Forest model
    anomaly_pred = loaded_model.predict(input_data)
    
    return anomaly_pred[0]  # Return the prediction for the input data


@app.get("/wildfire")
def check_wildfire(latitude: float, longitude: float):
    wildfire_possible = is_wildfire_possible(latitude, longitude)

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
