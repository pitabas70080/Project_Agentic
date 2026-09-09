import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time


# --------------------------------------------------
# Define the 2x2 environment
# --------------------------------------------------

environment = {
    "Room1": "Clean",
    "Room2": "Dirty",       # Start with dirt here
    "Room3": "Clean",
    "Room4": "Clean"
}


# --------------------------------------------------
# Mapping for grid positions
# --------------------------------------------------

room_positions = {
    "Room1": (0, 1),        # Top-left
    "Room2": (1, 1),        # Top-right
    "Room3": (0, 0),        # Bottom-left
    "Room4": (1, 0)         # Bottom-right
}


rooms = list(environment.keys())

# Agent starts in Room1
agent_index = 0


# --------------------------------------------------
# Reflex Agent
# --------------------------------------------------

def reflex_agent(state):

    if state == "Dirty":
        return "Clean"
    else:
        return "Move"


# --------------------------------------------------
# Function to Draw the Environment
# --------------------------------------------------

def draw_environment(env, agent_pos, step):

    fig, ax = plt.subplots(figsize=(8, 6))

    # Set grid limits
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)

    # Remove axis ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Title
    ax.set_title(
        f"Step {step} — Agent in {rooms[agent_pos]}",
        fontsize=14
    )

    # Draw each room
    for room, pos in room_positions.items():

        x, y = pos

        # Dirty = Red
        # Clean = Green
        color = "red" if env[room] == "Dirty" else "green"

        rect = patches.Rectangle(
            (x, y),
            1,
            1,
            facecolor=color,
            edgecolor="black"
        )

        ax.add_patch(rect)

        # Room name
        ax.text(
            x + 0.5,
            y + 0.5,
            room,
            ha="center",
            va="center",
            fontsize=12,
            color="white"
        )

    # --------------------------------------------------
    # Draw the agent
    # --------------------------------------------------

    agent_room = rooms[agent_pos]

    agent_x, agent_y = room_positions[agent_room]

    agent_patch = patches.Circle(
        (
            agent_x + 0.5,
            agent_y + 0.5
        ),
        0.1,
        facecolor="blue",
        edgecolor="black"
    )

    ax.add_patch(agent_patch)

    # Display for 1 second
    plt.pause(1)

    # Close current figure
    plt.close()


# --------------------------------------------------
# Run Simulation
# --------------------------------------------------

plt.ion()

steps = 8

for step in range(steps):

    # Find current room
    current_room = rooms[agent_index]

    # Get current state
    state = environment[current_room]

    # Ask reflex agent what to do
    action = reflex_agent(state)

    print(
        f"Step {step + 1}: "
        f"{current_room} = {state} → {action}"
    )

    # Perform the action
    if action == "Clean":

        environment[current_room] = "Clean"

    else:

        # Move to next room
        agent_index = (agent_index + 1) % len(rooms)

    # Draw updated environment
    draw_environment(
        environment,
        agent_index,
        step + 1
    )

    # Small delay
    time.sleep(0.5)


# Turn interactive mode off
plt.ioff()

print("✔ Simulation complete!")