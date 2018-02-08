import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib import style

import numpy as np
import urllib
import datetime as dt

style.use('ggplot')
print(plt.style.available)
print(plt.__file__)

MA1=10
MA2=30

def moving_average(values,window):
    weights=np.repeat(1.0,window)/window
    smas=np.convolve(values,weights,'valid')
    return smas

def high_minus_low(highs,lows):
    return highs-lows

# highs=[11,12,15,14,13]
# lows=[5,6,2,6,7]
#
# h_1=list(map(high_minus_low,highs,lows))
# print(h_1)

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def graph_data(stock):
    fig = plt.figure()
    ax1 = plt.subplot2grid((6, 1), (0, 0),rowspan=1,colspan=1)
    plt.title(stock)
    plt.ylabel('H-L')

    ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1,sharex=ax1)

    plt.ylabel('Price')
    ax2v=ax2.twinx()

    ax3 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1,sharex=ax1)
    plt.ylabel('MAVGgs')


    # Unfortunately, Yahoo's API is no longer available
    # feel free to adapt the code to another source, or use this drop-in replacement.
    stock_price_url = 'https://pythonprogramming.net/yahoo_finance_replacement'
    source_code = urllib.request.urlopen(stock_price_url).read().decode()
    stock_data = []
    split_source = source_code.split('\n')
    for line in split_source[1:]:
        split_line = line.split(',')
        if len(split_line) == 7:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)

    date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data,
                                                                      delimiter=',',
                                                                      unpack=True,
                                                                      converters={0: bytespdate2num('%Y-%m-%d')})

    x=0
    y=len(date)
    ohlc=[]

    while x<y:
        append_me=date[x], closep[x], highp[x], lowp[x], openp[x], adj_closep[x], volume[x]
        ohlc.append(append_me)
        x+=1

    ma1=moving_average(closep,MA1)
    ma2 = moving_average(closep, MA2)
    start=len(date[MA2-1:])

    h_1=list(map(high_minus_low,highp,lowp))

    ax1.plot_date(date[-start:],h_1[-start:],'-')
    # how many ticker there are<=5
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbin=3,prune='lower'))

    candlestick_ohlc(ax2,ohlc[-start:],width=0.4,colorup='g',colordown='r')
    # ax1.plot(date,closep)
    # ax1.plot(date, openp)


    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbin=6,prune='upper'))
    ax2.grid(True)
    # xytext=date[-1]+4 means that we will move the text outside the graphe
    bbox_props = dict(boxstyle='round', fc='w', ec='k', lw=1)
    ax2.annotate(str(closep[10]), (date[12], closep[12]),
                 xytext = (date[12], closep[12]), bbox=bbox_props)

    # # Annotation example with arrow
    # # add annotation
    # ax1.annotate('Big News!',(date[11],highp[11]),
    #              xytext=(0.8,0.9),textcoords='axes fraction',
    #              arrowprops=dict(facecolor='grey',color='grey'))
    #
    # # font dict example
    # # add the texts on the plot
    # font_dict={'family':'serif',
    #            'color':'darkred',
    #            'size':15}
    # ax1.text(date[10],closep[1],'Text Example',fontdict=font_dict)


    # plt.title(stock)
    # plt.legend()

    ax2v.fill_between(date[-start:],ma1[-start:],0,volume[-start:],facecolor='#007983',alpha=0.3)
    ax2v.axes.yaxis.set_ticklabels([])
    ax2v.grid(False)
    ax2v.set_ylim(0,3*volume.max())

    ax3.plot(date[-start:],ma1[-start:],linewidth=1)
    ax3.plot(date[-start:],ma2[-start:],linewidth=1)
    ax3.fill_between(date[-start:],ma2[-start:],ma1[-start:],where=(ma1[-start:]<ma2[-start:]),facecolor='r',edgecolor='r',alpha=0.5)
    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:], where=(ma1[-start:] > ma2[-start:]), facecolor='g',
                    edgecolor='g', alpha=0.5)

    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # set how many point to show in the x label
    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))

    ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbin=4, prune='upper'))
    for label in ax3.xaxis.get_ticklabels():
        label.set_rotation(45)


    plt.setp(ax1.get_xticklabels(),visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    plt.show()


graph_data('EBAY')