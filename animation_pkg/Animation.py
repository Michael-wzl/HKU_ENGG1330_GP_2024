import display_algo

class Animation:
    def __init__(self, frames = [], text = "",replay_times = 0,speed = 0.1,acceleration = 0):
        self.frames = frames if frames else []
        self.text = text if text else ""
        self.replay_times = replay_times if replay_times else 0
        self.speed = speed if speed else 0.1
        self.acceleration = acceleration if acceleration else 0

    def display(self,stdscr,algo):
        if algo == "gradual_appear_letters":
            display_algo.gradual_appear_letters(self.text,self.speed,self.acceleration,stdscr)
        elif algo == "gradual_appear_words":
            display_algo.gradual_appear_words(self.text,self.speed,self.acceleration,stdscr)
        elif algo == "appear":
            display_algo.appear(self.text,stdscr)
        elif algo == "stop_motion":
            display_algo.stop_motion(self.frames,self.replay_times,self.speed,stdscr)
