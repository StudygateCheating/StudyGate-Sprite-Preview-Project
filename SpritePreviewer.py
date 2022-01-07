import math
import sys
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskel_sprite(sprite_folder_name, number_of_sprite_frames):
    sprite_frames = []
    padding = math.ceil(math.log(number_of_sprite_frames - 1, 10))
    for frame in range(number_of_sprite_frames):
        folder_and_file_name = (
            sprite_folder_name + "/sprite_" + str(frame).rjust(padding, "0") + ".png"
        )
        sprite_frames.append(QPixmap(folder_and_file_name))

    return sprite_frames


class SpritePreview(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_sprite_frames = 21
        self.sprite_frames = load_piskel_sprite("spriteImages", self.num_sprite_frames)
        # setGeometry(left, top, width, height)
        self.setGeometry(100, 60, 500, 500)

        # Add any other instance variables needed to track information as the program
        # runs here

        # Make the GUI in the setupUI method
        self.grid = QGridLayout()

        self.number_of_frames_per_second = 1
        self.current_sprite_index = 0
        self.slider = QSlider(Qt.Vertical)
        self.slider.setValue(1)

        self.frames_pers_second_label = QLabel()
        self.frames_pers_second_label.setText(
            "Frames Per Second " + str(self.slider.value())
        )
        self.frames_pers_second_label.setFont(QFont("Arial", 20))
        self.grid.addWidget(self.frames_pers_second_label, *(2.5, 0))

        # The File Label
        self.file_label = QLabel()
        self.file_label.setText("File")
        self.file_label.setFont(QFont("Arial", 20))
        self.grid.addWidget(self.file_label, *(0, 0))

        # CurrentImage
        self.display_image_label = QLabel()
        self.grid.addWidget(self.display_image_label, *(1, 0))

        # The start/stop button
        self.start = True
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.set_number_of_frames_per_second)
        self.grid.addWidget(self.start_button, *(3, 0))

        self.create_slider()

        # Menu
        #Create pause action
        #No need to declare pause_action as am instance variable as it will be used only here
        pause_action = QAction('&Pause', self)
        pause_action.setStatusTip('Pause')
        pause_action.triggered.connect(self.menu_pause_animation)

        # Create exit action
        #No need to declare exit_action as am instance variable as it will be used only here
        exit_action = QAction('&Exit', self)
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.menu_exit_application)

        # Create menu bar and add action
        #No need to declare menubar as am instance variable as it will be used only here
        menuBar = self.menuBar()
        menu = menuBar.addMenu('&Menu')
        menu.addAction(pause_action)
        menu.addAction(exit_action)

        # Set timer as an instance variable as it would be used in multuple places in the code. such as the pause menu and the start button.
        self.timer = QTimer()
        self.timer.timeout.connect(self.pull_sprite_image)
        self.timer.start(1000)
        self.pull_sprite_image()
        self.setupUI()


    def menu_pause_animation(self):
        """"Stop the animation"""
        self.start = False
        self.start_button.setText("Start")
        self.timer.stop()


    def menu_exit_application(self):
        """Exit the application"""
        sys.exit()


    def setupUI(self):
        self.frame = QFrame()
        self.setCentralWidget(self.frame)

        self.frame.setLayout(self.grid)
        self.set_number_of_frames_per_second()
        self.show()


    def create_slider(self):
        """Creates a single instance of the slider"""
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(60)
        self.grid.addWidget(self.slider, *(0, 1, 4, 1))


    def get_number_of_digits_in_no(self, number):
        """This is necessary in order to have the proper naming of the sprites.
            It enables us to know to add zeros when the sprite number is single digit. e.g
            sprite_0.png becomes sprite_00.png
        """
        digits = len(str(number))
        return digits


    def set_number_of_frames_per_second(self):
        """Create a playback for sprite images"""
        if self.start:
            self.timer.stop()
            self.start_button.setText("Start")
            self.start = False
        else:
            self.start = True

            # Calculate the speed of the playback
            frames_per_second = 1000 / self.slider.value()
            self.timer.start(frames_per_second)
            self.start_button.setText("Stop")


        self.frames_pers_second_label.setText(
            "Frames Per Second " + str(self.slider.value())
        )


    def pull_sprite_image(self):
        """Get the next sprite image from the list"""

        current_index_length = self.get_number_of_digits_in_no(
            self.current_sprite_index
        )
        if current_index_length == 1:
            current_index = "0" + str(self.current_sprite_index)
        else:
            current_index = str(self.current_sprite_index)
        sprites_folder_path = "spriteImages"
        next_image = self.current_sprite_index + 1
        dir_path = os.path.dirname(os.path.realpath(__file__))

        full_image_path = dir_path + '/' + sprites_folder_path + "/sprite_" + str(current_index) + ".png"
        if os.path.exists(full_image_path):
            self.display_image_label.setPixmap(
                QPixmap(full_image_path).scaled(
                    200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        else:
            pass

        try:
            self.sprite_frames[self.current_sprite_index]
            self.current_sprite_index += 1
        except IndexError:
            self.current_sprite_index = 0
        return full_image_path


def main():

    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    app.exec_()


if __name__ == "__main__":
    main()
