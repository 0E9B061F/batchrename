import sys, os, shutil, fnmatch
from PyQt4 import QtCore, QtGui
from ui_batchrename import Ui_BatchRename


class BatchRename(QtGui.QWidget):
    def __init__(self):
        super(BatchRename, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_BatchRename()
        self.ui.setupUi(self)

        self.count = 0

        self.directory = os.getcwd()
        self.basename  = "renamed"

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


    def setBasename(self):
        self.ui.basenameInput.setText(self.basename)

    def setDirectory(self):
        self.ui.directoryInput.setText(self.directory)

    def outputDir(self):
        subdir = "renamed"
        return os.path.join(self.directory, subdir)

    def renameFile(self, path):
        ext    = os.path.splitext(path)[1]
        name   = self.basename + "-" + str(self.count) + ext
        self.count += 1
        return os.path.join(self.outputDir(), name)

    def updatePreview(self):
        files = self.listFiles()

        self.targetList.clear()
        for path in files:
            self.targetList.append(path)
        self.targetListModel.setStringList(self.targetList)

        self.outputList.clear()
        self.count = 0
        for path in files:
            path = self.renameFile(path)
            self.outputList.append(path)
        self.outputListModel.setStringList(self.outputList)

    def listFiles(self, match="*"):
        return [ x for x in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, x)) ]

    def rename(self):
        print("renaming")
        files = self.listFiles()
        try:
            os.mkdir(self.outputDir())
        except:
            pass
        self.count = 0
        for f in files:
            r = self.renameFile(f)
            self.ui.operationInput.text = f
            self.ui.operationOutput.text = r
            self.ui.progressLabel.text = str(self.count) + "/" + str(len(files))
            f = os.path.join(self.directory, f)
            r = os.path.join(self.outputDir(), r)
            shutil.copyfile(f, r)

    def changeDirectory(self):
        self.directory = str(self.ui.directoryInput.text())
        self.updatePreview()
        print("change dir")

    def browseDirectory(self):
        print("browsing")

    def changeBasename(self):
        self.basename = str(self.ui.basenameInput.text())
        self.updatePreview()
        print("basename changed")


def main():
    app = QtGui.QApplication(sys.argv)
    br  = BatchRename()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

