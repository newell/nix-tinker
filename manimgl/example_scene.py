from manimlib import *
import numpy as np

from numpy import sin, cos, tan


# To watch one of these scenes, run the following:
# manimgl example_scenes.py OpeningManimExample
# Use -s to skip to the end and just save the final frame
# Use -w to write the animation to a file
# Use -o to write it to a file and open it once done
# Use -n <number> to skip ahead to the n'th animation of a scene.


class OpeningManimExample(Scene):
    def construct(self):
        intro_words = Text(
            """
            The original motivation for manim was to
            better illustrate mathematical functions
            as transformations.
        """
        )
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        # Linear transform
        grid = NumberPlane((-10, 10), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        linear_transform_words = VGroup(
            Text("This is what the matrix"), IntegerMatrix(matrix), Text("looks like")
        )
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_backstroke(width=5)

        self.play(
            ShowCreation(grid), FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        # Complex map
        c_grid = ComplexPlane()
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        complex_map_words = TexText(
            """
            Or thinking of the plane as $\\mathds{C}$,\\\\
            this is the map $z \\rightarrow z^2$
        """
        )
        complex_map_words.to_corner(UR)
        complex_map_words.set_backstroke(width=5)

        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6,
        )
        self.wait(2)


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(R"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # You can animate the application of mobject methods with the
        # ".animate" syntax:
        self.play(grid.animate.shift(LEFT))

        # Both of those will interpolate between the mobject's initial
        # state and whatever happens when you apply that method.
        # For this example, calling grid.shift(LEFT) would shift the
        # grid one unit to the left, but both of the previous calls to
        # "self.play" animate that motion.

        # The same applies for any method, including those setting colors.
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # The method Mobject.apply_complex_function lets you apply arbitrary
        # complex functions, treating the points defining the mobject as
        # complex numbers.
        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # Even more generally, you could apply Mobject.apply_function,
        # which takes in functions form R^3 to R^3
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2],
                ]
            ),
            run_time=5,
        )
        self.wait()


class TextExample(Scene):
    def construct(self):
        # To run this scene properly, you should have "Consolas" font in your computer
        # for full usage, you can see https://github.com/3b1b/manim/pull/680
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial",
            font_size=24,
            # t2c is a dict that you can choose color for different text
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE},
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN},
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED},
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()


class TexTransformExample(Scene):
    def construct(self):
        # Tex to color map
        t2c = {
            "A": BLUE,
            "B": TEAL,
            "C": GREEN,
        }
        # Configuration to pass along to each Tex mobject
        kw = dict(font_size=72, t2c=t2c)
        lines = VGroup(
            Tex("A^2 + B^2 = C^2", **kw),
            Tex("A^2 = C^2 - B^2", **kw),
            Tex("A^2 = (C + B)(C - B)", **kw),
            Tex(R"A = \sqrt{(C + B)(C - B)}", **kw),
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)

        self.add(lines[0])
        # The animation TransformMatchingStrings will line up parts
        # of the source and target which have matching substring strings.
        # Here, giving it a little path_arc makes each part rotate into
        # their final positions, which feels appropriate for the idea of
        # rearranging an equation
        self.play(
            TransformMatchingStrings(
                lines[0].copy(),
                lines[1],
                # matched_keys specifies which substring should
                # line up. If it's not specified, the animation
                # will align the longest matching substrings.
                # In this case, the substring "^2 = C^2" would
                # trip it up
                matched_keys=["A^2", "B^2", "C^2"],
                # When you want a substring from the source
                # to go to a non-equal substring from the target,
                # use the key map.
                key_map={"+": "-"},
                path_arc=90 * DEG,
            ),
        )
        self.wait()
        self.play(
            TransformMatchingStrings(lines[1].copy(), lines[2], matched_keys=["A^2"])
        )
        self.wait()
        self.play(
            TransformMatchingStrings(
                lines[2].copy(),
                lines[3],
                key_map={"2": R"\sqrt"},
                path_arc=-30 * DEG,
            ),
        )
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, lines, shift=2 * RIGHT))

        # TransformMatchingShapes will try to line up all pieces of a
        # source mobject with those of a target, regardless of the
        # what Mobject type they are.
        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)
        saved_source = source.copy()

        self.play(Write(source))
        self.wait()
        kw = dict(run_time=3, path_arc=PI / 2)
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, saved_source, **kw))
        self.wait()


