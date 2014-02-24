import sys, os, shutil, fnmatch, glob, subprocess, platform
from PyQt4 import QtCore, QtGui
from ui_batchrename import Ui_BatchRename


class BatchRename(QtGui.QWidget):
    def __init__(self):
        super(BatchRename, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_BatchRename()
        self.ui.setupUi(self)

        self.count      = 0
        self.subdir     = "renamed"
        self.safety     = True
        self.padding    = 3
        self.startAt    = 1
        self.fileFilter = "*.jpg *.jpeg *.tif *.tiff *.png *.raw *.gif"

        self.directory = os.getcwd()
        self.basename  = "file"

        self.setBasename()
        self.setDirectory()

        self.targetList      = QtCore.QStringList()
        self.targetListModel = QtGui.QStringListModel(self.targetList)
        self.ui.previewTargets.setModel(self.targetListModel)

        self.outputList      = QtCore.QStringList()
        self.outputListModel = QtGui.QStringListModel(self.outputList)
        self.ui.previewOutput.setModel(self.outputListModel)

        self.updatePreview()

        self.show()


    def pad(self, num):
        return str(num).zfill(self.padding)

    def setBasename(self):
        self.ui.basenameInput.setText(self.basename)

    def setDirectory(self):
        self.ui.directoryInput.setText(self.directory)

    def outputDir(self):
        return os.path.join(self.directory, self.subdir)

    def genFilename(self, path):
        ext  = os.path.splitext(path)[1]
        name =  self.basename + "-" + self.pad(self.count+self.startAt-1) + ext
        return name

    def relativeFilename(self, path):
        return os.path.join(self.subdir, self.genFilename(path))

    def renameFile(self, path):
        return os.path.join(self.outputDir(), self.genFilename(path))

    def updatePreview(self):
        files = self.listFiles()

        self.targetList.clear()
        for path in files:
            self.targetList.append(path)
        self.targetListModel.setStringList(self.targetList)

        self.outputList.clear()
        self.count = 0
        for path in files:
            self.count += 1
            path = os.path.join(self.subdir, self.genFilename(path))
            if os.path.exists(os.path.join(self.directory, path)):
                path = "[x] "+path
            else:
                path = "[ ] "+path

            self.outputList.append(path)
        self.outputListModel.setStringList(self.outputList)

    def filterFile(self, filename):
        return os.path.isfile(os.path.join(self.directory, filename))

    def uniq(self, seq, idfun=None):
        if idfun is None:
            def idfun(x): return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen: continue
            seen[marker] = 1
            result.append(item)
        return result

    def listFiles(self, match="*"):
        files = []
        for extglob in self.fileFilter.split(" "):
            fullglob = os.path.join(self.directory, extglob)
            files += glob.glob(fullglob)
        files = self.uniq(files)
        return [ f for f in files if self.filterFile(f) ]

    def rename(self):
        files = self.listFiles()
        try:
            shutil.rmtree(self.outputDir())
        except:
            pass
        try:
            os.mkdir(self.outputDir())
        except:
            pass
        self.count = 0
        for f in files:
            self.count += 1
            r = self.renameFile(f)
            fabs = os.path.join(self.directory, f)
            rabs = os.path.join(self.outputDir(), r)
            shutil.copyfile(fabs, rabs)
        self.updatePreview()

    def changeDirectory(self):
        self.directory = str(self.ui.directoryInput.text())
        self.updatePreview()

    def browseDirectory(self):
        browse = QtGui.QFileDialog(self)
        browse.setDirectory(self.directory)
        browse.setFileMode(QtGui.QFileDialog.Directory)
        if (browse.exec_()):
            self.directory = str(browse.selectedFiles()[0])
            self.ui.directoryInput.setText(self.directory)
            self.updatePreview()

    def changeBasename(self):
        self.basename = str(self.ui.basenameInput.text())
        self.updatePreview()

    def updateFilter(self):
        self.fileFilter = str(self.ui.filterInput.text())
        self.updatePreview()

    def updatePadding(self):
        self.padding = int(self.ui.paddingInput.text())
        self.updatePreview()

    def updateStart(self):
        self.startAt = int(self.ui.startAtInput.text())
        self.updatePreview()

    def toggleSafety(self):
        self.safety = not self.safety
        if self.safety:
            self.ui.renameButton.setEnabled(True)
        else:
            self.ui.renameButton.setEnabled(False)

    def openOutputDir(self):
        platformType = platform.system()
        if platformType == "Linux":
            subprocess.Popen(["xdg-open", self.outputDir()])
        elif platformType == "Windows":
            subprocess.Popen(["start", self.outputDir()], shell=True)

    def cleanup(self):
        try:
            shutil.rmtree(self.outputDir())
        except:
            pass
        self.updatePreview()

    def doExit(self):
        exit()


def main():
    app = QtGui.QApplication(sys.argv)
    br  = BatchRename()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

