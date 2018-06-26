import numpy as np
import matplotlib.pyplot as P
import Analysis

SAVE_PATH = '/mnt/c/Users/Andrew/Desktop/Deloitte/project'

# constructs new figure with window and figure titles	
def constructFig(title):
	P.clf()
	fig = P.gcf()
	fig.canvas.set_window_title(title)
	fig.suptitle(title, fontsize = 8)
	return fig


#saves the figure to SAVE_DIRECTORY/title.extension
def savePlot(fig, title, extension = '.png'):
	savePath = SAVE_PATH + '/' + title + extension
	try:
		fig.savefig(savePath)
		P.close() #CAREFUL
	except:
		print('Could not save to path ' + savePath)
		traceback.print_exc(file = sys.stdout)
		pass


#simple scatter plot of an xProperty against yProperty for runners
def plotScatter(title, runners, xProperty, yProperty, **kwargs):
	#plot info
	plotTitle = "%s: scatterplot of %s vs %s" % (title, xProperty, yProperty)
	fig = constructFig(plotTitle)

	xvalues = Analysis.getAttributes(runners, xProperty);
	yvalues = Analysis.getAttributes(runners, yProperty);

	P.xlabel(xProperty)
	P.ylabel(yProperty)

	#plot generation
	P.scatter(xvalues, yvalues, **kwargs)

	P.show()
	savePlot(fig, plotTitle)
	return P