class TexIndexing(Scene):
    def construct(self):
        # You can index into Tex mobject (or other StringMobjects) by substrings
        equation = Tex(R"e^{\pi i} = -1", font_size=144)

        self.add(equation)
        self.play(FlashAround(equation["e"]))
        self.wait()
        self.play(Indicate(equation[R"\pi"]))
        self.wait()
        self.play(
            TransformFromCopy(
                equation[R"e^{\pi i}"].copy().set_opacity(0.5),
                equation["-1"],
                path_arc=-PI / 2,
                run_time=3,
            )
        )
        self.play(FadeOut(equation))

        # Or regular expressions
        equation = Tex("A^2 + B^2 = C^2", font_size=144)

        self.play(Write(equation))
        for part in equation[re.compile(r"\w\^2")]:
            self.play(FlashAround(part))
        self.wait()
        self.play(FadeOut(equation))

        # Indexing by substrings like this may not work when
        # the order in which Latex draws symbols does not match
        # the order in which they show up in the string.
        # For example, here the infinity is drawn before the sigma
        # so we don't get the desired behavior.
        equation = Tex(
            R"\sum_{n = 1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}", font_size=72
        )
        self.play(FadeIn(equation))
        self.play(
            equation[R"\infty"].animate.set_color(RED)
        )  # Doesn't hit the infinity
        self.wait()
        self.play(FadeOut(equation))

        # However you can always fix this by explicitly passing in
        # a string you might want to isolate later. Also, using
        # \over instead of \frac helps to avoid the issue for fractions
        equation = Tex(
            R"\sum_{n = 1}^\infty {1 \over n^2} = {\pi^2 \over 6}",
            # Explicitly mark "\infty" as a substring you might want to access
            isolate=[R"\infty"],
            font_size=72,
        )
        self.play(FadeIn(equation))
        self.play(equation[R"\infty"].animate.set_color(RED))  # Got it!
        self.wait()
        self.play(FadeOut(equation))


class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        # On all frames, the constructor Brace(square, UP) will
        # be called, and the mobject brace will set its data to match
        # that of the newly constructed object
        brace = always_redraw(Brace, square, UP)

        label = TexText("Width = 0.00")
        number = label.make_number_changeable("0.00")

        # This ensures that the method deicmal.next_to(square)
        # is called on every frame
        label.always.next_to(brace, UP)
        # You could also write the following equivalent line
        # label.add_updater(lambda m: m.next_to(brace, UP))

        # If the argument itself might change, you can use f_always,
        # for which the arguments following the initial Mobject method
        # should be functions returning arguments to that method.
        # The following line ensures thst decimal.set_value(square.get_y())
        # is called every frame
        number.f_always.set_value(square.get_width)
        # You could also write the following equivalent line
        # number.add_updater(lambda m: m.set_value(square.get_width()))

        self.add(square, brace, label)

        # Notice that the brace and label track with the square
        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(square.animate.set_width(2), run_time=3)
        self.wait()

        # In general, you can alway call Mobject.add_updater, and pass in
        # a function that you want to be called on every frame.  The function
        # should take in either one argument, the mobject, or two arguments,
        # the mobject and the amount of time since the last frame.
        now = self.time
        w0 = square.get_width()
        square.add_updater(lambda m: m.set_width(w0 * math.sin(self.time - now) + w0))
        self.wait(4 * PI)


class CoordinateSystemExample(Scene):
    def construct(self):
        axes = Axes(
            # x-axis ranges from -1 to 10, with a default step size of 1
            x_range=(-1, 10),
            # y-axis ranges from -2 to 2 with a step size of 0.5
            y_range=(-2, 2, 0.5),
            # The axes will be stretched so as to match the specified
            # height and width
            height=6,
            width=10,
            # Axes is made of two NumberLine mobjects.  You can specify
            # their configuration with axis_config
            axis_config=dict(
                stroke_color=GREY_A,
                stroke_width=2,
                numbers_to_exclude=[0],
            ),
            # Alternatively, you can specify configuration for just one
            # of them, like this.
            y_axis_config=dict(
                big_tick_numbers=[-2, 2],
            ),
        )
        # Keyword arguments of add_coordinate_labels can be used to
        # configure the DecimalNumber mobjects which it creates and
        # adds to the axes
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        # Axes descends from the CoordinateSystem class, meaning
        # you can call call axes.coords_to_point, abbreviated to
        # axes.c2p, to associate a set of coordinates with a point,
        # like so:
        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        # Similarly, you can call axes.point_to_coords, or axes.p2c
        # print(axes.p2c(dot.get_center()))

        # We can draw lines from the axes to better mark the coordinates
        # of a given point.
        # Here, the always_redraw command means that on each new frame
        # the lines will be redrawn
        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        # If we tie the dot to a particular set of coordinates, notice
        # that as we move the axes around it respects the coordinate
        # system defined by them.
        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))

        # Other coordinate systems you can play around with include
        # ThreeDAxes, NumberPlane, and ComplexPlane.


