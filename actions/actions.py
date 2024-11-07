
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import yaml

# Biến trạng thái nội bộ để lưu trữ trạng thái của các thiết bị
device_statuses = {}

# Hàm khởi tạo trạng thái từ file YAML
def initialize_device_statuses():
    global device_statuses
    with open('data/devices.yml', 'r', encoding='utf-8') as file:
        devices_data = yaml.safe_load(file)
        for device in devices_data.get("devices", []):
            device_statuses[device["name"]] = device["status"]

# Gọi hàm khởi tạo trạng thái khi file actions.py được tải
initialize_device_statuses()

class ActionToggleDevice(Action):
    def name(self):
        return "action_toggle_device"

    def run(self, dispatcher, tracker, domain):
        device_name = tracker.get_slot("device")
        intent_name = tracker.latest_message['intent'].get('name')

        # Kiểm tra xem thiết bị có tồn tại không trong biến trạng thái
        if device_name in device_statuses:
            # Thay đổi trạng thái dựa trên intent
            if intent_name == "turn_on_device":
                device_statuses[device_name] = "bật"
                dispatcher.utter_message(text=f"{device_name} đã được bật!.")
            elif intent_name == "turn_off_device":
                device_statuses[device_name] = "tắt"
                dispatcher.utter_message(text=f"{device_name} đã được tắt.")
        else:
            dispatcher.utter_message(text=f"Xin lỗi, không tìm thấy thiết bị có tên '{device_name}' trong nhà của bạn. Bạn có thể yêu cầu lại không?")

        return [SlotSet("device", device_name)]

class ActionCheckStatus(Action):
    def name(self) -> str:
        return "action_check_status"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain: str):
        device_name = tracker.get_slot("device")
        
        # Lấy trạng thái thiết bị từ biến trạng thái nội bộ
        status = device_statuses.get(device_name)
        if status:
            dispatcher.utter_message(text=f"Trạng thái của {device_name} là {status}.")
        else:
            dispatcher.utter_message(text=f"Xin lỗi, không tìm thấy thiết bị có tên '{device_name}' trong nhà của bạn. Bạn có thể yêu cầu lại không?")

        return []

