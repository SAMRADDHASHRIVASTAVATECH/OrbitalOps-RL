from client import SpaceMissionClient
from models import SpaceMissionAction

client = SpaceMissionClient(base_url="http://localhost:7860")

reset_response = client.reset(task_id="orbit_stabilization_1")
print(reset_response)

action = SpaceMissionAction(
    category="navigation",
    priority="medium",
    decision="adjust"
)

step_response = client.step(action)
print(step_response)