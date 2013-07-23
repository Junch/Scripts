from xml.etree import ElementTree
import argparse

class BMTest: # Benchmark Test
    def __init__(self, macrofile):
        self.macrofile = macrofile

    def analyse(self):
        self.treeResponse = ElementTree.parse(self.macrofile)
        self.actions = self.treeResponse.find("Actions")

        leftdowns = []
        for i, action in enumerate(self.actions):
            type = action.get("{http://www.w3.org/2001/XMLSchema-instance}type")
            flags = action.get("Flags")
            if (type  == "UIMouseAction" and \
                flags == "LEFTDOWN"):
                x = action.get("X")
                y = action.get("Y")
                leftdowns.append((i, int(x), int(y)))
        #print(leftdowns)
        
        maxspan = -1
        index = -1
        for i, item in enumerate(leftdowns):
            if (i > 0):
                span = item[0] - leftdowns[i-1][0]
                if maxspan < span:
                    maxspan = span
                    index = i-1

        self.result = (leftdowns[index][0], maxspan, (leftdowns[index][1],leftdowns[index][2]), (leftdowns[index+1][1], leftdowns[index+1][2]))
        print("Start=%d, Maxspan=%d" % (self.result[0], self.result[1]))
        print("x0=%d, y0=%d" % (self.result[2][0], self.result[2][1]))
        print("x1=%d, y1=%d" % (self.result[3][0], self.result[3][1]))

    def interpolate(self, steps):
        start = self.result[0]
        span  = self.result[1]
        pt0   = self.result[2]
        pt1   = self.result[3]

        #self.treeResponse.write("origin.Macro")
        for action in self.actions[start+2: start+span]:
            self.actions.remove(action)

        xlen = (pt1[0]-pt0[0])/steps
        ylen = (pt1[1]-pt0[1])/steps
        for i in range(steps+1):
            e = self.actions[start+1].copy()
            e.set("Flags", "MOVE")
            e.set("ResponseTime", "10")
            x = pt1[0] - xlen*i
            y = pt1[1] - ylen*i
            e.set("X", str(int(x)))
            e.set("Y", str(int(y)))
            self.actions.insert(start+2, e)
        self.treeResponse.write("result.Macro")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interpolate the .Macro file for the MOVE message')
    parser.add_argument('-f', '--f', help='Specify the .Macro file', required=True)
    parser.add_argument('-step', '--step', type=int, help="Specify the number of the MOVE message in the main operation", required=True)
    args = parser.parse_args()

    #test = BMTest("TrimSimple.Macro")
    test = BMTest(args.f)
    test.analyse()
    test.interpolate(args.step)
