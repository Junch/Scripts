import sys
import os
from xml.etree import ElementTree
from xml.dom.minidom import parse, parseString
import argparse

class BMReport:
    def __init__(self):
        self._Data = ElementTree.ElementTree()
        self.Root = ElementTree.Element('UIMacro')
        self._Data._setroot(self.Root)

    def dump(self):
        ElementTree.dump(self._Data)

    def output(self, reportfile):
        fp = open(reportfile, "w")
        fp.write("<?xml version=\"1.0\" ?>\n")
        fp.write("<UIMacro>\n")

        items = ["Build", "Benchmark", "Scenario", "Test", "Index", "Key", "ResponseTime", "FPS"]
        actions = self._Data.findall("UIAction")
        for action in actions:
            s = "    <UIAction"
            for item in items:
                s += " %s=\"%s\"" %(item , action.get(item))
            s += "/>\n"
            fp.write(s)

        fp.write("</UIMacro>")
        fp.close()

class BMTest: # Benchmark Test
    def __init__(self, report, resfile):
        self.ResponseFile = resfile
        self.Benchmark = "CommandPreview"
        self.Build = "BuildVer"
        self.Scenario = "Scenario"
        self.Test = "Test"
        self.Report = report

    def appendActions(self):
        root = self.Report.Root

        treeResponse = ElementTree.parse(self.ResponseFile)
        actions = treeResponse.find("Actions")

        index = 1
        for action in actions:
            attribs = dict()
            attribs["Build"] = self.Build
            attribs["Benchmark"] = self.Benchmark
            attribs["Scenario"]  = self.Scenario
            attribs["Test"]  = self.Test
            attribs["Index"] = str(index)
            index += 1

            attribs["ResponseTime"] = action.get("ResponseTime")
            attribs["FPS"] = action.get("FPS")

            flags = action.get("Flags")
            if flags == None:
                flags = ""
            flags = "%s@" % flags
            attribs["Key"] = flags
            ElementTree.SubElement(root, "UIAction", attribs)

class BMCommandPreview:
    def Run(self, resultDir, reportFile, buildVer):
        report = BMReport()
        for parent, dirnames, filenames in os.walk(resultDir):
            for filename in filenames:
                pair = os.path.splitext(filename)
                if pair[1] == ".response":
                    filepath = os.path.join(parent, filename)
                    test = BMTest(report, filepath)
                    test.Build = buildVer
                    test.Scenario = os.path.split(parent)[-1]
                    test.Test = pair[0]
                    test.appendActions()
                    print("Processed: " + filepath)

        report.output(reportFile)

if __name__ == "__main__":
    # -dir -build -o
    parser = argparse.ArgumentParser(description='Process the benchmark result of the CommandPreview.')
    parser.add_argument('-dir', '--dir', help='Specify the bmr dir of CommandPreview') #required=True
    parser.add_argument('-build', '--build', help='Specify the build version of AutoCAD', default='BuildVer')
    parser.add_argument('-o', '--o', help='Specify the output file', default='CommandPreview.xml')
    args = parser.parse_args()

    if args.dir == None:
        args.dir = os.getcwd()

    print("-"*40)
    print("Dir: " + args.dir)
    print("Build: " + args.build)
    print("Output: " + args.o)
    print("-"*40)

    bmcp = BMCommandPreview()
    bmcp.Run(args.dir, args.o, args.build)