class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8), height=6)
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        # Axes.get_graph will return the graph of a function
        sin_graph = axes.get_graph(
            lambda x: 2 * math.sin(x),
            color=BLUE,
        )
        # By default, it draws it so as to somewhat smoothly interpolate
        # between sampled points (x, f(x)).  If the graph is meant to have
        # a corner, though, you can set use_smoothing to False
        relu_graph = axes.get_graph(
            lambda x: max(x, 0),
            use_smoothing=False,
            color=YELLOW,
        )
        # For discontinuous functions, you can specify the point of
        # discontinuity so that it does not try to draw over the gap.
        step_graph = axes.get_graph(
            lambda x: 2.0 if x > 3 else 1.0,
            discontinuities=[3],
            color=GREEN,
        )

        # Axes.get_graph_label takes in either a string or a mobject.
        # If it's a string, it treats it as a LaTeX expression.  By default
        # it places the label next to the graph near the right side, and
        # has it match the color of the graph
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label),
        )
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(FadeOut(step_graph), FadeOut(step_label), ShowCreation(parabola))
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        dot.add_updater(lambda d: d.move_to(axes.i2gp(x_tracker.get_value(), parabola)))

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()


class TexAndNumbersExample(Scene):
    def construct(self):
        axes = Axes((-3, 3), (-3, 3), unit_size=1)
        axes.to_edge(DOWN)
        axes.add_coordinate_labels(font_size=16)
        circle = Circle(radius=2)
        circle.set_stroke(YELLOW, 3)
        circle.move_to(axes.get_origin())
        self.add(axes, circle)

        # When numbers show up in tex, they can be readily
        # replaced with DecimalMobjects so that methods like
        # get_value and set_value can be called on them, and
        # animations like ChangeDecimalToValue can be called
        # on them.
        tex = Tex("x^2 + y^2 = 4.00")
        tex.next_to(axes, UP, buff=0.5)
        value = tex.make_number_changeable("4.00")

        # This will tie the right hand side of our equation to
        # the square of the radius of the circle
        value.add_updater(lambda v: v.set_value(circle.get_radius() ** 2))
        self.add(tex)

        text = Text(
            """
            You can manipulate numbers
            in Tex mobjects
        """,
            font_size=30,
        )
        text.next_to(tex, RIGHT, buff=1.5)
        arrow = Arrow(text, tex)
        self.add(text, arrow)

        self.play(
            circle.animate.set_height(2.0),
            run_time=4,
            rate_func=there_and_back,
        )

        # By default, tex.make_number_changeable replaces the first occurance
        # of the number,but by passing replace_all=True it replaces all and
        # returns a group of the results
        exponents = tex.make_number_changeable("2", replace_all=True)
        self.play(
            LaggedStartMap(FlashAround, exponents, lag_ratio=0.2, buff=0.1, color=RED),
            exponents.animate.set_color(RED),
        )

        def func(x, y):
            # Switch from manim coords to axes coords
            xa, ya = axes.point_to_coords(np.array([x, y, 0]))
            return xa**4 + ya**4 - 4

        new_curve = ImplicitFunction(func)
        new_curve.match_style(circle)
        circle.rotate(angle_of_vector(new_curve.get_start()))  # Align
        value.clear_updaters()

        self.play(
            *(ChangeDecimalToValue(exp, 4) for exp in exponents),
            ReplacementTransform(circle.copy(), new_curve),
            circle.animate.set_stroke(width=1, opacity=0.5),
        )


class SurfaceExample(ThreeDScene):
    def construct(self):
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images, which will
        # be interpreted as the side towards the light, and away from
        # the light.  These can be either urls, or paths to a local file
        # in whatever you've set as the image directory in
        # the custom_config.yml file

        # day_texture = "EarthTextureMap"
        # night_texture = "NightEarthTextureMap"
        day_texture = "/home/newell/code/nix-tinker/manimgl/day.jpg"  # "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        night_texture = "/home/newell/code/nix-tinker/manimgl/night.jpg"  # "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(Transform(surface, surfaces[1]), run_time=3)

        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            self.frame.animate.increment_phi(-10 * DEG),
            self.frame.animate.increment_theta(-20 * DEG),
            run_time=3,
        )
        # Add ambient rotation
        self.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # Play around with where the light is
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        light_dot = GlowDot(color=WHITE, radius=0.5)
        light_dot.always.move_to(light)
        self.add(light, light_dot)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or f")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()


