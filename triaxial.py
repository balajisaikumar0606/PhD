#!/usr/bin/env python3
# filepath: /home/balaji/downloaded_videos/Manim/triaxial.py

from manim import *
import numpy as np

class CementedClayTriaxialTest(Scene):
    def construct(self):
        # Define the triaxial cell outline
        cell_outline = RoundedRectangle(
            height=6, 
            width=4.5, 
            corner_radius=0.2, 
            color=BLUE_E, 
            stroke_width=2,
            fill_opacity=0.05
        )
        cell_outline.shift(DOWN * 0.5)
        
        # Add stress-strain graph
        axes = Axes(
            x_range=[0, 15, 3],
            y_range=[0, 150, 30],
            axis_config={"include_tip": True, "color": WHITE},
            x_length=3.5,
            y_length=3,
            tips=False
        )
        axes.shift(RIGHT * 4.5)
        
        # Add axis labels
        x_label = MathTex("\\varepsilon", font_size=24)
        x_label.next_to(axes, DOWN, buff=0.2)
        
        y_label = MathTex("q", font_size=24)
        y_label.next_to(axes, LEFT, buff=0.2).rotate(90 * DEGREES)
        
        # Initial clay sample dimensions
        initial_height = 4
        initial_width = 2

        # Clay Sample
        clay_sample = Rectangle(
            height=initial_height,
            width=initial_width,
            color=ORANGE,
            fill_opacity=0.9,
            stroke_color=GOLD,
            stroke_width=2
        )
        # Position sample (e.g., centered horizontally, resting on base)
        # Base will be defined next, then sample positioned
        
        # Base pedestal
        base_height = 0.5
        base = Rectangle(
            height=base_height,
            width=initial_width + 0.5, # Slightly wider than sample
            color=DARK_GRAY,
            fill_opacity=1,
            stroke_width=1.5
        )
        # Position base (e.g., below cell outline, centered)
        base.move_to([cell_outline.get_center()[0], cell_outline.get_bottom()[1] + base_height/2 + 0.1, 0])

        # Now position clay_sample on top of the base
        clay_sample.move_to([base.get_center()[0], base.get_top()[1] + initial_height/2, 0])
        
        # Top piston (loading cap) - positioned to touch the sample
        top_piston = Rectangle(
            height=0.5, 
            width=initial_width, # Match sample width
            color=GRAY, 
            fill_opacity=1,
            stroke_width=1.5
        )
        # Position piston on top of the sample
        top_piston.move_to([clay_sample.get_center()[0], clay_sample.get_top()[1] + top_piston.height/2, 0])
        
        # Loading ram - positioned on top of the piston
        loading_ram = Rectangle(
            height=1.2, 
            width=0.6, 
            color=DARK_GRAY, 
            fill_opacity=1,
            stroke_width=1.5
        )
        loading_ram.move_to([top_piston.get_center()[0], top_piston.get_top()[1] + loading_ram.height/2, 0])
        
        # Water in the chamber
        water_height = cell_outline.height - 0.2
        water = Rectangle(
            height=water_height,
            width=cell_outline.width - 0.2,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=0
        )
        water.move_to(cell_outline.get_center())
        
        # Water surface with slight animation
        water_surface = Line(
            start=water.get_top() + LEFT * (water.width/2 - 0.1),
            end=water.get_top() + RIGHT * (water.width/2 - 0.1),
            color=BLUE_B,
            stroke_width=3
        )
        
        # Setup initial scene
        self.play(
            FadeIn(cell_outline),
            FadeIn(water),
            FadeIn(water_surface),
            FadeIn(clay_sample),
            FadeIn(top_piston),
            FadeIn(loading_ram),
            FadeIn(base),
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=2
        )
        
        # Create confining pressure arrows (10 arrows surrounding the sample)
        confining_arrows = VGroup()
        arrow_color = BLUE
        arrow_stroke_width = 2
        
        # Calculate positions around the sample
        sample_center = clay_sample.get_center()
        
        # Left side arrows (3 arrows)
        for i in range(3):
            y_pos = sample_center[1] + (i - 1) * initial_height * 0.3
            arrow = Arrow(
                start=[sample_center[0] - initial_width/2 - 0.6, y_pos, 0],
                end=[sample_center[0] - initial_width/2 + 0.1, y_pos, 0],
                color=arrow_color,
                stroke_width=arrow_stroke_width,
                max_tip_length_to_length_ratio=0.15,
                buff=0
            )
            confining_arrows.add(arrow)
        
        # Right side arrows (3 arrows)
        for i in range(3):
            y_pos = sample_center[1] + (i - 1) * initial_height * 0.3
            arrow = Arrow(
                start=[sample_center[0] + initial_width/2 + 0.6, y_pos, 0],
                end=[sample_center[0] + initial_width/2 - 0.1, y_pos, 0],
                color=arrow_color,
                stroke_width=arrow_stroke_width,
                max_tip_length_to_length_ratio=0.15,
                buff=0
            )
            confining_arrows.add(arrow)
        
        # Bottom arrows (4 arrows)
        for i in range(4):
            x_pos = sample_center[0] + (i - 1.5) * initial_width * 0.3
            arrow = Arrow(
                start=[x_pos, base.get_top()[1] - 0.4, 0], # MODIFIED: Use base.get_top()[1]
                end=[x_pos, base.get_top()[1] + 0.1, 0], # MODIFIED: Use base.get_top()[1]
                color=arrow_color,
                stroke_width=arrow_stroke_width,
                max_tip_length_to_length_ratio=0.15,
                buff=0
            )
            confining_arrows.add(arrow)
        
        # Show confining pressure
        self.play(
            *[GrowArrow(arrow) for arrow in confining_arrows],
            run_time=1.5
        )
        
        self.wait(1)
        
        # Consolidation phase - NO dimensional changes, just visual indication
        # Create consolidation effects around the sample (water movement indicators)
    
        self.wait(0.5)
        
        # Add axial load arrow
        top_arrow = Arrow(
            start=loading_ram.get_top() + UP * 0.5,
            end=loading_ram.get_top() + UP * 0.1,
            color=RED,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(GrowArrow(top_arrow), run_time=1)
        self.wait(0.5)
        
        # Stress-strain curve function for cemented clay
        def cemented_clay_stress_strain(x):
            if x < 0.5:
                # Initial steep elastic region (cemented clay)
                return 280 * x
            elif x <= 6:
                # Peak and beginning of softening
                elastic_stress = 280 * 0.5
                plastic_x = x - 0.5
                peak_addition = 20 * plastic_x * np.exp(-plastic_x/2)
                return elastic_stress + peak_addition
            else:
                # Strain softening
                peak_stress = 147  # Approximate peak
                softening_rate = 0.3
                residual_stress = 60
                softened = peak_stress * np.exp(-softening_rate * (x - 6))
                return max(softened, residual_stress)
        
        # Shearing stages with crack formation and gradual sample breaking
        stages = 50
        # NO dimensional changes - sample maintains original size throughout
        final_height_ratio = 1.0  # NO height change
        final_width_ratio = 1.0   # NO width change
        
        # Since there's no deformation, we just track loading progress
        t_values = np.linspace(0, 1, stages)
        
        # Initialize crack and broken piece storage
        cracks = VGroup() # This will be unused, replaced by a single main crack
        self.upper_piece = None # Use self to track pieces across stages
        self.lower_piece = None
        self.main_crack_visual = None
        
        # Total piston travel during shearing (adjust for visual effect)
        total_piston_travel_at_failure = 0.3 

        for i in range(1, stages):
            # Sample maintains original dimensions
            new_height = initial_height
            new_width = initial_width
            
            # Calculate loading progress
            progress = i / (stages - 1)
            
            # Update stress-strain curve
            x_max = 15 * progress
            
            current_partial_curve = axes.plot( # Renamed to avoid conflict with play argument
                lambda x: cemented_clay_stress_strain(x), 
                x_range=[0, x_max], 
                color=RED_E,
                stroke_width=3
            )
            
            # Variable timing for different phases
            if i < stages / 3:
                stage_run_time = 0.4
            elif i < stages * 0.6:
                stage_run_time = 0.35
            else:
                stage_run_time = 0.3
            
            animations_this_step = []
            if i == 1:
                animations_this_step.append(Create(current_partial_curve))
            else:
                if hasattr(self, 'current_stress_curve'):
                    animations_this_step.append(Transform(self.current_stress_curve, current_partial_curve))
                else:
                    # This case should ideally not be hit if self.current_stress_curve is managed correctly
                    animations_this_step.append(Create(current_partial_curve))
            
            # Piston Movement
            if self.upper_piece is None: # Before break
                # Piston moves down based on overall progress until potential failure point (e.g., 60% of stages)
                # Calculate displacement based on current progress towards total_piston_travel_at_failure
                # This displacement is from the *initial* position of the piston.
                current_strain_level = progress
                # Let piston move down proportionally to strain, up to a max before failure visualization
                # This needs initial positions stored.
                # Simpler: small incremental downward shift
                piston_inc_displacement = total_piston_travel_at_failure / (stages * 0.6) # Distribute travel over pre-failure stages
                if i <= int(stages * 0.6) : # Only move piston this way before explicit break animation
                    animations_this_step.append(top_piston.animate.shift(DOWN * piston_inc_displacement))
                    animations_this_step.append(loading_ram.animate.shift(DOWN * piston_inc_displacement))

            # Progressive crack formation and opening
            sample_center_coords = clay_sample.get_center() # Use original sample for coords before it's replaced
            
            # Main failure crack starts at 60%
            if i == int(stages * 0.4) and self.main_crack_visual is None:
                # Define crack line geometry
                cs_center = sample_center_coords
                cs_width = initial_width # Use initial_width as sample doesn't change size
                cs_height = initial_height

                # Crack from approx top-left region to bottom-right region
                p1 = cs_center + LEFT * cs_width/2 * 0.8 + UP * cs_height/2 * 0.5
                p2 = cs_center + RIGHT * cs_width/2 * 0.8 + DOWN * cs_height/2 * 0.5
                
                # Ensure p1 and p2 are on the boundary or make sense for cutting
                # For a more robust cut, ensure p1 and p2 are actual intersection points of a line with rectangle edges.
                # Using simpler definition for now:
                p1 = clay_sample.get_center() + LEFT * clay_sample.width * 0.45 + UP * clay_sample.height * 0.25
                p2 = clay_sample.get_center() + RIGHT * clay_sample.width * 0.45 + DOWN * clay_sample.height * 0.25

                self.main_crack_visual = Line(p1, p2, color=YELLOW, stroke_width=4) # ADDED: Ensure crack visual is created
                
                # Create upper and lower pieces based on this crack
                ul, ur, dr, dl = clay_sample.get_corner(UL), clay_sample.get_corner(UR), clay_sample.get_corner(DR), clay_sample.get_corner(DL)
                
                self.lower_piece = Polygon(dl, dr, p2, p1, color=ORANGE, fill_opacity=0.9, stroke_width=0) # MODIFIED: stroke_width=0
                self.upper_piece = Polygon(p1, p2, ur, ul, color=ORANGE, fill_opacity=0.9, stroke_width=0) # MODIFIED: stroke_width=0
                
                animations_this_step.extend([
                    FadeOut(clay_sample), # clay_sample is the original rectangle
                    # FadeOut(cracks), # cracks VGroup is no longer used for small cracks
                    Create(self.main_crack_visual),
                    FadeIn(self.lower_piece),
                    FadeIn(self.upper_piece)
                ])
                
            # Gradual sliding of upper piece after separation
            elif i > int(stages * 0.6) and self.upper_piece is not None:
                slide_progress_factor = (i - int(stages * 0.6)) / (stages - int(stages * 0.6)) # Factor from 0 to 1
                
                # Crack line vector (points from p1 to p2, defining slide direction)
                # Ensure main_crack_visual is defined before accessing its properties
                if self.main_crack_visual:
                    crack_vector = normalize(self.main_crack_visual.get_end() - self.main_crack_visual.get_start())
                else:
                    # Fallback or error handling if main_crack_visual is not yet created
                    # This case should ideally not be reached if logic is correct
                    crack_vector = RIGHT # Default slide direction if crack not defined
                
                # Total slide distance and rotation
                max_slide_distance = 0.1 # MODIFIED: Reduced slide distance
                max_rotation_angle = 0 # MODIFIED: Reduced rotation for subtlety with smaller slide
                
                current_slide_distance = slide_progress_factor * max_slide_distance
                current_rotation = slide_progress_factor * max_rotation_angle
                
                # Store the initial state of upper_piece if not already stored
                if not hasattr(self, 'initial_upper_piece_mobject'):
                    # This captures the state of self.upper_piece right after it's created
                    self.initial_upper_piece_mobject = self.upper_piece.copy()

                # Create the target state for this animation step
                # Start from the initial state of the broken piece
                target_upper_piece = self.initial_upper_piece_mobject.copy()
                
                # Apply the total slide and rotation for the current progress
                target_upper_piece.shift(crack_vector * current_slide_distance)
                if self.main_crack_visual: # Ensure crack visual exists for rotation point
                    target_upper_piece.rotate(-current_rotation, about_point=self.main_crack_visual.get_start()) # MODIFIED: Negative rotation for CW
                else: # Fallback rotation if no crack visual (e.g. rotate about its own center)
                    target_upper_piece.rotate(-current_rotation, about_point=target_upper_piece.get_center()) # MODIFIED: Negative rotation for CW


                animations_this_step.append(Transform(self.upper_piece, target_upper_piece))
                
                # Piston and ram follow the target state of the upper piece
                # Target y for piston center: target_upper_piece.get_top()[1] + top_piston.height / 2.0
                target_piston_center_y = target_upper_piece.get_top()[1] + top_piston.height / 2.0
                
                animations_this_step.append(top_piston.animate.move_to([top_piston.get_center()[0], target_piston_center_y, 0]))
                
                # Ram follows piston
                # Target y for ram center: (piston_center_y + piston_height/2.0) + ram_height/2.0
                target_ram_center_y = (target_piston_center_y + top_piston.height / 2.0) + loading_ram.height / 2.0
                animations_this_step.append(loading_ram.animate.move_to([loading_ram.get_center()[0], target_ram_center_y, 0]))

            if animations_this_step: # Ensure there are animations to play
                self.play(*animations_this_step, run_time=stage_run_time)
            
            # Update self.current_stress_curve for the next iteration's Transform
            self.current_stress_curve = current_partial_curve
            
            self.wait(0.05) # Short pause between stages

        self.wait(3) # Wait at the end of the animation
        
        # Complete the stress-strain curve
        final_curve = axes.plot(
            lambda x: cemented_clay_stress_strain(x), 
            x_range=[0, 15], 
            color=RED_E,
            stroke_width=3
        )
        
        # Mark peak point
        peak_x = 3.5
        peak_y = cemented_clay_stress_strain(peak_x)
        peak_point = Dot(axes.c2p(peak_x, peak_y), color=YELLOW, radius=0.1)
        
        # Ensure self.current_stress_curve exists before trying to transform it
        if hasattr(self, 'current_stress_curve'):
            self.play(
                Transform(self.current_stress_curve, final_curve),
                Create(peak_point),
                run_time=1.5
            )
        else: # Fallback if current_stress_curve wasn't initialized (e.g. if stages = 0 or 1)
            self.play(
                Create(final_curve),
                Create(peak_point),
                run_time=1.5
            )
        
        # Final pause to observe the complete test
        self.wait(3)


if __name__ == '__main__':
    print("Run this script with 'manim -pql triaxial.py CementedClayTriaxialTest'")
    print("For 4K resolution: 'manim --resolution 3840,2160 -pqh triaxial.py CementedClayTriaxialTest'")