from manim import *
import numpy as np

class BrazilianTensileStrengthTest(Scene):
    def construct(self):
        # Parameters
        disk_radius = 2
        disk_color = GRAY_B
        disk_stroke = 2
        platen_width = 2.5
        platen_height = 0.3
        platen_color = DARK_GRAY
        load_color = RED
        crack_color = BLACK
        stress_color = BLUE_E
        crack_width = 0.08
        crack_length = disk_radius * 0.98

        # Disk
        disk = Circle(radius=disk_radius, color=WHITE, fill_color=disk_color, fill_opacity=1, stroke_width=disk_stroke)
        disk.move_to(ORIGIN)

        # Platens
        top_platen = Rectangle(width=platen_width, height=platen_height, color=platen_color, fill_opacity=1)
        bottom_platen = Rectangle(width=platen_width, height=platen_height, color=platen_color, fill_opacity=1)
        top_platen.next_to(disk, UP, buff=0)
        bottom_platen.next_to(disk, DOWN, buff=0)

        # Load arrows
        top_arrow = Arrow(
            start=top_platen.get_top() + UP * 0.3,
            end=top_platen.get_top(),
            color=load_color,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )
        bottom_arrow = Arrow(
            start=bottom_platen.get_bottom() + DOWN * 0.3,
            end=bottom_platen.get_bottom(),
            color=load_color,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )
        load_label = Text("Load", font_size=28, color=load_color)
        load_label.next_to(top_arrow, UP, buff=0.2)

        # Add watermark at the bottom left from start to end
        watermark = Text("Balaji Bandaru (CE21D009)", font_size=14, color=WHITE, opacity=0.18)
        watermark.to_corner(DL, buff=0.2)
        self.add(watermark)

        # Add everything to the scene
        self.play(FadeIn(disk), FadeIn(top_platen), FadeIn(bottom_platen), run_time=1)
        self.play(GrowArrow(top_arrow), GrowArrow(bottom_arrow), Write(load_label), run_time=1)

        # Gradually compress platens (keep platens in contact with disk, only show load arrows moving in)
        compress_steps = 30
        compress_dist = 0.5
        for i in range(compress_steps):
            self.play(
                top_arrow.animate.shift(DOWN * compress_dist / compress_steps),
                bottom_arrow.animate.shift(UP * compress_dist / compress_steps),
                load_label.animate.shift(DOWN * compress_dist / compress_steps),
                run_time=0.04
            )

        # Show load-displacement graph after arrows finish moving
        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0, 1.2, 0.2],
            x_length=2.5,
            y_length=2,
            axis_config={"color": WHITE},
        )
        axes.to_corner(UR, buff=0.8)
        x_label = Text("Displacement", font_size=18)
        y_label = Text("Load", font_size=18)
        x_label.next_to(axes, DOWN, buff=0.2)
        y_label.next_to(axes, LEFT, buff=0.2)
        self.play(FadeIn(axes), Write(x_label), Write(y_label), run_time=0.7)

        # Animate the load-displacement curve up to crack
        crack_group = None
        def load_disp_curve(x):
            if x < 0.6:
                return 1.6 * x
            else:
                return 0.48 + 0.02 * (x-0.6)
        curve = axes.plot(lambda x: load_disp_curve(x), x_range=[0, 1], color=RED_E)
        partial_curve = axes.plot(lambda x: load_disp_curve(x), x_range=[0, 0], color=RED_E)
        self.add(partial_curve)
        crack_start_frac = 0.6
        crack_started = False
        # Animate curve up to crack, then animate crack and drop
        for i, frac in enumerate(np.linspace(0, 1, 30)):
            if not crack_started and frac <= crack_start_frac:
                new_partial = axes.plot(lambda x: load_disp_curve(x), x_range=[0, frac], color=RED_E)
                self.play(Transform(partial_curve, new_partial), run_time=0.04)
            if not crack_started and frac > crack_start_frac:
                # The moment the load drops, animate the crack and the drop together
                crack_started = True
                crack_group = VGroup()
                for j, crack_frac in enumerate(np.linspace(0, 1, 30)):
                    up = Line(
                        start=[0, 0, 0],
                        end=[0, crack_length * crack_frac, 0],
                        color=crack_color,
                        stroke_width=8
                    )
                    down = Line(
                        start=[0, 0, 0],
                        end=[0, -crack_length * crack_frac, 0],
                        color=crack_color,
                        stroke_width=8
                    )
                    new_crack = VGroup(up, down)
                    if crack_frac == 0:
                        self.add(new_crack)
                        crack_group = new_crack
                    else:
                        # Animate both crack and graph drop together
                        drop_frac = crack_start_frac + (1 - crack_start_frac) * (j / 29)
                        new_partial = axes.plot(lambda x: load_disp_curve(x), x_range=[0, drop_frac], color=RED_E)
                        self.play(
                            Transform(crack_group, new_crack),
                            Transform(partial_curve, new_partial),
                            run_time=0.04
                        )
                break
        # Keep the crack visible till the end
        if crack_group is not None:
            self.add(crack_group)
        self.play(Transform(partial_curve, curve), run_time=0.5)

        # Show BTS equation and label D, T
        eq = MathTex(r"\text{BTS} = \frac{2P}{\pi D T}", font_size=44)
        eq.to_edge(DOWN, buff=0.7)
        self.play(Write(eq), run_time=1.2)
        # Show D (diameter) and T (thickness) on the disk
        d_arrow = DoubleArrow(
            start=[-disk_radius, 0, 0],
            end=[disk_radius, 0, 0],
            color=YELLOW,
            buff=0.05
        )
        d_label = Text("D (Diameter)", font_size=28, color=YELLOW)
        d_label.next_to(d_arrow, DOWN, buff=0.1)
        t_arrow = DoubleArrow(
            start=[disk_radius * 0.7, -0.25, 0],
            end=[disk_radius * 0.7, 0.25, 0],
            color=GREEN,
            buff=0.05
        )
        t_label = Text("T (Thickness)", font_size=28, color=GREEN)
        t_label.next_to(t_arrow, RIGHT, buff=0.1)
        self.play(GrowArrow(d_arrow), Write(d_label), GrowArrow(t_arrow), Write(t_label), run_time=1.2)
        # Add a label for P (max load)
        p_label = Text("P = max load", font_size=28, color=RED_E)
        p_label.next_to(eq, DOWN, buff=0.3)
        self.play(Write(p_label), run_time=0.7)
        # Hold final frame
        self.wait(2)