class InteractiveDevelopment(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        # This opens an iPython terminal where you can keep writing
        # lines as if they were part of this construct method.
        # In particular, 'square', 'circle' and 'self' will all be
        # part of the local namespace in that terminal.
        self.embed()

        # Try copying and pasting some of the lines below into
        # the interactive shell
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEG))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text(
            """
            In general, using the interactive shell
            is very helpful when developing new scenes
        """
        )
        self.play(Write(text))

        # In the interactive shell, you can just type
        # play, add, remove, clear, wait, save_state and restore,
        # instead of self.play, self.add, self.remove, etc.

        # To interact with the window, type touch().  You can then
        # scroll in the window, or zoom by holding down 'z' while scrolling,
        # and change camera perspective by holding down 'd' while moving
        # the mouse.  Press 'r' to reset to the standard camera position.
        # Press 'q' to stop interacting with the window and go back to
        # typing new commands into the shell.

        # In principle you can customize a scene to be responsive to
        # mouse and keyboard interactions
        always(circle.move_to, self.mouse_point)


class ControlsExample(Scene):
    drag_to_pan = False

    def setup(self):
        self.textbox = Textbox()
        self.checkbox = Checkbox()
        self.color_picker = ColorSliders()
        self.panel = ControlPanel(
            Text("Text", font_size=24),
            self.textbox,
            Line(),
            Text("Show/Hide Text", font_size=24),
            self.checkbox,
            Line(),
            Text("Color of Text", font_size=24),
            self.color_picker,
        )
        self.add(self.panel)

    def construct(self):
        text = Text("text", font_size=96)

        def text_updater(old_text):
            assert isinstance(old_text, Text)
            new_text = Text(self.textbox.get_value(), font_size=old_text.font_size)
            # new_text.align_data_and_family(old_text)
            new_text.move_to(old_text)
            if self.checkbox.get_value():
                new_text.set_fill(
                    color=self.color_picker.get_picked_color(),
                    opacity=self.color_picker.get_picked_opacity(),
                )
            else:
                new_text.set_opacity(0)
            old_text.become(new_text)

        text.add_updater(text_updater)

        self.add(MotionMobject(text))

        self.textbox.set_value("Manim")
        # self.wait(60)
        # self.embed()


# See https://github.com/3b1b/videos for many, many more


# Need a function that will take a radiant point, a curve (parametric or other),
# then will trace the reflected points of the radiant point about the tangents to the curve.
# First start with a circle


class EvoluteOrthotomicCardioidExample(Scene):
    def construct(self):
        # Euler–Mascheroni constant (approximate)
        gamma = 0.57721

        # radiant point
        radiant_pt = np.array([0, 0, 0])
        radiant = Dot(radiant_pt).set_fill(YELLOW)
        # curve
        cardioid = ParametricCurve(
            lambda t: np.array(
                [
                    2 * (1 + np.cos(t)) * np.cos(t) + gamma,
                    2 * (1 + np.cos(t)) * np.sin(t),
                    0,
                ]
            ),
            # t_range=[0, 2 * PI, 0.01],
            t_range=[-PI + 0.001, PI - 0.001, 0.01],
            color="#0FF1CE",
        )

        tangent = TangentLine(cardioid, alpha=0, length=20)
        proj_pt = tangent.get_projection(radiant_pt)
        proj = Dot(proj_pt)

        # origin = Dot(np.array([0, 0, 0])).set_fill(BLACK)
        origin_line = Line(np.array([0, -20, 0]), np.array([0, 20, 0]))
        critical_line = Line(np.array([0.5, -20, 0]), np.array([0.5, 20, 0]))
        pole = Dot(np.array([1, 0, 0])).set_fill(PURPLE_E)
        pole_line = Line(np.array([1, -20, 0]), np.array([1, 20, 0]))

        # Calculate the reflected point using midpoint formula
        refl_pt = np.array(
            [2 * proj_pt[0] - radiant_pt[0], 2 * proj_pt[1] - radiant_pt[1], 0]
        )
        refl = Dot(refl_pt).set_fill(RED)
        self.play(
            # FadeIn(origin),
            FadeIn(pole),
            ShowCreation(critical_line),
            ShowCreation(origin_line),
            ShowCreation(pole_line),
        )
        self.play(ShowCreation(cardioid))
        self.play(ShowCreation(tangent))
        self.play(FadeIn(radiant))
        self.play(FadeIn(proj))
        self.play(FadeIn(refl))
        proj_trace = TracedPath(proj.get_center_of_mass, stroke_width=5)
        refl_trace = TracedPath(
            refl.get_center_of_mass, stroke_width=5, stroke_color=RED
        )
        self.add(proj_trace, refl_trace)
        x_tracker = ValueTracker()
        f_always(
            tangent.become,
            lambda: TangentLine(
                cardioid,
                alpha=((x_tracker.get_value() % TAU) / TAU),
                length=10,
                d_alpha=1e-4,
            ),
        )
        f_always(
            proj.move_to,
            lambda: tangent.get_projection(radiant_pt),
        )
        f_always(
            refl.move_to,
            lambda: np.array(
                [
                    2 * proj.get_center_of_mass()[0] - radiant_pt[0],
                    2 * proj.get_center_of_mass()[1] - radiant_pt[1],
                    0,
                ]
            ),
        )
        self.play(x_tracker.animate.set_value(TAU), run_time=5, rate_func=smooth)

        traced_path = refl_trace.copy().clear_updaters()

        # Group to store all normal lines
        normals = VGroup()

        # Generate normal lines at multiple positions
        for alpha in np.linspace(0, 1, 200):  # 20 normal lines for smooth effect
            normal_line = TangentLine(
                traced_path, alpha=alpha, length=30, stroke_color=YELLOW, stroke_width=1
            ).rotate(TAU / 4)
            normals.add(normal_line)

        self.play(
            AnimationGroup(*[ShowCreation(normal) for normal in normals], lag_ratio=0.1)
        )


