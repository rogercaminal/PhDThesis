
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from ROOT import *
from array import *

from optparse import OptionParser, OptionGroup

ROOT.gROOT.SetStyle('ATLAS')
ROOT.gROOT.ForceStyle()

ROOT.gStyle.SetPadTopMargin(0.05)
ROOT.gStyle.SetPadRightMargin(0.05)
ROOT.gStyle.SetPadBottomMargin(0.37)
ROOT.gStyle.SetPadLeftMargin(0.10)

orderedSyste = ['total', 'stat', 'mu\_Ele', 'mu\_Wmn', 'mu\_Zmm', 'alpha\_JER', 'alpha\_JES', 'alpha\_JvfUnc', 'alpha\_pdfUnc', 'alpha\_Pileup', 'alpha\_ktfac', 'alpha\_qfac', 'alpha\_SCALEST', 'alpha\_RESOST', 'alpha\_Luminosity', 'alpha\_bosonPtReweight', 'alpha\_WZtransfer', 'alpha\_EEFF', 'alpha\_EGZEE', 'alpha\_EGLOW', 'alpha\_EGMAT', 'alpha\_EGPS', 'alpha\_EGRES', 'alpha\_MID', 'alpha\_MMS', 'alpha\_MEFF', 'alpha\_MSCALE', 'alpha\_ttbarPs', 'alpha\_ttbarGen', 'alpha\_ttbarXsec', 'alpha\_ttbarRad', 'alpha\_ttbarFac', 'alpha\_ttbarRen', 'alpha\_singleTXsecS', 'alpha\_singleTXsecW', 'alpha\_singleTPs', 'alpha\_singleTGen', 'alpha\_singleTInt', 'alpha\_singleTRad', 'alpha\_dibMatch', 'alpha\_dibFac', 'alpha\_dibXsec', 'alpha\_dibRen', 'alpha\_qcdNorm']

regionDict = {'A6':'M1', 'A3':'M2', 'A4':'M3', 'A8':'M4', 'A9':'M5', 'A10':'M6'}
systeDictNames = {'total':'TOTAL', 'stat':'Stat.'}

def ATLASLabel(x, y, text, luminosity, color, selection):
    l = TLatex()
    l.SetNDC()
    l.SetTextFont(72)
    l.SetTextColor(color)
    l.DrawLatex(x,y,"ATLAS")

    delx = 0.115*696*ROOT.gPad.GetWh()/(472*ROOT.gPad.GetWw())

    lumi = TLatex()
    lumi.SetNDC()
    lumi.SetTextSize(0.04)
    lumi.DrawLatex(x+3*delx, y, "#int L dt = %.1f fb^{-1}, #sqrt{s} = 8 TeV" % float(luminosity/1000.))

    if (text):
      p = TLatex()
      p.SetNDC()
      p.SetTextFont(42)
      p.SetTextColor(color)
      p.DrawLatex(x,y-0.05,text)

      if (selection):
          p2 = TLatex()
          p2.SetNDC()
          p2.SetTextFont(42)
          p2.SetTextColor(color)
          p2.DrawLatex(x+7*delx,y,'Selection: %s'%selection)


def extractSystematics(fileName):
    file = open(fileName)
    lines = file.readlines()
    systeDict = {}
    totalBackground = 0.
    for line in lines:
        if 'Total background expectation' in line:
            totalBackground = float(line.split('$')[1])
        if 'Total background systematic' in line:
            systeDict['total'] = float(line.split('$')[1][3:].split('\\')[0])
        if 'Total statistical' in line:
            systeDict['stat'] = float(line.split('$')[3][3:].split('\\')[0])
        if ( ('mu\_' in line) or ('alpha\_' in line) ):
            systeDict[line.split()[0]] = float(line.split('$')[1][3:].split('\\')[0])
    file.close()

    systeDictPercent = {}
    for b in systeDict.keys():
        systeDictPercent[b] = systeDict[b]/totalBackground

    return systeDictPercent


def plotErrors(systeDictPercent, selection, savePlot):

    graph = TGraph(len(systeDictPercent))

    xValues = []
    yValues = []

    histo = TH1F('histo', 'histo', len(systeDictPercent), 0, len(systeDictPercent))
    histo.GetXaxis().SetLabelSize(0.04)

    counter = 0.
    for syste in orderedSyste:

        if syste not in systeDictPercent.keys():
            continue

        xValues.append(counter+0.5)
        yValues.append(systeDictPercent[syste]*100.)

        if syste in systeDictNames.keys():
            histo.GetXaxis().SetBinLabel(int(counter)+1, systeDictNames[syste])
        else:
            histo.GetXaxis().SetBinLabel(int(counter)+1, syste.replace('\_','_'))

        counter += 1

    histo.GetXaxis().LabelsOption("V")

    canvas = TCanvas("Systematic uncertainties", "Systematic uncertainties", 1200, 500)
    canvas.cd()

    xArray = array('d',xValues)
    yArray = array('d',yValues)
    graph = TGraph(len(systeDictPercent), xArray, yArray)
    
    histo.GetYaxis().SetTitle("Uncertainty [%]")
    histo.SetMaximum(systeDictPercent['total']*150)
    histo.Draw("")

    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.3)
    graph.SetMarkerColor(kGreen+3)
    graph.SetLineColor(kGreen+3)
    graph.Draw("samePx")

    xArraySpecial = array('d', [xValues[0]])
    yArraySpecial = array('d', [yValues[0]])
    graphSpecial = TGraph(1, xArraySpecial, yArraySpecial)
    graphSpecial.SetMarkerStyle(20)
    graphSpecial.SetMarkerSize(1.4)
    graphSpecial.SetMarkerColor(kRed+3)
    graphSpecial.SetLineColor(kRed+3)
    graphSpecial.Draw("samePx")

    ATLASLabel(0.2,0.83,"Internal", 20300, kBlack, regionDict[selection])

    if savePlot:
        canvas.Print('./totalSystematicPlot_SR_%s_%s.eps'%(baseAnalysis, selection))

    if not noCanvas:
        while True:
            a=1

if __name__=="__main__":

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("--baseAnalysis", action="store", type="string", dest="baseAnalysis", default="Stop", help="Analysis interpretation")
    parser.add_option("--selection", type="string", action="store", dest="selection", default='A6', help="Selection")
#    parser.add_option("--directory", action="store", type="string", dest="directory", default=os.getenv('ANALYSISROOTFILES')+'/Material_new/Tables/', help="HistFitter directory")
    parser.add_option("--directory", action="store", type="string", dest="directory", default='./', help="directory")
    parser.add_option("--noCanvas", action="store_true", dest="doNoCanvas", default=False, help="Not show the canvas")
    parser.add_option("--savePlot", action="store_true", dest="savePlot", default=False, help="Do save the plot")

    (options, args) = parser.parse_args()


    baseAnalysis   = options.baseAnalysis
    selection      = options.selection
    directory      = options.directory
    noCanvas       = options.doNoCanvas
    savePlot       = options.savePlot

    if noCanvas:
        ROOT.gROOT.SetBatch(1)

    fileName = directory+"SysMethod2_%s_%s_SR.tex" % (baseAnalysis, selection)
    
    systeDictPercent = extractSystematics(fileName=fileName)
    plotErrors(systeDictPercent=systeDictPercent, selection=selection, savePlot=savePlot)
