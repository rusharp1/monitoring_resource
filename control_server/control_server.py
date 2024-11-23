import subprocess
import re

class ServiceController:
    def __init__(self):
        self.server_ip = ""
        self.action = ""
        self.password = ""
        self.bash_script = "./control_service.sh"
        self.action_value = {"1": "start", "2": "stop", "3": "restart"}
    
    # ip
    def get_valid_ip(self):
        while True:
            server_ip = input("Enter the server IP address (ex. 192.168.0.1): ").strip()
            
            # Validate IP format
            if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", server_ip):
                octets = server_ip.split(".")
                if all(0 <= int(octet) <= 255 for octet in octets):
                    self.server_ip = server_ip
                    break
                else:
                    print("Each octet must be between 0 and 255.")
            else:
                print("Invalid IP address format. Please try again.")
    # action (start, stop, restart)
    def get_valid_action(self):
        """Validates and sets the action."""
        while True:
            action = input("Enter the action\n1.start\n2.stop\n3.restart \nInsert number: ").strip()
            
            # Validate action
            if action in self.action_value:
                self.action = self.action_value[action]
                break
            else:
                print("Invalid action. Please enter number 1~3.")

    def run_bash(self):
        try:
            result = subprocess.run(
                ["bash", self.bash_script, self.server_ip, self.action, self.password],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Output results
            print("Output:", result.stdout)
            if result.returncode != 0:
                print("Error:", result.stderr)
        except FileNotFoundError:
            print(f"{self.bash_script} not found or not executable.")

    def run(self):
        try:
            self.get_valid_ip()
            print("-" * 50)
            self.get_valid_action()
            print("-" * 50)
            self.password = input("Enter the sudo password: ").strip()
            self.run_bash_script()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    controller = ServiceController()
    controller.run()
