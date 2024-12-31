import curses
import threading
import time

# Constants
TOTAL_REINDEER = 9
ELF_GROUP_SIZE = 3

# Shared state
state = {
    "santa": "Sleeping",
    "elves_waiting": 0,
    "reindeer_waiting": 0,
    "tasks": [],
    "running": True,
}

# Mutex for shared state
state_lock = threading.Lock()

# Santa task thread
# Santa task thread
def santa_task():
    """Simulate Santa's behavior."""
    while state["running"]:
        with state_lock:
            reindeer_waiting = state["reindeer_waiting"]
            elves_waiting = state["elves_waiting"]

        # Handle reindeer in groups of 9
        if reindeer_waiting >= TOTAL_REINDEER:
            with state_lock:
                state["santa"] = "Preparing sleigh 🎅🦌"
            time.sleep(3)  # Simulate sleigh preparation
            with state_lock:
                state["reindeer_waiting"] -= TOTAL_REINDEER  # Process only 9 reindeer
                state["tasks"].append("🎅 Sleigh prepared for 9 reindeer!")

        # Handle elves in groups of 3
        elif elves_waiting >= ELF_GROUP_SIZE:
            with state_lock:
                state["santa"] = "Helping elves 🎅🧝"
            time.sleep(2)  # Simulate helping elves
            with state_lock:
                state["elves_waiting"] -= ELF_GROUP_SIZE  # Process only 3 elves
                state["tasks"].append("🎅 Helped 3 elves!")

        # Santa sleeps if no task
        else:
            with state_lock:
                state["santa"] = "Sleeping 😴"

        time.sleep(0.1)  # Prevent busy-waiting

# User input thread
def user_input(stdscr):
    """Handle user input."""
    while state["running"]:
        key = stdscr.getch()
        with state_lock:
            if key == ord("e"):
                state["elves_waiting"] += 1
            elif key == ord("r"):
                state["reindeer_waiting"] += 1
            elif key == ord("q"):
                state["running"] = False

# Terminal display thread
def display(stdscr):
    """Display the simulation."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch() non-blocking
    stdscr.clear()

    # Start Santa's thread
    santa_thread = threading.Thread(target=santa_task, daemon=True)
    santa_thread.start()

    # Start user input thread
    input_thread = threading.Thread(target=user_input, args=(stdscr,), daemon=True)
    input_thread.start()

    while state["running"]:
        with state_lock:
            # Clear screen
            stdscr.clear()

            # Display Santa's state
            stdscr.addstr(1, 2, f"Santa's State: {state['santa']}")

            # Display waiting queues
            stdscr.addstr(3, 2, f"Elves Waiting: {state['elves_waiting']}")
            stdscr.addstr(4, 2, f"Reindeer Waiting: {state['reindeer_waiting']}")

            # Display recent tasks
            stdscr.addstr(6, 2, "Recent Tasks:")
            for i, task in enumerate(state["tasks"][-5:]):  # Show last 5 tasks
                stdscr.addstr(7 + i, 4, task)

            # Display instructions
            stdscr.addstr(13, 2, "Press 'e' to add an Elf 🧝")
            stdscr.addstr(14, 2, "Press 'r' to add a Reindeer 🦌")
            stdscr.addstr(15, 2, "Press 'q' to Quit")

            # Add description of the simulation
            stdscr.addstr(17, 2, "-" * 70)
            stdscr.addstr(
                18, 2,
                "This simulation demonstrates a concurrency problem where Santa "
            )
            stdscr.addstr(
                19, 2,
                "handles tasks based on the number of waiting elves and reindeer. "
            )
            stdscr.addstr(
                20, 2,
                "Santa prioritizes reindeer when all 9 are waiting to prepare the "
            )
            stdscr.addstr(
                21, 2,
                "sleigh. Otherwise, Santa helps groups of 3 elves. This example "
            )
            stdscr.addstr(
                22, 2,
                "models task scheduling and resource sharing in concurrent systems."
            )

            # Refresh screen
            stdscr.refresh()

        time.sleep(0.1)  # Refresh rate

    # Clean up
    stdscr.clear()
    stdscr.addstr(10, 10, "Simulation Ended. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()  # Wait for user to acknowledge

# Run the curses application
curses.wrapper(display)
