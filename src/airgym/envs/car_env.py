import setup_path
import airsim
import numpy as np
import math
import time

import gym
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv


class AirSimCarEnv(AirSimEnv):
    def __init__(self, ip_address):
        super().__init__()

        self.car = airsim.CarClient(ip=ip_address)


        self.car_controls = airsim.CarControls()

        self.reset()

    def _setup_car(self):
        self.car.reset()
        self.car.enableApiControl(True)
        self.car.armDisarm(True)
        time.sleep(0.01)

    def __del__(self):
        self.car.reset()

    def _do_action(self, direction, accelerator):
        # Frear
        #if action == 0:
        #    self.car_controls.throttle = 0
        #    self.car_controls.brake = 1

        if accelerator == 42:
            self.reset()
            return None

        # Neutro
        if direction == 0:
            self.car_controls.steering = 0
        # Pouco direita
        elif direction == 1:
            self.car_controls.steering = 0.25
        # Muito direita
        elif direction == 2:
            self.car_controls.steering = 0.5
        # Pouco esquerda
        elif direction == 3:
            self.car_controls.steering = -0.25
        # Muito esquerda
        elif direction == 4:
            self.car_controls.steering = -0.5

        # Neutro (accelerator == 0)
        self.car_controls.throttle = 0
        self.car_controls.brake = 0
        # Frear/re
        if accelerator == -1:
            self.car_controls.throttle = -1
            self.car_controls.is_manual_gear = True
            self.car_controls.manual_gear = -1
            #self.car_controls.brake = 0
        # Acelerar
        elif accelerator == 1:
            self.car_controls.throttle = 1
            self.car_controls.is_manual_gear = False
            self.car_controls.manual_gear = 0
            #self.car_controls.brake = 0

        self.car.setCarControls(self.car_controls)
        #time.sleep(1)

    def step(self, action):
        direction, accelerator = action
        self._do_action(direction, accelerator)
        #return self.state

    def reset(self):
        self._setup_car()
        self._do_action(0,0)