class SwitchedFreethNephroid(Scene):
    def construct(self):
        a = 2  # Scaling factor for size

        # Parametric equations for the switched nephroid
        switched_nephroid = ParametricCurve(
            lambda t: np.array(
                [
                    a * (3 * np.cos(t) + np.cos(3 * t)),  # Flipped inner loops
                    a * (3 * np.sin(t) + np.sin(3 * t)),
                    0,
                ]
            ),
            t_range=[0, TAU, 0.01],  # Full loop
            color=BLUE,
        )

        # Animate drawing the curve
        self.play(ShowCreation(switched_nephroid), run_time=4)
        self.wait(2)


class EvoluteOrthotomicCircleExample(Scene):
    def construct(self):
        # radiant point
        radiant_pt = np.array([0, 2, 0])
        radiant = Dot(radiant_pt).set_fill(YELLOW)
        # curve
        circle = Circle(radius=1)
        circle.set_stroke(BLUE, 5)

        tangent = TangentLine(circle, alpha=0, length=20)
        proj_pt = tangent.get_projection(radiant_pt)
        proj = Dot(proj_pt)

        origin = Dot(np.array([0, 0, 0])).set_fill(BLACK)

        # Calculate the reflected point using midpoint formula
        refl_pt = np.array(
            [2 * proj_pt[0] - radiant_pt[0], 2 * proj_pt[1] - radiant_pt[1], 0]
        )
        refl = Dot(refl_pt).set_fill(RED)
        self.play(FadeIn(origin))
        self.play(ShowCreation(circle))
        self.play(ShowCreation(tangent))
        self.play(FadeIn(radiant))
        self.play(FadeIn(proj))
        self.play(FadeIn(refl))
        proj_trace = TracedPath(proj.get_center_of_mass, stroke_width=5)
        refl_trace = TracedPath(
            refl.get_center_of_mass, stroke_width=5, stroke_color=RED
        )
        self.add(proj_trace, refl_trace)
        x_tracker = ValueTracker(0 * PI)
        f_always(
            tangent.become,
            lambda: TangentLine(
                circle,
                alpha=((x_tracker.get_value() % (2 * PI)) / (2 * PI)),
                length=10,
                d_alpha=1e-3,
            ),
        )
        f_always(
            proj.move_to,
            lambda: tangent.get_projection(radiant_pt),
        )
        f_always(
            refl.move_to,
            lambda: np.array(
                [
                    2 * proj.get_center_of_mass()[0] - radiant_pt[0],
                    2 * proj.get_center_of_mass()[1] - radiant_pt[1],
                    0,
                ]
            ),
        )
        self.play(x_tracker.animate.set_value(2 * PI), run_time=5, rate_func=smooth)

        traced_path = refl_trace.copy().clear_updaters()

        # Group to store all normal lines
        normals = VGroup()

        # Generate normal lines at multiple positions
        for alpha in np.linspace(0, 1, 300):  # 20 normal lines for smooth effect
            normal_line = TangentLine(
                traced_path, alpha=alpha, length=30, stroke_color=YELLOW, stroke_width=1
            ).rotate(TAU / 4)
            normals.add(normal_line)

        self.play(
            AnimationGroup(*[ShowCreation(normal) for normal in normals], lag_ratio=0.1)
        )


