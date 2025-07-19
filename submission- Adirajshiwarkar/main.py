import os
import json
from ciq import Agent,Workflow
# -------------------------------
# Load meeting transcript
# -------------------------------
input_file = "sample_inputs/meeting1.txt"
with open(input_file, "r", encoding="utf-8") as file:
    transcript = file.read()

# -------------------------------
# Ensure output directory exists
# -------------------------------
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# Define CIQ Agents
# -------------------------------
agents = [
    Agent(
        name="SummarizerAgent",
        type="llm",
        config={
            "model": "gpt-4",
            "prompt": "Summarize the meeting transcript clearly and concisely."
        }
    ),
    Agent(
        name="DecisionExtractorAgent",
        type="llm",
        config={
            "model": "gpt-4",
            "prompt": "Extract key decisions made in the transcript."
        }
    ),
    Agent(
        name="ActionItemAgent",
        type="llm",
        config={
            "model": "gpt-4",
            "prompt": "List action items with owners and deadlines based on this transcript."
        }
    ),
    Agent(
        name="SentimentAnalyzerAgent",
        type="llm",
        config={
            "model": "gpt-4",
            "prompt": "Analyze speaker-wise sentiment from the transcript."
        }
    ),
    Agent(
        name="TopicClassifierAgent",
        type="llm",
        config={
            "model": "gpt-4",
            "prompt": "Classify the main topics discussed in the transcript."
        }
    )
]

# -------------------------------
# Create and run workflow
# -------------------------------
workflow = Workflow(name="MeetingInsightWorkflow", agents=agents)
results = workflow.run(input=transcript)

# -------------------------------
# Format results
# -------------------------------
output = {agent.name: results.get(agent.name, "No result") for agent in agents}

# Print output
print("✅ Output:\n")
print(json.dumps(output, indent=4))

# Save to file
output_path = "outputs/meeting_insights.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f"\n📁 Output saved to: {output_path}")
