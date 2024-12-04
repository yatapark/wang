import matplotlib.pyplot as plt
import random
import csv
import datetime
import os

class PlotImages():
    def __init__(
        self,
        steps: int = 10
    ) -> None:
        
        self.fig = plt.figure(figsize=(10, 10))
        
        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.ax2 = self.fig.add_axes([0.0, 0.1, 0.1, 0.8])
        self.ax3 = self.fig.add_axes([0.9, 0.1, 0.1, 0.8])
        self.ax4 = self.fig.add_axes([0.1, 0.9, 0.8, 0.1])
        self.ax5 = self.fig.add_axes([0.1, 0.0, 0.8, 0.1])
        
        self.cartoon_image = plt.imread("./img/pk.jpg")
        self.icon_size = 1
        self.icon_height = self.icon_size
        self.icon_width = self.icon_size

        self.sides = ['left', 'right', 'top', 'bottom'] * steps
        random.shuffle(self.sides)

        cartoon_icon_left = self.ax2.imshow(self.cartoon_image, extent=self.get_extent(direction='left'))
        cartoon_icon_right = self.ax3.imshow(self.cartoon_image, extent=self.get_extent(direction='right'))
        cartoon_icon_top = self.ax4.imshow(self.cartoon_image, extent=self.get_extent(direction='top'))
        cartoon_icon_bottom = self.ax5.imshow(self.cartoon_image, extent=self.get_extent(direction='bottom'))
        self.cartoon_icons = [cartoon_icon_left, cartoon_icon_right, cartoon_icon_top, cartoon_icon_bottom]

        self.frame = 0

        self.current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.original_filename = "ksa"
        self.directory = "results"
        self.new_filename = f"{self.current_datetime}_{self.original_filename}"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(f"./{self.directory}/{self.new_filename}.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Frame", "Side", "Red Dot", "Icon Coords", "Dem Input"])

        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        plt.show()
        self.update_plot()
        print("Press Enter to move to the next frame.")
        
    def get_extent(self, direction: str):
        """Generate the position for the cartoon icon based on the direction."""
        if direction == 'bottom':
            position = random.uniform(0, 3.5) if random.random() < 0.5 else random.uniform(4.5, 8)
            fixed_extent = [position - self.icon_width/2, position + self.icon_width/2, -1, 0]
        elif direction == 'left':
            position = random.uniform(0, 8)
            fixed_extent = [-1, 0, position - self.icon_height/2, position + self.icon_height/2]
        elif direction == 'right':
            position = random.uniform(0, 8)
            fixed_extent = [8, 9, position - self.icon_height/2, position + self.icon_height/2]
        elif direction == 'top':
            position = random.uniform(0, 8)
            fixed_extent = [position - self.icon_width/2, position + self.icon_width/2, 8, 9]
        return fixed_extent

    def update_plot(self):

        if self.frame >= len(self.sides):
            print("All frames have been completed.")
            exit()

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.ax5.clear()

        self.ax1.set_xlim(0, 8)
        self.ax1.set_ylim(0, 8)
        self.ax1.set_xticks(range(0, 9))
        self.ax1.set_yticks(range(0, 9))
        self.ax1.grid(True)
        self.ax1.tick_params(axis='both', which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

        self.ax2.set_xlim(-1, 0)
        self.ax2.set_ylim(0, 8)
        self.ax2.axis('off')

        self.ax3.set_xlim(8, 9)
        self.ax3.set_ylim(0, 8)
        self.ax3.axis('off')

        self.ax4.set_xlim(0, 8)
        self.ax4.set_ylim(8, 9)
        self.ax4.axis('off')

        self.ax5.set_xlim(0, 8)
        self.ax5.set_ylim(-1, 0)
        self.ax5.axis('off')

        red_dot = self.ax1.plot([], [], 'ro', markersize=10)
        
        red_x = random.uniform(0, 8)
        red_y = random.uniform(0, 8)
        red_dot[0].set_data(red_x, red_y)
        side = self.sides[self.frame]

        if side == 'left':
            cartoon_icon_coords = self.get_extent('left')
            self.cartoon_icons[0].set_extent(cartoon_icon_coords)
            self.ax2.imshow(self.cartoon_image, extent=cartoon_icon_coords)
        elif side == 'right':
            cartoon_icon_coords = self.get_extent('right')
            self.cartoon_icons[1].set_extent(cartoon_icon_coords)
            self.ax3.imshow(self.cartoon_image, extent=cartoon_icon_coords)
        elif side == 'top':
            cartoon_icon_coords = self.get_extent('top')
            self.cartoon_icons[2].set_extent(cartoon_icon_coords)
            self.ax4.imshow(self.cartoon_image, extent=cartoon_icon_coords)
        elif side == 'bottom':
            cartoon_icon_coords = self.get_extent('bottom')
            self.cartoon_icons[3].set_extent(cartoon_icon_coords)
            self.ax5.imshow(self.cartoon_image, extent=cartoon_icon_coords)

        self.cartoon_icons[0].set_visible(side == 'left')
        self.cartoon_icons[1].set_visible(side == 'right')
        self.cartoon_icons[2].set_visible(side == 'top')
        self.cartoon_icons[3].set_visible(side == 'bottom')

        print(f"Frame: {self.frame}, Red Dot ({red_x:.2f}, {red_y:.2f}), Cartoon Icon {cartoon_icon_coords} on {side}")
        cartoon_x = (cartoon_icon_coords[0] + cartoon_icon_coords[1]) / 2
        cartoon_y = (cartoon_icon_coords[2] + cartoon_icon_coords[3]) / 2
        self.buffer = [self.frame, side, (red_x, red_y), (cartoon_x, cartoon_y)]

        plt.draw()

        return [(red_x, red_y), cartoon_icon_coords]
            
    def on_key_press(self, event):
        if event.key == 'k':
            self.frame += 1
            self.dem = 'こ'
            self.save_history()
            self.update_plot()
        elif event.key == 't':
            self.frame += 1
            self.dem = 'そ'
            self.save_history()
            self.update_plot()
        elif event.key == 'a':
            self.frame += 1
            self.dem = 'あ'
            self.save_history()
            self.update_plot()
        elif event.key == 'q':
            plt.close()
        elif event.key == 'enter':
            self.update_plot()
        else:
            print("Invalid key. Press 'k' for こ, 't' for そ, 'a' for あ, and 'q' to quit.")

    def save_history(self):
        with open(f"./{self.directory}/{self.new_filename}.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.buffer[0],
                self.buffer[1],
                self.buffer[2],
                self.buffer[3],
                self.dem
            ])
            
        print("Data has been recorded in the CSV file.")

def main():
    steps = input("Enter to steps to run the program: ")
    PlotImages(steps=int(steps))

if __name__ == "__main__":
    main()