class NormalExample(Scene):
    def construct(self):
        # circle_pt = Dot(np.array([1, 0, 0])).set_fill(RED)
        circle = Circle(radius=1)
        circle.set_stroke(BLUE, 5)
        tangent = TangentLine(circle, alpha=0, length=20).set_stroke(RED)
        self.play(ShowCreation(circle), run_time=2)
        self.play(ShowCreation(tangent))
        self.play(tangent.animate.rotate(TAU / 4))


class TangentEnvelope(Scene):
    def construct(self):
        # Define the parametric function
        def parametric_func(t):
            return np.array([t, np.sin(t), 0])  # Example: Sinusoidal curve

        # Define curve
        curve = ParametricCurve(parametric_func, t_range=[-PI, PI, 0.01], color=BLUE)

        # Animate the curve
        self.play(ShowCreation(curve), run_time=3)

        # Define parameters for tangent lines
        num_tangents = 30
        t_values = np.linspace(-PI, PI, num_tangents)

        tangent_lines = VGroup()
        for t in t_values:
            # Compute point on curve
            point = parametric_func(t)

            # Compute derivative (slope)
            dx = 1
            dy = np.cos(t)  # Derivative of sin(t) is cos(t)
            slope = dy / dx

            # Define tangent line
            tangent = Line(
                start=point + np.array([-1, -slope, 0]),  # Move along tangent direction
                end=point + np.array([1, slope, 0]),
                color=YELLOW,
            )

            tangent_lines.add(tangent)

        # Animate the creation of tangent lines sequentially
        self.play(
            AnimationGroup(*[ShowCreation(tan) for tan in tangent_lines], lag_ratio=0.2)
        )
        self.wait(2)


class NormalEnvelope(Scene):
    def construct(self):
        # Define the parametric function
        def parametric_func(t):
            return np.array([t, np.sin(t), 0])  # Example: Sinusoidal curve

        # Define curve
        curve = ParametricCurve(parametric_func, t_range=[-PI, PI, 0.01], color=BLUE)

        # Animate the curve
        self.play(ShowCreation(curve), run_time=3)

        # Define parameters for tangent lines
        num_tangents = 30
        t_values = np.linspace(-PI, PI, num_tangents)

        tangent_lines = VGroup()
        for t in t_values:
            # Compute point on curve
            point = parametric_func(t)

            # Compute derivative (slope)
            dx = 1
            dy = np.cos(t)  # Derivative of sin(t) is cos(t)
            slope = dy / dx

            # Define tangent line
            tangent = (
                Line(
                    start=point
                    + np.array([-1, -slope, 0]),  # Move along tangent direction
                    end=point + np.array([1, slope, 0]),
                    color=YELLOW,
                )
                .rotate(TAU / 4)
                .set_length(20)
            )
            tangent_lines.add(tangent)

        # Animate the creation of tangent lines sequentially
        self.play(
            AnimationGroup(*[ShowCreation(tan) for tan in tangent_lines], lag_ratio=0.2)
        )
        self.wait(2)


class PedalCurveExample(Scene):
    def construct(self):
        pedal_pt = np.array([0, 2, 0])
        pedal = Dot(pedal_pt).set_fill(GREEN)
        circle_pt = Dot(np.array([1, 0, 0])).set_fill(RED)
        circle = Circle(radius=1)
        circle.set_stroke(BLUE, 5)
        tangent = TangentLine(circle, alpha=0, length=20).set_stroke(RED)
        proj_pt = tangent.get_projection(pedal_pt)
        self.play(ShowCreation(circle), run_time=2)
        self.play(ShowCreation(tangent))

        intersection_pt = Dot(proj_pt)
        intersection_line = Line(pedal_pt, proj_pt).set_length(20)
        ## NOTE: can also find line intersection point from both lines
        # print(
        #     line_intersection(
        #         [tangent.start, tangent.end],
        #         [intersection_line.start, intersection_line.end],
        #     ),
        #     intersection_pt.get_center(),
        # )
        self.play(FadeIn(circle_pt))
        self.play(FadeIn(pedal))
        self.play(ShowCreation(intersection_line))
        self.play(FadeIn(intersection_pt))
        trace = TracedPath(intersection_pt.get_center_of_mass, stroke_width=5)
        self.add(trace)

        x_tracker = ValueTracker(0 * PI)
        f_always(
            circle_pt.move_to, lambda: circle.point_at_angle(x_tracker.get_value())
        )
        f_always(
            tangent.become,
            lambda: TangentLine(
                circle,
                alpha=((x_tracker.get_value() % (2 * PI)) / (2 * PI)),
                length=10,
                d_alpha=1e-3,
            ).set_stroke(RED),
        )
        f_always(
            intersection_line.become,
            lambda: Line(pedal_pt, intersection_pt.get_center()).set_length(20),
        )
        f_always(
            intersection_pt.move_to,
            lambda: tangent.get_projection(pedal_pt),
        )
        self.play(x_tracker.animate.set_value(2 * PI), run_time=5, rate_func=smooth)


