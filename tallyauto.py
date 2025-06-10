import os
import time
import subprocess
import pyautogui
from datetime import datetime

def automate_tally_balance_sheet_export():
    """
    Launches TallyPrime, enters education mode, opens the specified data path,
    navigates, selects Balance Sheet, exports it,
    specifies the export path AND a dynamic filename, and confirms.
    Includes precise escape key placement during export configuration.
    Closes the exported file's Explorer window and then TallyPrime.
    """
    tally_exe_path = r"D:\TallyPrime\tally.exe"
    # The specific Tally data folder path where companies are located
    tally_data_folder_path = r"D:\tally\data\010001"
    # The base path where exported reports will be saved
    export_output_folder = r"D:\tally\data"

    # Initialize process to None, so it's always defined for the finally block
    process = None

    # --- 1. Validate if Tally.exe exists ---
    if not os.path.exists(tally_exe_path):
        print(f"Error: Tally.exe not found at {tally_exe_path}")
        print("Please ensure the path is correct.")
        return

    # Ensure the export output directory exists
    if not os.path.exists(export_output_folder):
        print(f"Creating export output directory: {export_output_folder}")
        os.makedirs(export_output_folder)
    else:
        print(f"Export output directory already exists: {export_output_folder}")

    print(f"Attempting to launch TallyPrime from: {tally_exe_path}")

    try:
        # --- 2. Launch TallyPrime ---
        process = subprocess.Popen(tally_exe_path)
        print("TallyPrime launched. Waiting for it to fully open...")

        initial_wait_time_seconds = 20
        print(f"Waiting for {initial_wait_time_seconds} seconds for TallyPrime to become ready...")
        time.sleep(initial_wait_time_seconds)

        # --- 3. Press 'T' to enter Education Mode ---
        print("Sending 'T' key to TallyPrime to enter Education Mode...")
        pyautogui.press('T')
        time.sleep(2)

        # --- 4. Open the specified Tally Data Path (Down Arrow x 2, Enter, Type Path, Enter) ---
        print("Navigating to Tally Data Path input (Down Arrow x 2, Enter)...")
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('down')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)
        print(f"Typing Tally data folder path: {tally_data_folder_path}")
        pyautogui.write(tally_data_folder_path)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(3)

        # --- 5. Navigate and Select Balance Sheet (Down arrow 6 times, Enter) ---
        print("Navigating to Balance Sheet (Down Arrow x 6, Enter)...")
        for _ in range(6):
            pyautogui.press('down')
            time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(2)

        # --- 6. Press Ctrl + E to export ---
        print("Pressing Ctrl + E to export...")
        pyautogui.hotkey('ctrl', 'e')
        time.sleep(1.5)

        # --- 7. Press C to configure the export ---
        print("Pressing C to configure export...")
        pyautogui.press('c')
        time.sleep(1.5)

        # --- 8. Navigate to the EXPORT PATH field (Down arrow 15 times) ---
        print("Navigating to Export PATH field (Down Arrow x 15)...")
        for _ in range(16):
            pyautogui.press('down')
            time.sleep(0.1)

        pyautogui.press('enter')
        time.sleep(1)

        # --- 12. Generate dynamic filename and type the FILENAME ONLY ---
        current_time = datetime.now()
        timestamp_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        export_filename_only = f"balancesheet_{timestamp_str}.xml"

        print(f"Typing export filename: {export_filename_only}")
        pyautogui.write(export_filename_only)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(1)

        # --- 13. Press Ctrl + A two times for final confirmation/export ---
        print("Pressing Ctrl + A two times for final confirmation...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(5) # Longer delay to allow export process to complete

        full_exported_file_path = os.path.join(export_output_folder, export_filename_only)
        print(f"Automation complete. Balance Sheet exported to: {full_exported_file_path}")

        # --- NEW STEP: Close the Explorer window that opens after export ---
        print("Closing the Explorer window (Alt+F4)...")
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1.5) # Give it time to close

    except Exception as e:
        print(f"An error occurred during automation: {e}")
        print("Please check Tally's UI and adjust timings/key presses if needed.")
        import traceback
        traceback.print_exc()

    finally:
        # --- Final Step: Close TallyPrime ---
        # This block ensures Tally is closed even if an error occurred earlier.
        if process and process.poll() is None: # Check if the Tally process is still running
            print("Closing TallyPrime...")
            try:
                # Attempt to send Alt+F4 to gracefully close the Tally window
                pyautogui.hotkey('alt', 'f4')
                time.sleep(2) # Give Tally time to respond to close command
                # Press 'Y' to confirm quitting
                print("Pressing 'Y' to confirm quitting TallyPrime...")
                pyautogui.press('y')
                time.sleep(3) # Give Tally time to fully shut down                
                if process.poll() is None: # If Tally is still running after Alt+F4, try terminate
                    process.terminate()
                    time.sleep(1)
                if process.poll() is None: # If still running after terminate, force kill
                    process.kill()
                    print("TallyPrime process forcibly terminated.")
                else:
                    print("TallyPrime closed gracefully.")
            except Exception as close_e:
                print(f"Error while trying to close TallyPrime: {close_e}")
        elif process:
            print("TallyPrime process already exited or was not launched by this script.")
        else:
            print("TallyPrime process object was not created.")


if __name__ == "__main__":
    automate_tally_balance_sheet_export()
