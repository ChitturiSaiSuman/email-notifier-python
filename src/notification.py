from notifypy import Notify


class Notification:
    def __init__(
        self,
        title: str,
        message: str,
        application_name: str,
        urgency: str,
        path_to_icon: str,
        path_to_audio: str,
        enable_logging: bool,
    ):

        self.notifier = Notify(enable_logging=enable_logging)
        self.notifier.title = title
        self.notifier.message = message
        self.notifier.application_name = application_name
        self.notifier.urgency = urgency
        self.notifier.icon = path_to_icon
        self.notifier.audio = path_to_audio

    def notify(self):
        self.notifier.send()


if __name__ == "__main__":

    sample_notification = Notification(
        title="Sample Notification",
        message="This is a sample notification.",
        application_name="Sample App",
        urgency="normal",
        path_to_icon="../assets/icon.png",
        path_to_audio="../assets/sound.wav",
        enable_logging=True,
    )

    sample_notification.notify()
