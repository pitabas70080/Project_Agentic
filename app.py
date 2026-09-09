import streamlit as st

from agent import agent, warehouse

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Warehouse Agentic AI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🤖 Warehouse Agentic AI")

st.write(
    "A goal-based AI agent that autonomously "
    "picks up and delivers a package."
)


# --------------------------------------------------
# Goal
# --------------------------------------------------

st.info(
    "🎯 Goal: Pick up the package and deliver it "
    "to the destination."
)


# --------------------------------------------------
# Warehouse Display
# --------------------------------------------------

def display_warehouse():

    # Get the latest warehouse state
    state = warehouse.get_state()

    robot = tuple(state["robot_position"])
    package = tuple(state["package_position"])
    destination = tuple(state["destination"])

    package_picked = state["package_picked"]
    delivered = state["delivered"]

    st.subheader("🏭 Warehouse")

    # -----------------------------------------
    # Warehouse Grid
    # -----------------------------------------

    for row in range(warehouse.rows):

        cols = st.columns(warehouse.cols)

        for col in range(warehouse.cols):

            position = (row, col)

            # Robot at destination with package
            if position == robot and position == destination:

                cell_content = "🤖📦🎯"

            # Robot carrying package
            elif position == robot and package_picked:

                cell_content = "🤖📦"

            # Robot without package
            elif position == robot:

                cell_content = "🤖"

            # Package waiting to be picked
            elif position == package and not package_picked:

                cell_content = "📦"

            # Destination
            elif position == destination:

                cell_content = "🎯"

            # Empty cell
            else:

                cell_content = "⬜"

            cols[col].markdown(
                f"""
                <div style="
                    height: 100px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 1px solid #666;
                    border-radius: 10px;
                    margin: 3px;
                    font-size: 32px;
                ">
                    {cell_content}
                </div>
                """,
                unsafe_allow_html=True
            )

    # -----------------------------------------
    # Current State
    # -----------------------------------------

    st.markdown("---")

    if robot == destination:

        st.success(
            f"🤖 Robot: {robot} — AT DESTINATION 🎯"
        )

    else:

        st.write(
            f"🤖 Robot: {robot}"
        )

    if package_picked:

        st.write(
            "📦 Package: Picked up"
        )

    else:

        st.write(
            f"📦 Package: {package}"
        )

    st.write(
        f"🎯 Destination: {destination}"
    )

    # -----------------------------------------
    # Goal Status
    # -----------------------------------------

    if delivered:

        st.success(
            "🎯 GOAL ACHIEVED — Package delivered successfully! 🎉"
        )


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "activity" not in st.session_state:

    st.session_state.activity = []


# --------------------------------------------------
# Layout
# --------------------------------------------------

left_column, right_column = st.columns([1, 1])


# ==================================================
# LEFT COLUMN
# ==================================================

with left_column:

    display_warehouse()


# ==================================================
# RIGHT COLUMN
# ==================================================

with right_column:

    st.subheader("🤖 Agent Activity")

    # -----------------------------------------
    # Start Agent Button
    # -----------------------------------------

    if st.button(
        "🚀 Start Agent",
        use_container_width=True
    ):

        # Clear previous activity
        st.session_state.activity = []

        # -----------------------------------------
        # Reset warehouse
        # -----------------------------------------

        warehouse.robot_position = (3, 0)
        warehouse.package_picked = False
        warehouse.delivered = False

        # -----------------------------------------
        # Run Agent
        # -----------------------------------------

        with st.spinner("🤖 Agent is working..."):

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": """
                            Pick up the package and deliver it
                            to the destination.

                            Continue until the goal is achieved.
                            """
                        }
                    ]
                }
            )

        # -----------------------------------------
        # Extract Tool Activity
        # -----------------------------------------

        for message in result["messages"]:

            if hasattr(message, "tool_calls") and message.tool_calls:

                for tool_call in message.tool_calls:

                    tool_name = tool_call["name"]

                    arguments = tool_call["args"]

                    st.session_state.activity.append(
                        {
                            "tool": tool_name,
                            "arguments": arguments
                        }
                    )

        # -----------------------------------------
        # IMPORTANT
        # -----------------------------------------
        # Rerun Streamlit so the warehouse grid
        # displays the FINAL warehouse state.

        st.rerun()


    # ==================================================
    # DISPLAY AGENT ACTIVITY
    # ==================================================

    for activity in st.session_state.activity:

        tool_name = activity["tool"]

        arguments = activity["arguments"]

        if tool_name == "observe_warehouse":

            st.write(
                "🔍 Observing warehouse"
            )

        elif tool_name == "move_robot":

            direction = arguments.get(
                "direction",
                ""
            )

            arrows = {
                "up": "⬆️",
                "down": "⬇️",
                "left": "⬅️",
                "right": "➡️"
            }

            st.write(
                f"{arrows.get(direction, '🚶')} "
                f"Moving **{direction}**"
            )

        elif tool_name == "pick_package":

            st.write(
                "📦 Package picked up"
            )

        elif tool_name == "deliver_package":

            st.write(
                "🚚 Package delivered"
            )

        elif tool_name == "check_goal":

            st.write(
                "🎯 Checking goal"
            )


# ==================================================
# FINAL STATUS
# ==================================================

st.divider()

if warehouse.is_goal_achieved():

    st.success(
        "🎯 GOAL ACHIEVED — Package delivered successfully! 🎉"
    )

else:

    st.warning(
        "⏳ Waiting for the agent to complete the task."
    )