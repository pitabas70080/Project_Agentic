# environment.py


class WarehouseEnvironment:

    def __init__(self):

        # Warehouse dimensions
        self.rows = 4
        self.cols = 4

        # Initial positions
        self.robot_position = (3, 0)
        self.package_position = (2, 1)
        self.destination = (0, 3)

        # Package status
        self.package_picked = False
        self.delivered = False

    # ------------------------------------------
    # Get current warehouse state
    # ------------------------------------------

    def get_state(self):

        return {
            "robot_position": self.robot_position,
            "package_position": self.package_position,
            "destination": self.destination,
            "package_picked": self.package_picked,
            "delivered": self.delivered
        }

    # ------------------------------------------
    # Move robot
    # ------------------------------------------

    def move(self, direction):

        row, col = self.robot_position

        if direction == "up":
            new_position = (row - 1, col)

        elif direction == "down":
            new_position = (row + 1, col)

        elif direction == "left":
            new_position = (row, col - 1)

        elif direction == "right":
            new_position = (row, col + 1)

        else:
            return "Invalid direction."

        # Check warehouse boundaries
        new_row, new_col = new_position

        if (
            new_row < 0
            or new_row >= self.rows
            or new_col < 0
            or new_col >= self.cols
        ):
            return "Cannot move outside the warehouse."

        # Update robot position
        self.robot_position = new_position

        return f"Robot moved {direction}."

    # ------------------------------------------
    # Pick up package
    # ------------------------------------------

    def pick_package(self):

        if self.package_picked:
            return "Package has already been picked up."

        if self.robot_position != self.package_position:
            return "Robot is not at the package."

        self.package_picked = True

        return "Package picked up successfully."

    # ------------------------------------------
    # Deliver package
    # ------------------------------------------

    def deliver_package(self):

        if not self.package_picked:
            return "Robot has not picked up the package."

        if self.robot_position != self.destination:
            return "Robot is not at the destination."

        self.delivered = True

        return "Package delivered successfully."

    # ------------------------------------------
    # Check whether goal is achieved
    # ------------------------------------------

    def is_goal_achieved(self):

        return self.delivered

# ------------------------------------------
# Test
# ------------------------------------------

if __name__ == "__main__":

    warehouse = WarehouseEnvironment()

    print("Initial State:")
    print(warehouse.get_state())

    print()

    print(warehouse.move("up"))
    print(warehouse.move("right"))

    print()

    print("Current State:")
    print(warehouse.get_state())