import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_set(fig, stator):
    ax = fig.add_subplot(1,1,1)
    ax.grid(b=False, which='major', color = "grey")
    ax.set_aspect(aspect='equal')
    if stator == 2:
        ax.set_xlim((-11, 31))
    else:
        ax.set_xlim((-11,11))
    ax.set_ylim((-11, 11))

    plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)

    for pos in ['right', 'top', 'bottom', 'left']:
        plt.gca().spines[pos].set_visible(False)

    #table
    if stator == 1:
        table(ax,0,0)
    elif stator == 2:
        table(ax,0,0)
        table(ax,20,0)
    else:
        return False

    return ax

def table(ax,xo,yo):
    #############################################################################################################
    #tabuleiro
    ##circulos, traços e pontos
    circle = plt.Circle((xo, yo), 6, color='grey', fill = False)
    circle1 = plt.Circle((xo, yo), 8, color='grey', fill = False)
    circle2 = plt.Circle((xo, yo), 9, color='grey', fill = False)

    b = 0
    while b < np.pi*2:
        x = np.array([xo, xo+8*np.cos(b)])
        y = np.array([yo, yo+8*np.sin(b)])
        ax.plot(x,y,c="grey", linewidth = 1.0)
        ax.plot((xo+8*np.cos(b)), (yo+8*np.sin(b)), 'o', color='white', ms = 10, mec = 'black')
        ax.plot((xo+6*np.cos(b)), (yo+6*np.sin(b)), 'o', color='white', ms = 10, mec = 'black')
        b += np.pi/12

    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle)

    return

def make_line(ax, paint, size1, size2, origin, offset,xo) :
    y = [xo+size1*np.sin(origin), xo+size2*np.sin(origin+offset)]
    x = [size1*np.cos(origin), size2*np.cos(origin+offset)]
    ax.plot((xo+size1*np.sin(origin)), (size1*np.cos(origin)), 'o', color=paint, ms = 10, mec = 'black')
    ax.plot((xo+size2*np.sin(origin+offset)), (size2*np.cos(origin+offset)), 'o', color=paint, ms = 10, mec = 'black')
    ax.plot(y,x, color=paint)
    return

def make_point(ax, paint, size1, origin):
    ax.plot((size1*np.sin(origin)), (size1*np.cos(origin)), 'o', color=paint, ms = 10, mec = 'black')
    return

