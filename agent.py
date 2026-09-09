from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from environment import WarehouseEnvironment


# --------------------------------------------------
# Load .env from parent notebook folder
# --------------------------------------------------

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


# --------------------------------------------------
# Create Warehouse Environment
# --------------------------------------------------

warehouse = WarehouseEnvironment()


# --------------------------------------------------
# TOOL 1: Observe Warehouse
# --------------------------------------------------

@tool
def observe_warehouse():
    """Observe the current state of the warehouse."""

    return warehouse.get_state()


# --------------------------------------------------
# TOOL 2: Move Robot
# --------------------------------------------------

@tool
def move_robot(direction: str):
    """
    Move the robot one step.

    Valid directions:
    up, down, left, right.
    """

    return warehouse.move(direction)


# --------------------------------------------------
# TOOL 3: Pick Up Package
# --------------------------------------------------

@tool
def pick_package():
    """Pick up the package when the robot is at its location."""

    return warehouse.pick_package()


# --------------------------------------------------
# TOOL 4: Deliver Package
# --------------------------------------------------

@tool
def deliver_package():
    """Deliver the package when the robot is at the destination."""

    return warehouse.deliver_package()


# --------------------------------------------------
# TOOL 5: Check Goal
# --------------------------------------------------

@tool
def check_goal():
    """Check whether the package has been successfully delivered."""

    return warehouse.is_goal_achieved()


# --------------------------------------------------
# Tools available to the agent
# --------------------------------------------------

tools = [
    observe_warehouse,
    move_robot,
    pick_package,
    deliver_package,
    check_goal
]


# --------------------------------------------------
# Create Groq LLM
# --------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# --------------------------------------------------
# System Prompt
# --------------------------------------------------

system_prompt = """
You are a warehouse robot goal-based agent.

Your goal is:

DELIVER THE PACKAGE TO THE DESTINATION.

You have access to the following tools:

1. observe_warehouse
   - Check the current warehouse state.

2. move_robot
   - Move the robot one step.
   - Valid directions are:
     up, down, left, right.

3. pick_package
   - Pick up the package when the robot reaches it.

4. deliver_package
   - Deliver the package when the robot reaches
     the destination.

5. check_goal
   - Check whether the package has been delivered.

Rules:

- Always observe the warehouse before deciding.
- First reach the package.
- Pick up the package.
- Then move toward the destination.
- Deliver the package.
- Check whether the goal has been achieved.
- Continue taking actions until the package is successfully delivered.
- Do not stop before the goal is achieved.
"""


# --------------------------------------------------
# Create Goal-Based Agent
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


# --------------------------------------------------
# Run the Agent
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("🤖 WAREHOUSE GOAL-BASED AGENT")
    print("=" * 60)

    print("\n🎯 Goal:")
    print("Deliver the package to the destination.")

    print("\n🚀 Agent starting...\n")

    # Run the agent
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
Start the warehouse task.

Pick up the package and deliver it
to the destination.

Continue until the goal is achieved.
"""
                }
            ]
        }
    )

    # --------------------------------------------------
    # Display Agent Conversation
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("🤖 AGENT EXECUTION")
    print("=" * 60)

    for message in result["messages"]:

        # Tool calls made by the AI
        if hasattr(message, "tool_calls") and message.tool_calls:

            for tool_call in message.tool_calls:

                print(
                    f"\n🔧 Tool: {tool_call['name']}"
                )

                print(
                    f"   Arguments: {tool_call['args']}"
                )

        # Tool results
        elif message.type == "tool":

            print(
                f"   ↳ Result: {message.content}"
            )

    # --------------------------------------------------
    # Final Response
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("🏁 FINAL AGENT RESPONSE")
    print("=" * 60)

    print(result["messages"][-1].content)

    # --------------------------------------------------
    # Final Warehouse State
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("📦 FINAL WAREHOUSE STATE")
    print("=" * 60)

    final_state = warehouse.get_state()

    print(f"Robot Position     : {final_state['robot_position']}")
    print(f"Package Position   : {final_state['package_position']}")
    print(f"Destination        : {final_state['destination']}")
    print(f"Package Picked     : {final_state['package_picked']}")
    print(f"Delivered          : {final_state['delivered']}")

    # --------------------------------------------------
    # Goal Status
    # --------------------------------------------------

    print("\n" + "=" * 60)

    if warehouse.is_goal_achieved():
        print("🎯 GOAL ACHIEVED! PACKAGE DELIVERED SUCCESSFULLY! 🎉")
    else:
        print("❌ GOAL NOT ACHIEVED")

    print("=" * 60)