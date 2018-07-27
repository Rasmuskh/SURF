from PyOceansOpticsWrapper import OceansOpticsWrapper
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

if __name__ == "__main__":
    print "OceansOpticsWrapper class development:"
    OO = OceansOpticsWrapper()
    OO.OpenSpectrometer('HR4C5720')
    print OO.GetSerialNumber()
    print OO.GetName()
    print OO.GetFirmwareVersion()
    
    OO.SetCorrectForElectricalDark(1)
    print OO.GetCorrectForElectricalDark()    
    print OO.GetCorrectForStrayLight()
    OO.SetCorrectForDetectorNonlinearity(1)
    print OO.GetCorrectForDetectorNonlinearity()
    
    print OO.GetIntegrationTime()
    OO.SetIntegrationTime(4*1000)
    print OO.GetIntegrationTime()
    
    OO.GetCalibrationCoefficientsFromBuffer()
    print OO.coefficients.GetNlOrder()
    print OO.coefficients.GetNlCoef()
    print OO.coefficients.GetStrayLight()
    print OO.coefficients.GetWlCoef()
    
    
    w = OO.GetWavelengths()
    s = OO.GetSpectrum()
    
    
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.resize(800,800)
    view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
    mw.setCentralWidget(view)
    mw.show()
    mw.setWindowTitle('pyqtgraph: OceansOptics')
    w1 = view.addPlot()
    curve = w1.plot(pen='y')
    s = OO.GetSpectrum()
    curve.setData(x=w, y=s)
    def update():
        global curve, w, s
        s = OO.GetSpectrum()
        curve.setData(x=w, y=s)
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(100)
    
    
    QtGui.QApplication.instance().exec_()
    
    OO.CloseSpectrometer()