def make_set_s1_end_to_start(ax, origin, size_up, size_bot, pp, phases):
    colors = ['black','red','blue','green','purple','orange','pink','coral','magenta','chocolate','goldenrod','tomato']
    size_up_arrow = 10
    size_bot_arrow = 8
    d_up = -1
    d_bot = 1
    blocks = 24/(phases*pp)
    offset1 = (np.pi*2)/(phases*pp)
    offset2 = (np.pi*2)/(pp*phases) - np.pi/12
    position = o = origin = 0
    origin_arrow = np.pi/2#O 0 do make line é o no.pi/2 no plt.arrow
    origin_line = origin_l = np.pi/2 - offset1 + np.pi/12
    i = 0
    l = 0
    sizex = 0
    connections = 1
    ################PHASES
    while i < phases:
        if i%2 == 0:
            size1 = size_bot
            size2 = size_up
            ax.arrow(x=size_up_arrow*np.cos(origin_arrow), y=size_up_arrow*np.sin(origin_arrow), dx=d_up*np.cos(origin_arrow), dy=d_up*np.sin(origin_arrow), width=.2, color = colors[i])
        else:
            size1 = size_up
            size2 = size_bot
            ax.arrow(x=(size_bot_arrow-4)*np.cos(origin_arrow), y=(size_bot_arrow-4)*np.sin(origin_arrow), dx=d_bot*np.cos(origin_arrow), dy=d_bot*np.sin(origin_arrow), width=.2, color = colors[i])
        j = 0
        while j < pp:
            l = 0
            while l < blocks - 1:
                #FIRST
                make_line(ax = ax, paint = colors[i], size1 = size1, size2 = size2, origin = o, offset = np.pi/12, xo = 0)
                o += np.pi/12
                l += 1
            if j + 1 < pp:
                #ODD PHASES
                if i%2 == 0:
                    offsetx = offset1*3
                    if j%2 == 0:
                        sizex = size_bot -1
                        offseti = 0
                    else:
                        sizex = size_up + 1
                        offseti = offset2
                else:
                    offsetx = offset1*3
                    if j%2 == 0:
                        sizex = size_up + 1
                        offseti = 0
                    else :
                        sizex = size_bot -1
                        offseti = offset2
                #LINES
                x = [sizex*np.cos(origin_line+ offseti),sizex*np.cos(origin_line -offsetx*phases/3 + offseti)]
                y = [sizex*np.sin(origin_line+ offseti),sizex*np.sin(origin_line -offsetx*phases/3 + offseti)]
                plt.text(x[0], y[0], str(connections),
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                plt.text(x[1], y[1], str(connections)+"'",
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                connections += 1
                if ( phases == 3 ):
                    o += 2*offset1 + np.pi/12
                elif (phases == 6):
                    o += 2*offset1 + offset1*(phases/2) + np.pi/12
                else: #12
                    o += 2*offset1 + offset1*phases*3/4 + np.pi/12
            else:
                position = np.pi/2 - o
                #LINES
                connections = 1
                if i%2 == 1:
                    ################EXIT ARROW
                    ax.arrow(x=(size_bot_arrow-2)*np.cos(position+offset2), y=(size_bot_arrow-2)*np.sin(position+offset2), dx=d_up*np.cos(position+offset2), dy=d_up*np.sin(position+offset2), width=.2, color = colors[i])
                else:
                    ################EXIT ARROW
                    ax.arrow(x=size_bot_arrow*np.cos(position+offset2), y=size_bot_arrow*np.sin(position+offset2), dx=d_bot*np.cos(position+offset2), dy=d_bot*np.sin(position+offset2), width=.2, color = colors[i])
            j += 1
            origin_line -= 3*offset1*phases/3
        size1 = size_bot
        size2 = size_up
        i+=1
        origin_line = origin_l-offset1*i
        origin_arrow-= offset1
        origin += offset1
        o = origin
    return

def make_set_s2_end_to_start(ax, origin, size_up, size_bot, pp, phases):
    colors = ['black','red','blue','orange','purple','brown','pink','coral','magenta','chocolate','goldenrod','tomato']
    size_up_arrow = 12
    size_bot_arrow = 8
    d_up = -2
    d_bot = 2
    blocks = 24/(phases*pp)
    offset1 = (np.pi*2)/(phases*pp)
    offset2 = (np.pi*2)/(pp*phases) - np.pi/12
    o1 = origin1 = 0
    position = 0
    origin2 = o2 = -np.pi/12
    origin_arrow = np.pi/2#O 0 do make line é o no.pi/2 no plt.arrow
    origin_line1 = origin_line2 = origin_l = np.pi/2 - offset1 + np.pi/12
    xo = 20
    i = 0
    l = 0
    sizex = 0
    sizey = 0
    connections = 1
    ################PHASES
    while i < phases:
        ################ENTRY ARROWs
        if i%2 == 0:
            ax.arrow(x=size_up_arrow*np.cos(origin_arrow), y=size_up_arrow*np.sin(origin_arrow), dx=d_up*np.cos(origin_arrow), dy=d_up*np.sin(origin_arrow), width=.4, color = colors[i])
        else:
            ax.arrow(x=(size_bot_arrow-6)*np.cos(origin_arrow), y=(size_bot_arrow-6)*np.sin(origin_arrow), dx=d_bot*np.cos(origin_arrow), dy=d_bot*np.sin(origin_arrow), width=.4, color = colors[i])
        j = 0
        while j < pp:
            l = 0
            if i%2 == 0:
                size1 = size_bot
                size2 = size_up
            else:
                size1 = size_up
                size2 = size_bot
            while l < blocks - 1:
                #FIRST
                make_line(ax = ax, paint = colors[i], size1 = size1, size2 = size2, origin = o1, offset = np.pi/12, xo = 0)
                #SECOND
                make_line(ax = ax, paint = colors[i], size1 = size1, size2 = size2, origin = o2, offset = np.pi/12, xo = xo)
                o1 += np.pi/12
                o2 -= np.pi/12
                l += 1
            if j + 1 < pp:
                #ODD PHASES
                if i%2 == 0:
                    offsetx = offset1*3
                    offsety = offset2
                    if j%2 == 0:
                        sizex = size_bot -1
                        sizey = size_up + 1
                        offseti = 0
                    else:
                        sizex = size_up + 1
                        sizey = size_bot -1
                        offseti = offset2
                #EVEN PHASES
                else:
                    offsetx = offset1*3
                    offsety = offset2
                    if j%2 == 0:
                        sizex = size_up + 1
                        sizey = size_bot -1
                        offseti = 0
                    else :
                        sizex = size_bot -1
                        sizey = size_up + 1
                        offseti = offset2
                #LINES
                x = [sizex*np.cos(origin_line1+ offseti),xo - sizex*np.cos(origin_line2+offsety -offseti)]
                y = [sizex*np.sin(origin_line1+ offseti),sizex*np.sin(origin_line2+offsety -offseti)]
                plt.text(x[0], y[0], str(connections),
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                plt.text(x[1], y[1], str(connections)+"'",
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                connections += 1
                x = [sizex*np.cos(origin_line1 - offsetx*phases/3+ offseti),xo - sizey*np.cos(origin_line2+ offseti)]
                y = [sizex*np.sin(origin_line1 - offsetx*phases/3+ offseti),sizey*np.sin(origin_line2+ offseti)]
                plt.text(x[0], y[0], str(connections)+"'",
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                plt.text(x[1], y[1], str(connections),
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                connections += 1
                if ( phases == 3 ):
                    o1 += 2*offset1 + np.pi/12
                    o2 -= 2*offset1 + np.pi/12
                elif ( phases == 6 ):
                    o1 += 2*offset1 + offset1*phases/2 + np.pi/12
                    o2 -= 2*offset1 + offset1*phases/2 + np.pi/12
                else: #12
                    o2 -= 2*offset1 + offset1*phases*3/4 + np.pi/12
                if(size1 == size_bot):
                    size1 = size_up
                    size2 = size_bot
                else:
                    size2 = size_up
                    size1 = size_bot
            else:
                position = np.pi/2 + o2
                x = [sizey*np.cos(origin_line2 +offset2),xo - sizey*np.cos(origin_line2)]
                y = [sizey*np.sin(origin_line2 +offset2),sizey*np.sin(origin_line2)]
                plt.text(x[0], y[0], str(connections),
                        horizontalalignment='center',
                        verticalalignment='center',
                        size='large',
                        fontweight = 'bold',
                        color = colors[i])
                plt.text(x[1], y[1], str(connections)+"'",
                    horizontalalignment='center',
                    verticalalignment='center',
                    size='large',
                    fontweight = 'bold',
                    color = colors[i])
                connections = 1
                if i%2 == 1:
                    ################EXIT ARROW
                    ax.arrow(x=xo-size_bot_arrow*np.cos(position+offset1), y=size_bot_arrow*np.sin(position+offset1), dx=-d_bot*np.cos(position+offset1), dy=d_bot*np.sin(position+offset1), width=.4, color = colors[i])
                else:
                    ################EXIT ARROW
                    ax.arrow(x=xo-(size_bot_arrow-2)*np.cos(position+offset1), y=(size_bot_arrow-2)*np.sin(position+offset1), dx=-d_up*np.cos(position+offset1), dy=d_up*np.sin(position+offset1), width=.4, color = colors[i])
            j += 1
            origin_line1 -= 3*offset1*phases/3
            origin_line2 -= 3*offset1*phases/3
        size1 = size_bot
        size2 = size_up
        i+=1
        origin_line1 = origin_l-offset1*i
        origin_line2 = origin_l-offset1*i
        origin_arrow-= offset1
        origin1 += offset1
        origin2 -= offset1
        o1 = origin1
        o2 = origin2
    return

def check_value(q, pp, phases):
    #check pp by phases
    print("oi")
    if phases == 3:
        if pp in [1,2,4]:
            return True
    elif phases == 6:
        if pp in [1,2]:
            return True
    elif phases == 12:
        if pp == 1:
            return True
    return False

def plot_configuration(q,pp,phases,stator):
    ####DEFINE VARIABLES
    fig = plt.figure()
    ax = plot_set(fig,stator)
    if stator == 2 and check_value(q,pp,phases):
        make_set_s2_end_to_start(ax = ax, origin = 0, size_up = 8, size_bot = 6, pp = pp*2, phases = phases)
        config = "2 Stators"
    elif stator == 1 and check_value(q,pp,phases):
        make_set_s1_end_to_start(ax = ax, origin = 0, size_up=8, size_bot=6, pp = pp*2, phases = phases)
        config = "Consequent Poles Series"
    else:
        return False

    plt.title(str(config)+" configuration with "+str(int(pp*2))+" poles and "+str(phases)+
    " phases", pad = 10, fontsize = 12)
    ax.grid(b=False)
    plt.show()
    return True
