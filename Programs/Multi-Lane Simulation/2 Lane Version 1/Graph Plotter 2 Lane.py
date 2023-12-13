import numpy as np
import matplotlib.pyplot as plt

import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])

HTML("<div style='column-count: 2;'>{}</div>".format(code))

def suvat_graph(time, graph_position, graph_speed, graph_acceleration):
    # plt.xlabel('Time ($s$)')
    # plt.ylabel('Velocity ($v$)')
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Acceleration (ms$^{-2}$)')
    ax1.plot(time, graph_acceleration, color='red', label='Acceleration $(m/s/s)$')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Velocity (ms$^{-1}$)')
    ax2.plot(time, graph_speed, color='blue', label='Velocity $(m/s)$')

    #ax3 = ax1.twinx()
    #ax3.set_ylabel('Lane $(m/s/s)$')
    #ax3.plot(time, graph_acceleration, color = 'red', label = 'Acceleration $(m/s/s)$')
    # plt.legend(loc='upper right')
    plt.show()


# time_tick(0.016666667, len(velocity1))
#suvat_graph(time_tick(dt, len(position)), position, velocity1, acceleration1)

import matplotlib

def subplot_suvat_graph(time, lane, graph_speed, graph_acceleration):
    plt.rcParams.update({'font.family':'Times New Roman'})
    plt.rcParams.update({'mathtext.default':"regular"})
    plt.figure(1)
    #acceleration subplot
    plt.subplot(311)
    plt.plot(time, graph_acceleration, '--', color = 'black')
    plt.ylabel('Acceleration (ms$^{-2}$)', fontsize = 11)
    #plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)


    #velocity subplot
    plt.subplot(312)
    plt.plot(time, graph_speed,':', color = 'black')
    plt.ylabel('Velocity (ms$^{-1}$)', fontsize = 11)
    #plt.xlabel('Time (s)', fontsize = 11)
    #plt.xticks(fontsize = 11)
    plt.yticks(fontsize = 11)


    #lane subplot
    plt.subplot(313)
    plt.plot(time, lane, ':', color = 'black')
    plt.ylabel('Lane Number', fontsize = 11)
    plt.xlabel('Time (s)', fontsize = 11)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.yticks(np.arange(1, 2.1, 1))

    plt.show()

#unpack
X = np.load('datax.npy')
Y = np.load('datay.npy')
Z = np.load('dataz.npy')
T = np.load('datat.npy')
L = np.load('datal.npy')
velocity = X
acceleration = Y
position = Z
lane = L
time = T[:len(X)]
subplot_suvat_graph(time[:2000],L[:2000],X[:2000],Y[:2000])

