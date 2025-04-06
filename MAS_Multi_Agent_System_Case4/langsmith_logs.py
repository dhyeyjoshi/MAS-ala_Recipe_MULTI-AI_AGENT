import json
from pathlib import Path
from langsmith import Client
import time

# Set up LangSmith client
client = Client(
    api_url="https://api.smith.langchain.com",
    api_key="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"
)

# Fetch and format logs
def get_recent_runs(project_name="pr-sandy-paperwork-72", limit=5):
    runs = client.list_runs(
        project_name=project_name,
        execution_order=1,
        limit=limit
    )

    formatted = []
    for run in runs:
        formatted.append({
            "name": run.name,
            "start_time": run.start_time.isoformat(),
            "end_time": run.end_time.isoformat() if run.end_time else None,
            "latency": (run.end_time - run.start_time).total_seconds() if run.end_time and run.start_time else None,
            "input": run.inputs,
            "output": run.outputs,
            "run_type": run.run_type,
            "status": run.status
        })

    return formatted

# Append only new logs to JSON file
def save_logs_to_file(new_logs, filename="logs/langsmith_logs.json"):
    Path("logs").mkdir(parents=True, exist_ok=True)

    # Load existing logs if any
    if Path(filename).exists():
        with open(filename, "r", encoding="utf-8") as f:
            existing_logs = json.load(f)
    else:
        existing_logs = []

    # Create a set of unique IDs from existing logs to avoid duplicates
    seen = {f"{log['name']}_{log['start_time']}" for log in existing_logs}

    # Add only new logs
    for log in new_logs:
        log_id = f"{log['name']}_{log['start_time']}"
        if log_id not in seen:
            existing_logs.append(log)
            seen.add(log_id)

    # Save combined logs back to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_logs, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(new_logs)} logs fetched, {len(existing_logs)} total saved.")


# Run as script with live polling
if __name__ == "__main__":
    while True:
        logs = get_recent_runs()
        save_logs_to_file(logs)
        time.sleep(5)
