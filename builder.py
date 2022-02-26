import json
import copy


class Parameters:
    def __init__(self, testID, refnum, api, platform, testFileName, deadlineForStonewall, stoneWallingWearOut,
                 maxTimeDuration, outlierThreshold,
                 options, dryRun, nodes, memoryPerTask, memoryPerNode, tasksPerNode, repetitions, multiFile,
                 interTestDelay, fsync, fsyncperwrite, useExistingTestFile, uniqueDir, singleXferAttempt,
                 readFile, writeFile, filePerProc, reorderTasks, reorderTasksRandom, reorderTasksRandomSeed,
                 randomOffset, checkWrite, checkRead, dataPacketType, keepFile, keepFileWithError, warningAsErrors,
                 verbose, collective, segmentCount, transferSize,
                 blockSize):
        self.testID = testID
        self.refnum = refnum
        self.api = api
        self.platform = platform
        self.testFileName = testFileName
        self.deadlineForStonewall = deadlineForStonewall
        self.stoneWallingWearOut = stoneWallingWearOut
        self.maxTimeDuration = maxTimeDuration
        self.outlierThreshold = outlierThreshold
        self.options = options
        self.dryRun = dryRun
        self.nodes = nodes
        self.memoryPerTask = memoryPerTask
        self.memoryPerNode = memoryPerNode
        self.tasksPerNode = tasksPerNode
        self.repetitions = repetitions
        self.multiFile = multiFile
        self.interTestDelay = interTestDelay
        self.fsync = fsync
        self.fsyncperwrite = fsyncperwrite
        self.useExistingTestFile = useExistingTestFile
        self.uniqueDir = uniqueDir
        self.singleXferAttempt = singleXferAttempt
        self.readFile = readFile
        self.writeFile = writeFile
        self.filePerProc = filePerProc
        self.reorderTasks = reorderTasks
        self.reorderTasksRandom = reorderTasksRandom
        self.reorderTasksRandomSeed = reorderTasksRandomSeed
        self.randomOffset = randomOffset
        self.checkWrite = checkWrite
        self.checkRead = checkRead
        self.dataPacketType = dataPacketType
        self.keepFile = keepFile
        self.keepFileWithError = keepFileWithError
        self.warningAsErrors = warningAsErrors
        self.verbose = verbose
#        self.data_packet_type = data_packet_type
#       self.setTimeStampSignature_incompressibleSeed = setTimeStampSignature_incompressibleSeed
        self.collective = collective
        self.segmentCount = segmentCount
        self.transferSize = transferSize
        self.blockSize = blockSize


    # @staticmethod
    # def create_from_json(json_dictionary):
    #     # json_dictionary = json.loads(data.read())
    #     p = json_dictionary['tests'][0]['Parameters']
    #     return Parameters(**p)


class Summary:
    def __init__(self, operation, API, TestID, ReferenceNumber, segmentCount, blockSize, transferSize, numTasks,
                 tasksPerNode, repetitions, filePerProc, reorderTasks, taskPerNodeOffset, reorderTasksRandom,
                 reorderTasksRandomSeed,
                 bwMaxMIB, bwMinMIB, bwMeanMIB, bwStdMIB, OPsMax, OPsMin, OPsMean, OPsSD, MeanTime, xsizeMiB):
        self.operation = operation
        self.API = API
        self.TestID = TestID
        self.ReferenceNumber = ReferenceNumber
        self.segmentCount = segmentCount
        self.blockSize = blockSize
        self.transferSize = transferSize
        self.numTasks = numTasks
        self.tasksPerNode = tasksPerNode
        self.repetitions = repetitions
        self.filePerProc = filePerProc
        self.reorderTasks = reorderTasks
        self.taskPerNodeOffset = taskPerNodeOffset
        self.reorderTasksRandom = reorderTasksRandom
        self.reorderTasksRandomSeed = reorderTasksRandomSeed
        self.bwMaxMIB = bwMaxMIB
        self.bwMinMIB = bwMinMIB
        self.bwMeanMIB = bwMeanMIB
        self.bwStdMIB = bwStdMIB
        self.OPsMax = OPsMax
        self.OPsMin = OPsMin
        self.OPsMean = OPsMean
        self.OPsSD = OPsSD
        self.MeanTime = MeanTime
        self.xsizeMiB = xsizeMiB

    # @staticmethod
    # def create_from_json(json_dictionary):
    #     summaries = []
    #     for summary in json_dictionary['summary']:
    #         summaries.append(Summary(**summary))
    #     return summaries


class Result:
    def __init__(self, access, bwMiB, blockKiB, xferKiB, iops, latency, openTime, wrRdTime,
                 closeTime, totalTime):
        self.access = access
        self.bwMiB = bwMiB
        self.blockKiB = blockKiB
        self.xferKiB = xferKiB
        self.iops = iops
        self.latency = latency
        self.openTime = openTime
        self.wrRdTime = wrRdTime
        self.closeTime = closeTime
        self.totalTime = totalTime

    # @staticmethod
    # def create_from_json(json_dictionary):
    #     results = []
    #     for result in json_dictionary['tests'][0]['Results']:
    #         results.append(Result(**result))
    #     return results


class Test:
    def __init__(self, test_id, start_time, path, used_capacity, inodes, used_inodes, parameters, options,
                 results, finished):
        self.TestID = test_id
        self.StartTime = start_time
        self.Path = path
        self.Used_Capacity = used_capacity
        self.Inodes = inodes
        self.Used_Inodes = used_inodes
        self.Parameters = parameters
        self.Options = options
        self.Results = results
        self.Finished = finished


class Builder:
    def create_from_json(json_dictionary):
        results = []
        summaries = []
        for result in json_dictionary['tests'][0]['Results']:
            results.append(Result(**result))
        for summary in json_dictionary['summary']:
            summaries.append(Summary(**summary))
        p = json_dictionary['tests'][0]['Parameters']
        p.pop('data packet type')
        p.pop('setTimeStampSignature/incompressibleSeed')
        cmd = json_dictionary['Command line']
        ts = json_dictionary['Began']
        te = json_dictionary['Finished']
        return PerformanceModel(cmd, ts, te, Parameters(**p), summaries, results)


class PerformanceModel:
    def __init__(self, cmd, ts, te, parameters, summaries, results):
        self.id = 0
        self.cmd = cmd
        self.ts = ts
        self.te = te
        self.parameters = parameters
        self.summaries = summaries
        self.results = results
