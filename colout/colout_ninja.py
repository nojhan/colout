
import colout_cmake

def theme(context):
    # Ninja theme

    # Inherit from the CMake theme
    context,th = colout_cmake.theme(context)

    # Because Ninja note progress as a fraction, we do not want the scale of a percentage
    context["scale"] = (0,1)

    # Link (ninja)
    th.append( [ "^\[[0-9/]+\]\s?(Linking .* )(library|executable) (.*/)*(.+(\.[aso]+)*)$",
          "blue", "normal,normal,bold" ] )
    # progress percentage (ninja)
    th.append( [ "^(\[[0-9]+/[0-9]+\])","Scale" ] )

    return context,th
