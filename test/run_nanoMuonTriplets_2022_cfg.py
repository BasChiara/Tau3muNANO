from FWCore.ParameterSet.VarParsing import VarParsing
import FWCore.ParameterSet.Config as cms

options = VarParsing('python')

options.register('isMC', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)
options.register('isPreECALleakage',True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Data taken during ECAL leakage"
)
options.register('globalTag', 'NOTSET',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Set global tag"
)
options.register('wantSummary', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)
options.register('wantFullRECO', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)
options.register('reportEvery', 100,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "report every N events"
)
options.register('skip', 0,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "skip first N events"
)

#options.setDefault('maxEvents', -1)
options.setDefault('maxEvents', 1000)
tag = '2022' if options.isPreECALleakage else '2022EE'
options.setDefault('tag', tag)
options.parseArguments()

# global tags:
#    (!) december 2023 - reminiAOD for eras 
# MC pre ECAL leakage  : 130X_mcRun3_2022_realistic_v5           
# MC post ECAL leakage : 130X_mcRun3_2022_realistic_postEE_v6    
# 2022 ABCDE ReReco    : 130X_dataRun3_v2                        # for the time being, not available in 130X for parking
# 2022 FG Prompt       : 130X_dataRun3_PromptAnalysis_v1
if not options.isMC :
    globaltag = '124X_dataRun3_v11'
 
else :
    globaltag = '124X_mcRun3_2022_realistic_v12' if options.isPreECALleakage else '124X_mcRun3_2022_realistic_postEE_v1'


if options._beenSet['globalTag']:
    globaltag = options.globalTag

extension = {False : 'data', True : 'mc'}
outputFileNANO = cms.untracked.string('_'.join(['tau3muNANO', extension[options.isMC], options.tag])+'.root')
outputFileFEVT = cms.untracked.string('_'.join(['xFullEvt', extension[options.isMC], options.tag])+'.root')
if not options.inputFiles :
    if options.isMC :
        # signal channel
        options.inputFiles = ['/store/mc/Run3Summer22MiniAODv3/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v2/2820000/0b14e03f-168c-4e39-b441-d1b949ee4890.root'] if options.isPreECALleakage else \
                            ['/store/mc/Run3Summer22EEMiniAODv3/WtoTauNu_Tauto3Mu_TuneCP5_13p6TeV_pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2810000/975d40c3-629d-41e5-8887-cb34ca21e308.root'] 
                            
        # control channel
        #options.inputFiles = ['/store/mc/Run3Summer22MiniAODv3/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v2/2810000/0da9edba-f8b9-4e0c-8be1-282cdd2b5685.root'] if options.isPreECALleakage else \
        #                     ['/store/mc/Run3Summer22EEMiniAODv3/DstoPhiPi_Phito2Mu_MuFilter_TuneCP5_13p6TeV_pythia8-evtgen/MINIAODSIM/124X_mcRun3_2022_realistic_postEE_v1-v2/2810000/00589525-be33-4abd-af78-428bb9ace158.root']


    else :
        options.inputFiles =  ['/store/data/Run2022D/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/30000/04eef6b0-bbab-4c97-abf2-001d452dc794.root',
                                 '/store/data/Run2022D/ParkingDoubleMuonLowMass0/MINIAOD/10Dec2022-v2/30000/0794dd66-bc41-4ff3-b0a9-676c7ad56949.root']
annotation = '%s nevts:%d' % (outputFileNANO, options.maxEvents)

#from Configuration.StandardSequences.Eras import eras
process = cms.Process('Tau3muNANO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
#process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.Tau3muNANO.nanoTau3Mu_cff')
process.load('PhysicsTools.Tau3muNANO.nanoDsPhiMuMuPi_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents=cms.untracked.uint32(options.skip),
)
process.options = cms.untracked.PSet(
    #Rethrow 
    SkipEvent = cms.untracked.vstring('ProductNotFound'),
    wantSummary = cms.untracked.bool(options.wantSummary),
)

process.nanoMetadata.strings.tag = annotation
# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string(annotation),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = outputFileNANO,
    outputCommands = cms.untracked.vstring(
      'drop *',
      "keep nanoaodFlatTable_*Table_*_*",     # event data
      "keep nanoaodUniqueString_nanoMetadata_*_*",   # basic metadata
    )

)


# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, globaltag, '')

from PhysicsTools.Tau3muNANO.nanoTau3Mu_cff import *
from PhysicsTools.Tau3muNANO.nanoDsPhiMuMuPi_cff import *
process = nanoAOD_customizeTrackTau3Mu(process)
process = nanoAOD_customizeMuonTriggerTau3Mu(process)
process = nanoAOD_customizeWnuTau3Mu(process)
process = nanoAOD_customizeDsPhiMuMuPi(process)
process = nanoAOD_customizeTriggerBitsTau3Mu(process)

# Path and EndPath definitions
process.nanoAOD_TauTo3mu_step = cms.Path(process.nanoSequence + process.nanoWnuTau3MuSequence )
process.nanoAOD_DsPhiMuMuPi_step = cms.Path(process.nanoDsPhiMuMuPi )

# customisation of the process.
if options.isMC:
    from PhysicsTools.Tau3muNANO.nanoTau3Mu_cff import nanoAOD_customizeMC
    nanoAOD_customizeMC(process)

process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(
                                process.nanoAOD_TauTo3mu_step,
                                process.nanoAOD_DsPhiMuMuPi_step,
                                process.endjob_step,
                                process.NANOAODoutput_step
                               )

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

process.NANOAODoutput.SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring(
                                   'nanoAOD_TauTo3mu_step', 'nanoAOD_DsPhiMuMuPi_step'
                                   )
)


process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
process.NANOAODoutput.fakeNameForCrab=cms.untracked.bool(True)    

process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
