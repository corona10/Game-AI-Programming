import os
import sys
import nuclai.bootstrap		# Demonstration specific setup.
import scipy.misc               # Image loading and manipulation.
import vispy.scene              # Canvas & visuals for rendering.
 

class Application(object):
    
    def __init__(self):
        self.canvas = vispy.scene.SceneCanvas(
                                title='nucl.ai Placeholder',
                                size=(1280, 720),
                                bgcolor='#F0F0F0',
                                show=False,
                                keys='interactive')

        self.widget = self.canvas.central_widget
        
        # Image CC-SA-NC by alexjc and iquilezles.
        data = scipy.misc.imread('background.jpg')

        vispy.scene.visuals.Image(data, parent=self.widget)

        vispy.scene.visuals.Text(parent=self.widget,
                                 text='nucl.ai Courses',
                                 face='Questrial', color='#000000', font_size=20 * self.canvas.pixel_scale,
                                 anchor_x='right', anchor_y='top',
                                 pos=[1268.0, 12.0, 0.0])

        vispy.scene.visuals.Text(parent=self.widget,
                                 text='The Principles of Modern Game AI',
                                 face='Questrial', color='#f0f0f0', font_size=12 * self.canvas.pixel_scale,
                                 anchor_x='left', anchor_y='bottom',
                                 pos=[16.0, 712.0, 0.0])


        self.canvas.show(visible=True)
        
        # HACK: Bug in VisPy 0.5.0-dev requires a click for layout to occur.
        self.canvas.events.mouse_press()

    def process(self, _):
        return

    def run(self):
        timer = vispy.app.Timer(interval=1.0 / 30.0)
        timer.connect(self.process)
        timer.start()
    
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    
    app = Application()
    app.run()