class CardiodExample(Scene):
    def construct(self):
        cardioid = ParametricCurve(
            lambda t: np.array(
                [
                    # np.exp(1) * np.cos(t) * (1 - np.cos(t)),
                    # np.exp(1) * np.sin(t) * (1 - np.cos(t)),
                    (1 + np.cos(t)) * np.cos(t),
                    (1 + np.cos(t)) * np.sin(t),
                    0,
                ]
            ),
            t_range=[0, 2 * PI, 0.01],
            color="#0FF1CE",
        )
        self.add(cardioid)


class Cardiod2Example(Scene):
    def construct(self):
        # Two circles
        stationary_circle = Circle(radius=1).set_stroke(WHITE, 5)
        moving_circle = Circle(radius=1).move_to(np.array([2, 0, 0]))
        inte_pt = Dot(np.array([1, 0, 0])).set_fill(RED)
        vg = VGroup(inte_pt, moving_circle)
        self.add(stationary_circle, vg)
        trace = TracedPath(inte_pt.get_center_of_mass, stroke_width=5, stroke_color=RED)
        self.add(trace)
        x_tracker = ValueTracker(0 * PI)
        self.play(
            x_tracker.animate.set_value(2 * PI), run_time=5
        )  # , rate_func=smooth)

        # pedal_pt = np.array([0, 2, 0])
        # pedal = Dot(pedal_pt).set_fill(GREEN)
        # circle_pt = Dot(np.array([1, 0, 0])).set_fill(RED)
        # circle = Circle(radius=1)
        # circle.set_stroke(BLUE, 5)
        # tangent = TangentLine(circle, alpha=0, length=20).set_stroke(RED)
        # self.play(ShowCreation(circle), run_time=2)
        # self.play(ShowCreation(tangent))
        # proj_pt = tangent.get_projection(pedal_pt)
        # intersection_pt = Dot(proj_pt)
        # intersection_line = Line(pedal_pt, proj_pt).set_length(20)
        # self.play(FadeIn(circle_pt))
        # self.play(FadeIn(pedal))
        # self.play(ShowCreation(intersection_line))
        # self.play(FadeIn(intersection_pt))
        # trace = TracedPath(intersection_pt.get_center_of_mass, stroke_width=5)
        # self.add(trace)

        # x_tracker = ValueTracker(0 * PI)
        # f_always(
        #     circle_pt.move_to, lambda: circle.point_at_angle(x_tracker.get_value())
        # )
        # f_always(
        #     tangent.become,
        #     lambda: TangentLine(
        #         circle,
        #         alpha=((x_tracker.get_value() % (2 * PI)) / (2 * PI)),
        #         length=10,
        #         d_alpha=1e-3,
        #     ).set_stroke(RED),
        # )
        # f_always(
        #     intersection_line.become,
        #     lambda: Line(pedal_pt, intersection_pt.get_center()).set_length(20),
        # )
        # f_always(
        #     intersection_pt.move_to,
        #     lambda: tangent.get_projection(pedal_pt),
        # )
        # self.play(x_tracker.animate.set_value(2 * PI), run_time=5, rate_func=smooth)


# Varniex - CodingManim 03: Mastering the Graphs & Coordinate System
# YouTube Video: https://youtu.be/KFsYpc_pgh4


def get_slope_of_tangent(t, graph):
    p0 = graph.get_function()(t)
    p1 = graph.get_function()(t + EPSILON)
    return tan(angle_of_vector([EPSILON, p1 - p0]))


class RosePatternWithParametricCurve(ParametricCurve):
    def __init__(
        self,
        radius: float = 2,
        k: float = 10,
        theta_range: float = TAU,
        step_size: float = 0.05,
        **kwargs,
    ):
        self.radius = radius
        self.k = k
        super().__init__(
            t_func=lambda t: [
                radius * cos(k * t) * cos(t),
                radius * cos(k * t) * sin(t),
                0,
            ],
            t_range=(0, theta_range + step_size, step_size),
            **kwargs,
        )


class ParametricCurveExample(Scene):
    def construct(self):
        step_func = ParametricCurve(
            lambda t: [t, 0 if t < 0 else 1, 0],
            t_range=[-5, 5, 0.1],
            discontinuities=[0],
        )
        self.play(ShowCreation(step_func))


