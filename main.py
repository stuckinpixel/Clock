
import pygame, sys, time, random, json, datetime, math
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 400, 400
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Clock')



class Clock:
    def __init__(self):
        init_time_frame = self.get_current_time()
        self.hour = init_time_frame[0]
        self.minute = init_time_frame[1]
        self.second = init_time_frame[2]
        self.source_point = (WIDTH//2, HEIGHT//2)
        self.gap_between_points = 10
        self.radius = 150
        self.hour_radius = self.radius-(self.gap_between_points*5)
        self.minute_radius = self.radius-(self.gap_between_points*4)
        self.second_radius = self.radius-(self.gap_between_points*3)
        self.hour_thickness = 5
        self.minute_thickness = 3
        self.second_thickness = 1
        self.offset_angle = -90
        self.frame_point_tickness = 5
        self.frame_point_radius = self.radius-(self.gap_between_points*2)
        self.center_point_radius = 10
    def update_time(self):
        init_time_frame = self.get_current_time()
        self.hour = init_time_frame[0]
        self.minute = init_time_frame[1]
        self.second = init_time_frame[2]
    def get_current_time(self):
        hour = datetime.datetime.now().hour
        if hour>12:
            hour -= 12
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        return hour, minute, second
    def get_point(self, angle, radius):
        angle = math.radians(angle)
        x = self.source_point[0]+(radius*math.cos(angle))
        y = self.source_point[1]+(radius*math.sin(angle))
        return (x, y)
    def get_second_point(self):
        percentage_of_second = self.second/60
        angle = (360*percentage_of_second)+self.offset_angle
        return self.get_point(angle, self.second_radius)
    def get_minute_point(self):
        one_percentage_of_minute = 1/60
        percentage_of_second = self.second/60
        percentage_of_minute = (self.minute/60)+(one_percentage_of_minute*percentage_of_second)
        angle = (360*percentage_of_minute)+self.offset_angle
        return self.get_point(angle, self.minute_radius)
    def get_hour_point(self):
        one_percentage_of_minute = 1/60
        percentage_of_second = self.second/60
        percentage_of_minute = (self.minute/60)+(one_percentage_of_minute*percentage_of_second)
        one_percentage_of_hour = 1/12
        percentage_of_minute = self.minute/60
        percentage_of_hour = (self.hour/12)+(one_percentage_of_hour*percentage_of_minute)
        angle = (360*percentage_of_hour)+self.offset_angle
        return self.get_point(angle, self.hour_radius)
    def get_hour_for_frame_point(self, hour):
        percentage_of_hour = hour/12
        angle = (360*percentage_of_hour)+self.offset_angle
        return self.get_point(angle, self.frame_point_radius)


class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (40, 51, 80),
            "alpha": (0, 249, 56)
        }
        self.clock = Clock()
    def action(self):
        self.clock.update_time()
    def draw_clock(self):
        # draw full round
        pygame.draw.circle(self.surface, self.color["alpha"], self.clock.source_point, self.clock.radius, 1)
        # draw second pin
        pygame.draw.line(self.surface, self.color["alpha"], self.clock.source_point, self.clock.get_second_point(), self.clock.second_thickness)
        # draw minute pin
        pygame.draw.line(self.surface, self.color["alpha"], self.clock.source_point, self.clock.get_minute_point(), self.clock.minute_thickness)
        # draw hour pin
        pygame.draw.line(self.surface, self.color["alpha"], self.clock.source_point, self.clock.get_hour_point(), self.clock.hour_thickness)
        # draw time frame points
        for hour in range(12):
            pygame.draw.circle(self.surface, self.color["alpha"], self.clock.get_hour_for_frame_point(hour), self.clock.frame_point_tickness)
        # draw center point
        pygame.draw.circle(self.surface, self.color["alpha"], self.clock.source_point, self.clock.center_point_radius)
    def render(self):
        self.draw_clock()
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
            #--------------------------------------------------------------
            self.action()
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()
