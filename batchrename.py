import sys, os, shutil, fnmatch
from PyQt4 import QtCore, QtGui
from ui_batchrename import Ui_BatchRename


class BatchRename(QtGui.QWidget):
    def __init__(self):
        super(BatchRename, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_BatchRename()
        self.ui.setupUi(self)

        self.count  = 0
        self.subdir = "batchrename"

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
        self.resetProgress()

        self.show()


    def pad(self, num):
        return '%03d' % num

    def setBasename(self):
        self.ui.basenameInput.setText(self.basename)

    def setDirectory(self):
        self.ui.directoryInput.setText(self.directory)

    def outputDir(self):
        return os.path.join(self.directory, self.subdir)

    def genFilename(self, path):
        ext  = os.path.splitext(path)[1]
        name =  self.basename + "-" + self.pad(self.count) + ext
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
        self.count = 1
        for path in files:
            path = os.path.join(self.subdir, self.genFilename(path))
            self.outputList.append(path)
            self.count += 1
        self.outputListModel.setStringList(self.outputList)

    def updateProgress(self):
        files = self.listFiles()
        fileCount = len(files)
        self.ui.progressLabel.setText(self.pad(self.count) + "/" + self.pad(fileCount))
        self.ui.progressBar.setValue(100 * (self.count / fileCount))

    def resetProgress(self):
        self.count = 1
        self.updateProgress()
        self.ui.operationInput.setText("")
        self.ui.operationOutput.setText("")

    def listFiles(self, match="*"):
        return [ x for x in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, x)) ]

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
        self.count = 1
        for f in files:
            r = self.renameFile(f)
            fabs = os.path.join(self.directory, f)
            rabs = os.path.join(self.outputDir(), r)
            shutil.copyfile(fabs, rabs)
            self.ui.operationInput.setText(f)
            self.ui.operationOutput.setText(self.relativeFilename(f))
            self.updateProgress()
            self.count += 1

    def changeDirectory(self):
        self.directory = str(self.ui.directoryInput.text())
        self.updatePreview()
        self.resetProgress()

    def browseDirectory(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        if (dialog.exec_()):
            self.ui.directoryInput.setText(dialog.selectedFiles()[0])
            self.changeDirectory()

    def changeBasename(self):
        self.basename = str(self.ui.basenameInput.text())
        self.updatePreview()
        self.resetProgress()


def main():
    os.chdir("testdir")
    app = QtGui.QApplication(sys.argv)
    br  = BatchRename()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

