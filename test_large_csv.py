import requests
import os

BASE_URL = "http://127.0.0.1:8000"
CSV_FILE_PATH = "/home/halfy/Desktop/everything/Project/test_csvs/UNSW-NB15_1.csv"

def test_large_csv_processing():
    print(f"Testing with {CSV_FILE_PATH}")

    # Step 1: Upload CSV
    try:
        with open(CSV_FILE_PATH, "rb") as f:
            files = {"files": (os.path.basename(CSV_FILE_PATH), f, "text/csv")}
            upload_response = requests.post(f"{BASE_URL}/upload-csv/", files=files)
            upload_response.raise_for_status()
            upload_data = upload_response.json()
            session_id = upload_data["session_id"]
            print(f"Uploaded CSV. Session ID: {session_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error during upload: {e}")
        return

    # Step 2: Process Data
    try:
        process_response = requests.post(f"{BASE_URL}/process-data/{session_id}")
        process_response.raise_for_status()
        process_data = process_response.json()
        print("\nProcessing complete. Results:")
        # print(json.dumps(process_data, indent=2)) # Uncomment for full output
        print(f"Session ID: {process_data.get('session_id')}")
        print(f"CSV Metadata: {process_data.get('csv_metadata')}")
        print(f"Cleaning Errors: {process_data.get('cleaning_errors')}")
        print(f"Analysis Results (partial): {list(process_data.get('analysis_results', {}).keys())}")
        print(f"AI Commentary (partial): {process_data.get('ai_commentary')[:100]}...")

    except requests.exceptions.RequestException as e:
        print(f"Error during processing: {e}")
        return

if __name__ == "__main__":
    test_large_csv_processing()
