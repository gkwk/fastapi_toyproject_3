import os
import time
from logging.handlers import TimedRotatingFileHandler


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def getFilesToDelete(self):
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        baseName_split_list = baseName.split(".")

        prefix = baseName_split_list[0] + "."
        plen = len(prefix)
        for fileName in fileNames:
            if self.namer is None:
                if not fileName.startswith(prefix):
                    continue
            else:
                if (
                    not fileName.startswith(baseName)
                    and len(fileName) > (plen + 1)
                    and not fileName[plen + 1].isdigit()
                ):
                    continue

            if fileName[:plen] == prefix:
                suffix = fileName[plen:]

                parts = suffix.split(".")
                for part in parts:
                    if self.extMatch.match(part):
                        result.append(os.path.join(dirName, fileName))
                        break

        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[: len(result) - self.backupCount]

        return result

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)

        # 저장명 커스텀
        dirName, baseName = os.path.split(self.baseFilename)
        baseName_list = baseName.split(".")
        baseName_list.insert(1, time.strftime(self.suffix, time.localtime(currentTime)))

        dfn = self.rotation_filename(os.path.join(dirName, ".".join(baseName_list)))

        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        if (self.when == "MIDNIGHT" or self.when.startswith("W")) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:
                    addend = -3600
                else:
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