class ParametricSinCurve(Scene):
    def construct(self):
        sin_curve = ParametricCurve(
            t_func=lambda t: [t, sin(t), 0], t_range=[-PI, PI, 0.1]
        )
        sin_curve.set_color(YELLOW)
        self.play(ShowCreation(sin_curve))


class GroupingObjects(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        hexagon = RegularPolygon(6)
        star = Star(5).scale(0.7)

        shapes = VMobject()
        shapes.add(circle, square, hexagon, star)
        shapes.scale(0.75)
        shapes.set_stroke(WHITE)
        shapes.set_color_by_gradient(BLUE, RED, YELLOW, PINK)

        self.play(ShowCreation(shapes))

        # VGroup
        shapes_vgroup = VGroup(circle, square, hexagon, star)
        shapes_vgroup.arrange(RIGHT, buff=2)
        shapes_vgroup.set_stroke(YELLOW, width=8)


class FunctionGraphExample(Scene):
    def construct(self):
        sin_curve = FunctionGraph(sin).set_color(BLUE)
        cos_curve = FunctionGraph(cos).set_color(RED)
        parabola = FunctionGraph(lambda x: x**2).set_color(YELLOW)
        cubic = FunctionGraph(lambda x: x**3).set_color(PINK)
        relu = FunctionGraph(lambda x: max(0, x)).set_color(TEAL)

        self.play(ShowCreation(sin_curve))
        self.play(ReplacementTransform(sin_curve, cos_curve))
        self.play(ReplacementTransform(cos_curve, parabola))
        self.play(ReplacementTransform(parabola, cubic))
        self.play(ReplacementTransform(cubic, relu))


class IntroToAxes(Scene):
    def construct(self):
        axes = Axes(
            x_range=(-5, 5, 1), y_range=(-3, 3, 1), axis_config=dict(include_tip=True)
        )
        axes.add_coordinate_labels()
        axes_labels = axes.get_axis_labels()
        self.play(ShowCreation(axes), Write(axes_labels))

        sin_curve = axes.get_graph(sin)
        sin_curve.set_color(YELLOW)
        self.play(ShowCreation(sin_curve))


class DistanceTimeGraph(Scene):
    def construct(self):
        axes = Axes(
            x_range=(0, 7, 1),
            y_range=(0, 25, 3),
            height=6,
            axis_config=dict(include_tip=True),
        )
        axes.add_coordinate_labels()
        axes_labels = axes.get_axis_labels("t", "x(t)")
        self.play(ShowCreation(axes), Write(axes_labels))

        dist_graph = axes.get_graph(
            function=lambda t: t**2 if t < 3 else 6 * t - 9, x_range=(0, 5)
        ).set_color(BLUE)
        self.play(ShowCreation(dist_graph))

        tangent = axes.get_tangent_line(2.5, dist_graph)
        self.play(ShowCreation(tangent))

        vel_graph = axes.get_graph(
            lambda t: 2 * t if t < 3 else 6, x_range=(0, 5)
        ).set_color(RED)
        self.play(ShowCreation(vel_graph))

        dist_label = axes.get_graph_label(dist_graph, "x(t)")
        vel_label = axes.get_graph_label(vel_graph, "v(t)")
        self.play(
            Write(dist_label),
            Write(vel_label),
            FadeOut(axes_labels[1]),
            FadeOut(tangent),
        )

        ## Code to sweep tangent from t = 0 to t = 5 secs

        # very helpful to access dot coords at any time (t).
        # dot coords: (time coord, slope of tangent at that time)
        def get_dot_coords():
            return axes.c2p(
                t := t_coord.get_value(), get_slope_of_tangent(t, dist_graph)
            )

        # time coordinate tracker
        t_coord = ValueTracker(0)
        tangent = always_redraw(
            lambda: axes.get_tangent_line(t_coord.get_value(), dist_graph, length=2)
        )

        dot = Dot(fill_color=YELLOW)
        dot.f_always.move_to(get_dot_coords)

        h_line = always_redraw(lambda: axes.get_h_line(dot.get_center()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_center()))

        self.add(h_line, v_line)
        self.play(ShowCreation(dot), ShowCreation(tangent))
        self.wait()
        self.play(
            t_coord.animate.set_value(5),
            run_time=5,
            rate_func=there_and_back,
        )

        area = axes.get_area_under_graph(
            graph=vel_graph, x_range=(2, 4), fill_color=RED  # fill_opacity=0.5
        )
        self.play(ShowCreation(area))
        self.wait()
