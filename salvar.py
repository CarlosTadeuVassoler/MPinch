from svg_turtle import SvgTurtle
from cairosvg import svg2png


def draw_spiral(t):
    t.fillcolor('blue')
    t.begin_fill()
    for i in range(20):
        d = 50 + i*i*1.5
        t.pencolor(0, 0.05*i, 0)
        t.width(i)
        t.forward(d)
        t.right(144)
    t.end_fill()


def write_file(draw_func, filename, width, height):
    t = SvgTurtle(width, height)
    draw_func(t)
    t.save_as(filename)


def main():
    write_file(draw_spiral, 'example.svg', 500, 500)
    print('Done.')
    svg_code = """
    <?xml version="1.0" encoding="utf-8" ?>
    <svg baseProfile="full" height="500px" version="1.1" width="500px" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink"><defs><clipPath id="border_clip"><rect height="500" width="500" x="0" y="0" /></clipPath></defs><polygon clip-path="url(#border_clip)" fill="#0000ff" fill-rule="evenodd" points="250.5,250.5 300.5,250.5 258.8356247896902,280.77094049306237 276.14057647468724,227.51177558053377 295.7631556174964,287.90386436527604 235.8958980337503,244.40775569563303 323.3958980337503,244.40775569563297 239.25813061875584,305.53742193405026 277.4217294240617,188.08194217159874 322.5382106028042,326.9361935506911 183.7917960675006,226.13102278253217 383.7917960675006,226.13102278253183 196.5043618697005,362.2033086882397 278.70288237343607,109.22227535372872 372.48954016623316,397.86792804930764 94.1876941012508,195.6698012606974 481.6876941012508,195.66980126069657 130.5743185425242,450.7686007556307 279.9840353228102,-9.067224873076384 445.6171443077833,500.6990678611255 -32.91640786499897,153.02409113012897" stroke-width="0" /><polyline clip-path="url(#border_clip)" fill="none" points="250.5,250.5 300.5,250.5" stroke="#000000" stroke-linecap="round" stroke-width="0" /><polyline clip-path="url(#border_clip)" fill="none" points="300.5,250.5 258.8356247896902,280.77094049306237" stroke="#000d00" stroke-linecap="round" stroke-width="1" /><polyline clip-path="url(#border_clip)" fill="none" points="258.8356247896902,280.77094049306237 276.14057647468724,227.51177558053377" stroke="#001a00" stroke-linecap="round" stroke-width="2" /><polyline clip-path="url(#border_clip)" fill="none" points="276.14057647468724,227.51177558053377 295.7631556174964,287.90386436527604" stroke="#002600" stroke-linecap="round" stroke-width="3" /><polyline clip-path="url(#border_clip)" fill="none" points="295.7631556174964,287.90386436527604 235.8958980337503,244.40775569563303" stroke="#003300" stroke-linecap="round" stroke-width="4" /><polyline clip-path="url(#border_clip)" fill="none" points="235.8958980337503,244.40775569563303 323.3958980337503,244.40775569563297" stroke="#004000" stroke-linecap="round" stroke-width="5" /><polyline clip-path="url(#border_clip)" fill="none" points="323.3958980337503,244.40775569563297 239.25813061875584,305.53742193405026" stroke="#004d00" stroke-linecap="round" stroke-width="6" /><polyline clip-path="url(#border_clip)" fill="none" points="239.25813061875584,305.53742193405026 277.4217294240617,188.08194217159874" stroke="#005900" stroke-linecap="round" stroke-width="7" /><polyline clip-path="url(#border_clip)" fill="none" points="277.4217294240617,188.08194217159874 322.5382106028042,326.9361935506911" stroke="#006600" stroke-linecap="round" stroke-width="8" /><polyline clip-path="url(#border_clip)" fill="none" points="322.5382106028042,326.9361935506911 183.7917960675006,226.13102278253217" stroke="#007300" stroke-linecap="round" stroke-width="9" /><polyline clip-path="url(#border_clip)" fill="none" points="183.7917960675006,226.13102278253217 383.7917960675006,226.13102278253183" stroke="#008000" stroke-linecap="round" stroke-width="10" /><polyline clip-path="url(#border_clip)" fill="none" points="383.7917960675006,226.13102278253183 196.5043618697005,362.2033086882397" stroke="#008c00" stroke-linecap="round" stroke-width="11" /><polyline clip-path="url(#border_clip)" fill="none" points="196.5043618697005,362.2033086882397 278.70288237343607,109.22227535372872" stroke="#009900" stroke-linecap="round" stroke-width="12" /><polyline clip-path="url(#border_clip)" fill="none" points="278.70288237343607,109.22227535372872 372.48954016623316,397.86792804930764" stroke="#00a600" stroke-linecap="round" stroke-width="13" /><polyline clip-path="url(#border_clip)" fill="none" points="372.48954016623316,397.86792804930764 94.1876941012508,195.6698012606974" stroke="#00b300" stroke-linecap="round" stroke-width="14" /><polyline clip-path="url(#border_clip)" fill="none" points="94.1876941012508,195.6698012606974 481.6876941012508,195.66980126069657" stroke="#00bf00" stroke-linecap="round" stroke-width="15" /><polyline clip-path="url(#border_clip)" fill="none" points="481.6876941012508,195.66980126069657 130.5743185425242,450.7686007556307" stroke="#00cc00" stroke-linecap="round" stroke-width="16" /><polyline clip-path="url(#border_clip)" fill="none" points="130.5743185425242,450.7686007556307 279.9840353228102,-9.067224873076384" stroke="#00d900" stroke-linecap="round" stroke-width="17" /><polyline clip-path="url(#border_clip)" fill="none" points="279.9840353228102,-9.067224873076384 445.6171443077833,500.6990678611255" stroke="#00e600" stroke-linecap="round" stroke-width="18" /><polyline clip-path="url(#border_clip)" fill="none" points="445.6171443077833,500.6990678611255 -32.91640786499897,153.02409113012897" stroke="#00f200" stroke-linecap="round" stroke-width="19" /></svg>
    """
    svg2png(bytestring=svg_code,write_to='output.png')


if __name__ == '__main__':
    main()
