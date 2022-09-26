from kivy.clock import Clock


class Timer:
    def __init__(self, label, countdown=False, countdown_start_time=0, countdown_callback=None):
        self.label = label
        self.countdown = countdown
        self.time = countdown_start_time if countdown else 0
        self.countdown_callback = countdown_callback
        self.running = False

    def start(self):
        self.running = True
        Clock.schedule_once(self.update, 1)

    def update(self, *args):
        if not self.countdown:
            self.time += 1
        else:
            self.time -= 1
            if not self.time:
                self.countdown_callback()
                return

        self.label.text = str(self)

        if self.running:
            Clock.schedule_once(self.update, 1)

    def stop(self):
        self.running = False

    def __str__(self):
        return str((self.time // 60) % 60).zfill(2) + ':' + str(self.time % 60).zfill(2)
