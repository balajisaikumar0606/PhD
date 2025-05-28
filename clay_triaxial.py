#!/usr/bin/env python3
# filepath: /home/balaji/downloaded_videos/Manim/clay_triaxial.py

from manim import *
import numpy as np

class ClayTriaxialTest(Scene):
    def construct(self):
        # No title/subtitle - start directly with the setup
        
        # Create initial setup
        # Define the triaxial cell outline (just the outer boundary)
        cell_outline = RoundedRectangle(
            height=6, 
            width=4.5, 
            corner_radius=0.2, 
            color=BLUE_E, 
            stroke_width=2,
            fill_opacity=0.05
        )
        
        # Add water in the cell (represented as a transparent blue fill)
        water = RoundedRectangle(
            height=5.9, 
            width=4.4, 
            corner_radius=0.15, 
            color=BLUE,
            stroke_width=0,
            fill_opacity=0.15
        )
        cell_outline.shift(DOWN * 0.5)
        
        # Add stress-strain graph on the right side with proper bounds
        axes = Axes(
            x_range=[0, 10, 2],  # Reduced x-range for better visibility
            y_range=[0, 100, 20],
            axis_config={"include_tip": True, "color": WHITE},
            x_length=3,
            y_length=2.5,
            tips=False  # Remove the arrow tips to keep graph inside boundary
        )
        axes.shift(RIGHT * 4)
        
        # Add axis labels
        x_label = Text("Axial Strain (%)", font_size=16) # Corrected from previous "Axial Strain (%)" to ensure it's not a typo from my side
        x_label.next_to(axes, DOWN, buff=0.2)
        
        # Replace "Deviator Stress" with simple "q" label
        y_label = MathTex("q", font_size=32) # Corrected from previous "q" to ensure it's not a typo from my side
        y_label.next_to(axes, LEFT, buff=0.4)
        
        # Top piston (loading cap)
        top_piston = Rectangle(
            height=0.5, 
            width=2.2, 
            color=GRAY, 
            fill_opacity=1,
            stroke_width=1.5
        )
        top_piston.next_to(cell_outline, UP, buff=0)
        
        # Loading ram
        loading_ram = Rectangle(
            height=1.2, 
            width=0.6, 
            color=DARK_GRAY, 
            fill_opacity=1,
            stroke_width=1.5
        )
        loading_ram.next_to(top_piston, UP, buff=0)
        
        # Base pedestal
        base = Rectangle(
            height=0.5, 
            width=2.2, 
            color=GRAY, 
            fill_opacity=1,
            stroke_width=1.5
        )
        base.next_to(cell_outline, DOWN, buff=0)
        
        # Clay sample (simple rectangular block representation - fully 2D)
        initial_height = 4
        initial_width = 2
        
        # Create a simple rectangular block - pure 2D representation
        clay_sample = Rectangle(
            height=initial_height,
            width=initial_width,
            color=GOLD_E,
            fill_opacity=0.9,
            stroke_width=1.5,
            stroke_color=GOLD
        )
        
        # Position the sample to sit exactly on the base pedestal
        base_top_y = base.get_top()[1]
        clay_sample.move_to([0, base_top_y + initial_height/2, 0])
        
        # Setup scene with graph axes
        self.play(
            FadeIn(cell_outline),
            FadeIn(clay_sample),
            FadeIn(top_piston),
            FadeIn(loading_ram),
            FadeIn(base),
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )

        # Add watermark
        watermark = Text("Balaji Bandaru (CE21D009)", font_size=12)
        watermark.to_corner(DL, buff=0.2)
        self.add(watermark) # Add to scene, will persist

        # Create the stress-strain curve object (but don\'t draw it yet)
        def clay_stress_strain(x):
            # Simplified hyperbolic model for clay stress-strain relationship
            # q = q_ult * x / (C + x)
            # ultimate_strength (q_ult) defines the asymptote
            # C affects the initial stiffness (initial slope = q_ult / C)
            ultimate_strength = 88  # Asymptotic ultimate strength
            C_hyperbolic = 0.3      # Parameter affecting initial stiffness
            
            if x < 0: # Ensure strain is non-negative
                return 0
            return ultimate_strength * (x / (C_hyperbolic + x))
        
        # stress_strain_curve = axes.plot(clay_stress_strain, x_range=[0, 10], color=RED_E) # This line is not used until later
        
        # Add confining pressure (σ₃) arrows - moved inside the cell acting directly on sample
        # Create arrows from multiple directions to show true confining pressure
        arrow_stroke_width = 1.8
        arrow_color = BLUE
        tip_ratio = 0.15
        
        # Left and right arrows (horizontal)
        left_arrow = Arrow(
            start=clay_sample.get_left() + LEFT * 0.4, 
            end=clay_sample.get_left() + RIGHT * 0.1, 
            color=arrow_color, 
            buff=0,
            stroke_width=arrow_stroke_width,
            max_tip_length_to_length_ratio=tip_ratio
        )
        
        right_arrow = Arrow(
            start=clay_sample.get_right() + RIGHT * 0.4, 
            end=clay_sample.get_right() + LEFT * 0.1, 
            color=arrow_color, 
            buff=0,
            stroke_width=arrow_stroke_width,
            max_tip_length_to_length_ratio=tip_ratio
        )
        
        # Add bottom arrows to show confining pressure from all sides
        
        # Create confining pressure label (σ₃)
        sigma3_label = MathTex(r"\sigma_3", color=BLUE, font_size=32)
        sigma3_label.next_to(right_arrow, RIGHT, buff=0.2)
        
        # Add more left and right confining pressure arrows
        num_side_arrows = 8
        left_arrows = VGroup()
        right_arrows = VGroup()
        for i in range(num_side_arrows):
            frac = (i + 0.5) / num_side_arrows
            y_pos = base_top_y + frac * initial_height
            left_arrow = Arrow(
                start=[clay_sample.get_left()[0] - 0.4, y_pos, 0],
                end=[clay_sample.get_left()[0] + 0.1, y_pos, 0],
                color=arrow_color,
                buff=0,
                stroke_width=arrow_stroke_width,
                max_tip_length_to_length_ratio=tip_ratio
            )
            right_arrow = Arrow(
                start=[clay_sample.get_right()[0] + 0.4, y_pos, 0],
                end=[clay_sample.get_right()[0] - 0.1, y_pos, 0],
                color=arrow_color,
                buff=0,
                stroke_width=arrow_stroke_width,
                max_tip_length_to_length_ratio=tip_ratio
            )
            left_arrows.add(left_arrow)
            right_arrows.add(right_arrow)
        # Group all confining pressure arrows
        confining_arrows = VGroup(left_arrows, right_arrows)
        self.play(
            *[GrowArrow(arrow) for arrow in left_arrows],
            *[GrowArrow(arrow) for arrow in right_arrows],
            Write(sigma3_label),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Before applying the axial load, show consolidation for 2 seconds
        # Calculate consolidation dimensions (decrease both height and width)
        consol_height = initial_height * 0.95  # 5% height reduction
        consol_width = initial_width * 0.95    # 5% width reduction
        
        # Create the consolidated sample
        consolidated_sample = Rectangle(
            height=consol_height,
            width=consol_width,
            color=GOLD_E,
            fill_opacity=0.9,
            stroke_width=1.5,
            stroke_color=GOLD
        )
        
        # Position the consolidated sample properly
        consolidated_sample.move_to([0, base_top_y + consol_height/2, 0])
        
        # Show gradual consolidation
        # Reduce both height and width during consolidation
        self.play(
            Transform(clay_sample, consolidated_sample),
            run_time=1.5
        )
        # Show consolidation plot (time vs volume change)
        volume_axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[0.9, 1.01, 0.02],
            x_length=2.5,
            y_length=1.2,
            axis_config={"color": WHITE},
        )
        volume_axes.to_corner(UR, buff=0.7)
        t_label = Text("Time", font_size=16)
        v_label = Text("Volume", font_size=16)
        t_label.next_to(volume_axes, DOWN, buff=0.15)
        v_label.next_to(volume_axes, LEFT, buff=0.15)
        self.play(FadeIn(volume_axes), Write(t_label), Write(v_label), run_time=0.7)
        
        def volume_curve(x):
            if x < 0: # Ensure time is non-negative
                return 1.0
            if x < 0.7: # Consolidation phase (0 to 0.7 time units)
                # Logarithmic decrease: V(t) = V_initial - (V_initial - V_final) * (log(k*t + 1) / log(k*T_consol + 1))
                # V_initial = 1.0, V_final = 0.9, T_consol = 0.7
                k_factor = 10.0  # Factor to shape the logarithmic curve
                
                # Avoid log(0) or negative values if x is extremely small, though x starts from 0 in linspace
                log_input_t = k_factor * x + 1
                if log_input_t <= 0: log_input_t = 1e-9 # safety for log

                log_term_t = np.log(log_input_t)
                
                log_input_T_consol = k_factor * 0.7 + 1
                if log_input_T_consol <= 0: log_input_T_consol = 1e-9 # safety for log (e.g. if 0.7 was 0 and k_factor*x+1 was 1)

                log_term_T_consol = np.log(log_input_T_consol) # Should be np.log(8.0) for k_factor=10, T_consol=0.7
                
                if log_term_T_consol == 0: # Avoid division by zero if T_consol somehow makes log_input_T_consol = 1
                    return 1.0 - 0.1 * (k_factor * x / (k_factor * 0.7)) # Fallback to linear if log term is problematic

                return 1.0 - 0.1 * (log_term_t / log_term_T_consol)
            else: # Post-consolidation (0.7 to 1.0 time units)
                return 0.9  # Constant volume
        
        full_curve = volume_axes.plot(lambda x: volume_curve(x), x_range=[0, 1], color=BLUE_E)
        partial_curve = volume_axes.plot(lambda x: volume_curve(x), x_range=[0, 0.0001], color=BLUE_E) # Start with tiny segment
        self.add(partial_curve)
        for frac in np.linspace(0, 0.7, 20):
            new_partial = volume_axes.plot(lambda x: volume_curve(x), x_range=[0, frac], color=BLUE_E)
            self.play(Transform(partial_curve, new_partial), run_time=0.04)
        for frac in np.linspace(0.7, 1, 10):
            new_partial = volume_axes.plot(lambda x: volume_curve(x), x_range=[0, frac], color=BLUE_E)
            self.play(Transform(partial_curve, new_partial), run_time=0.04)
        self.play(Transform(partial_curve, full_curve), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(volume_axes), FadeOut(t_label), FadeOut(v_label), FadeOut(partial_curve), run_time=0.7)
        
        # Before shearing, slowly lower the loading ram and top piston together to sit on the sample
        # The top surface of the consolidated sample is at y = base_top_y + consol_height
        # The bottom of the top_piston should align with this y-coordinate.
        # So, the center of the top_piston should be at y = (base_top_y + consol_height) + (top_piston.height / 2)
        piston_target_center_y = base_top_y + consol_height + (top_piston.height / 2)
        
        # The loading_ram sits on top of the top_piston.
        # The top surface of the top_piston (after moving) will be at y = piston_target_center_y + (top_piston.height / 2)
        # The center of the loading_ram should be at y = (top of piston) + (loading_ram.height / 2)
        ram_target_center_y = piston_target_center_y + (top_piston.height / 2) + (loading_ram.height / 2)
        
        self.play(
            top_piston.animate.move_to([top_piston.get_center()[0], piston_target_center_y, 0]),
            loading_ram.animate.move_to([loading_ram.get_center()[0], ram_target_center_y, 0]),
            run_time=1.5
        )

        # Now add the top arrow and label, positioned relative to the moved loading_ram
        top_arrow = Arrow(
            start=loading_ram.get_top() + UP * 0.5, 
            end=loading_ram.get_top() + UP * 0.1,
            color=RED,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        sigma1_label = MathTex(r"\sigma_1", color=RED, font_size=32)
        sigma1_label.next_to(top_arrow, UP, buff=0.2)
        
        self.play(
            GrowArrow(top_arrow),
            Write(sigma1_label),
            run_time=1.5
        )
        
        self.wait(0.1)
        
        # Define the stages of deformation - increased for smoother animation
        stages = 100  # Adjusted stages for smoother animation (~5s total for shearing)
        stage_run_time = 15.0 / stages # Adjusted run time per stage

        final_height_ratio = 0.75  # final height will be 75% of initial shearing height
        final_mid_bulge_ratio = 1.2  # middle width will be 120% of initial shearing width
        
        # Shearing deformation is relative to consolidated dimensions
        current_sample_height_at_shear_start = consol_height
        current_sample_width_at_shear_start = consol_width
        
        top_bottom_width = current_sample_width_at_shear_start # Use consolidated width for bulging reference

        # Show gradual deformation of the sample (bulging middle)
        t_values = np.linspace(0, 1, stages)
        height_ratios = 1 - (1 - final_height_ratio) * (t_values ** 1.5)
        mid_bulge_ratios = 1 + (final_mid_bulge_ratio - 1) * (t_values ** 1.2)

        def bulged_shape(height, mid_ratio):
            """Returns a Polygon representing a bulged sample with curved sides."""
            w_top = top_bottom_width  # This is consol_width
            w_mid = top_bottom_width * mid_ratio
            h = height
            y0 = base_top_y # Base of the sample

            num_curve_points = 11 # Number of points to define one side of the curve (e.g., 10 segments)
            
            # y_coords are absolute y-coordinates from the base of the sample to its top
            y_coords = np.linspace(y0, y0 + h, num_curve_points)
            
            # relative_heights goes from 0 at bottom (y0) to 1 at top (y0 + h) of the sample
            relative_heights = np.linspace(0, 1, num_curve_points)

            # Calculate bulge profile using a sine curve.
            # bulge_factor is 0 at ends (relative_heights=0 or 1), and 1 at middle (relative_heights=0.5).
            bulge_factor = np.sin(np.pi * relative_heights)
            
            # half_added_width_at_y is the extra width on one side due to bulging.
            # This is (w_mid - w_top) / 2 at the point of maximum bulge (sample mid-height).
            # At any relative_height, the added width on one side is:
            # (w_mid - w_top) / 2 gives the max possible added half-width.
            # Multiply by bulge_factor to get the actual added half-width at that height.
            max_bulge_half_width = (w_mid - w_top) / 2
            half_added_width_at_y = max_bulge_half_width * bulge_factor

            # Calculate x-coordinates for left and right sides of the sample
            # The base width at any point is w_top. The bulge adds to this.
            x_coords_left = -w_top/2 - half_added_width_at_y
            x_coords_right = w_top/2 + half_added_width_at_y

            left_vertices = []
            for i in range(num_curve_points):
                left_vertices.append(np.array([x_coords_left[i], y_coords[i], 0]))
            
            right_vertices = []
            for i in range(num_curve_points):
                right_vertices.append(np.array([x_coords_right[i], y_coords[i], 0]))
            
            # Construct the list of all vertices for the polygon:
            # Start from bottom-left, go up along the left curve,
            # then from top-right, go down along the right curve.
            # left_vertices are already ordered from bottom to top.
            # right_vertices are also ordered from bottom to top, so we reverse them (right_vertices[::-1])
            # to get points from top to bottom for the polygon definition.
            all_vertices = left_vertices + right_vertices[::-1]
            
            return Polygon(
                *all_vertices, # Unpack the list of Point objects
                color=GOLD_E, 
                fill_opacity=0.9, 
                stroke_width=1.5, 
                stroke_color=GOLD
            )

        # Initialize the stress-strain curve plot object before the loop
        current_stress_strain_plot = axes.plot(
            clay_stress_strain, # Pass the function directly
            x_range=[0, 0.0001],  # Initial tiny segment
            color=RED_E
        )
        self.add(current_stress_strain_plot)

        # In shearing, fix glitch: always use a single partial_curve object, and update both top piston and loading ram
        for i in range(1, stages): # Loop from 1 to stages-1 for progress calculation
            # Calculate new height based on consolidated height
            new_height = current_sample_height_at_shear_start * height_ratios[i]
            mid_ratio = mid_bulge_ratios[i]
            deformed = bulged_shape(new_height, mid_ratio)

            # Move the top piston and loading ram down together
            # new_piston_pos[1] is the center of the top_piston
            new_piston_pos_y = base_top_y + new_height + top_piston.height / 2
            new_piston_pos = [top_piston.get_center()[0], new_piston_pos_y, 0]
            
            # loading_ram sits on top of top_piston
            # center_ram_y = center_piston_y + piston_height/2 + ram_height/2
            new_ram_pos_y = new_piston_pos_y + (top_piston.height / 2) + (loading_ram.height / 2)
            new_ram_pos = [loading_ram.get_center()[0], new_ram_pos_y, 0]

            progress = i / (stages - 1) # progress from 0 to 1
            x_max = 10 * progress # x_max for stress-strain curve goes up to 10
            
            # Create the new state of the stress-strain curve for transformation
            new_stress_strain_plot_segment = axes.plot(
                clay_stress_strain,
                x_range=[0, x_max],
                color=RED_E
            )

            self.play(
                Transform(clay_sample, deformed),
                top_piston.animate.move_to(new_piston_pos),
                loading_ram.animate.move_to(new_ram_pos),
                Transform(current_stress_strain_plot, new_stress_strain_plot_segment),
                run_time=stage_run_time
            )

        self.wait(0.15)

        # The stress-strain curve should be complete due to the loop.
        # Remove the redundant final curve creation.
        # final_curve = axes.plot(
        #     lambda x: clay_stress_strain(x),
        #     x_range=[0, 10],
        #     color=RED_E
        # )
        # self.play(Create(final_curve), run_time=0.8)

        self.wait(3)


if __name__ == '__main__':
    print("Run this script with 'manim -pql clay_triaxial.py ClayTriaxialTest'")
    print("For higher quality: 'manim -pqh clay_triaxial.py ClayTriaxialTest'")
