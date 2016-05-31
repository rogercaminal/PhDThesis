import urllib2, urllib, os, subprocess, sys, commands, math, time, operator
from optparse import OptionParser, OptionGroup


def checkCoincidences(directory, chapterList, what):
    #--- Get all the reference labels
    reflabels = {}
    for chapter in chapterList:
        labelfile = open(directory+'/%s/%s.tex'%(chapter, chapter))
        lines = labelfile.readlines()
        labelfile.close()
  
        for l in lines:
            if '\\label' in l:
                reflabels[l.split('{')[1].split('}')[0]] = chapter

    #--- Get all the bibliography labels
    citelabels = {}
    for chapter in chapterList:
        labelfile = open(directory+'/Bibliography/mybib.bib')
        lines = labelfile.readlines()
        labelfile.close()
  
        for l in lines:
            if (('@article' in l) or ('@misc' in l) or ('@book' in l)):
                citelabels[l.split('{')[1].split(',')[0]] = chapter

    #--- Get all the reference calls
    if what=="references":
        refNotFound = []
        refcalls = {}
        for chapter in chapterList:
            reffile = open(directory+'/%s/%s.tex'%(chapter, chapter))
            lines = reffile.readlines()
            reffile.close()

            for l in lines:
                if '\\ref' in l:
                    refcalls[l[l.find("\\ref{")+5:l.find("}")]] = chapter

        for ref in refcalls.keys():
            if ref not in reflabels.keys():
                print str(ref).ljust(50),
                print 'called in chapter %s is not found' % (refcalls[ref])

    #--- Get all the cite calls
    elif what=="cites":
        citeNotFound = []
        citecalls = {}
        for chapter in chapterList:
            citefile = open(directory+'/%s/%s.tex'%(chapter, chapter))
            lines = citefile.readlines()
            citefile.close()

            for l in lines:
                if '\\cite' in l:
                    argument = l[l.find("\\cite{")+6:l.find("}")]
                    for arg in argument.split(','):
                        citecalls[arg.replace(' ','')] = chapter

        for cite in citecalls.keys():
            if cite not in citelabels.keys():
                print str(cite).ljust(50),
                print 'called in chapter %s is not found' % (citecalls[cite])


if __name__=="__main__":

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-v","--verbose", action="store_true", dest="doVerbose", default=False, help="Set the program in verbose mode")
    parser.add_option("--directory", action="store", type="string", dest="directory", default="./", help="Set the directory of the thesis")
    parser.add_option("--chapters", action="store", type="string", dest="chapters", default=None, help="Set the chapters to look at")

    (options, args) = parser.parse_args()

    doVerbose = options.doVerbose
    directory = options.directory
    chapters  = options.chapters

    chapterList = []
    if chapters==None:
        chapterList.append("Introduction")
        chapterList.append("StandardModel")
        chapterList.append("BeyondSM")
        chapterList.append("StatisticalModel")
        chapterList.append("ATLASdetector")
        chapterList.append("ObjectReconstruction")
        chapterList.append("MonojetAnalysis")
        chapterList.append("Interpretations")
        chapterList.append("Conclusions")
        chapterList.append("Appendix_FitResults")
        chapterList.append("Appendix_PlotsSR")
        chapterList.append("Appendix_BosonPtReweight")
        chapterList.append("Appendix_JetSmearingMethod")
        chapterList.append("Appendix_FluctuationM6")
        chapterList.append("Appendix_ClosureTestZnunu")
        chapterList.append("Appendix_CharmTagged")
    else:
        chapterList = chapters.split(',')

    checkCoincidences(directory=directory, chapterList=chapterList, what="references")
    checkCoincidences(directory=directory, chapterList=chapterList, what="cites")
