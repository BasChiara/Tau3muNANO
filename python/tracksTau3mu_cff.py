import FWCore.ParameterSet.Config as cms
from PhysicsTools.Tau3muNANO.common_cff import *

Path2022=["HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1","HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"]
Path=Path2022

trackTrgSelector = cms.EDProducer("TrackTriggerSelector",
                                  beamSpot   = cms.InputTag("offlineBeamSpot"),
                                  tracks     = cms.InputTag("packedPFCandidates"),
                                  lostTracks = cms.InputTag("lostTracks"),
                                  ## trigger match  
                                  bits = cms.InputTag("TriggerResults","","HLT"), 
                                  objects = cms.InputTag("slimmedPatTrigger"), 
                                  drForTriggerMatch = cms.double(0.1), 
                                  HLTPaths=cms.vstring(Path),
                                  #
                                  trkPtCut = cms.double(1.0),
                                  trkEtaCut = cms.double(2.6),
                                  muons      = cms.InputTag("slimmedMuons"),
                                  vertices   = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                  trkNormChiMin = cms.int32(-1),
                                  trkNormChiMax = cms.int32(-1)
                              )

trackT3mTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
                               src = cms.InputTag("trackTrgSelector:SelectedTracks"),
                               cut = cms.string(""), 
                               name = cms.string("ProbeTracks"),
                               doc  = cms.string("track collection after basic selection"),
                               singleton = cms.bool(False),         
                               extension = cms.bool(False),         
                               variables = cms.PSet(PTVars, 
                               nValidHits = Var("userInt('nValidHits')",float,doc="N. valid hits"), 
                               dZpv = Var("userFloat('dZpv')",float,doc="long distance from PV"),
                               err_dZpv = Var("userFloat('err_dZpv')",float,doc="long error from PV"),
                               drForHLT = Var("userFloat('drForHLT')",float,doc="BS compatibility"),
                                                )
)

trackT3mMCMatchForTable = cms.EDProducer("MCMatcher",   
    src         = trackT3mTable.src,         
    matched     = cms.InputTag("finalGenParticlesT3m"), 
    mcPdgId     = cms.vint32(211),
    checkCharge = cms.bool(False),     
    mcStatus    = cms.vint32(1),
    maxDeltaR   = cms.double(0.03),      
    maxDPtRel   = cms.double(0.5),       
    resolveAmbiguities = cms.bool(True),       
    resolveByMatchQuality = cms.bool(True),    
)

trackT3mMCMatchEmbedded = cms.EDProducer(
    'CompositeCandidateMatchEmbedder',
    src = trackT3mTable.src,
    matching = cms.InputTag("tracksT3mMCMatchForTable")
)

trackT3mMCTable = cms.EDProducer("CandMCMatchTableProducerT3m",
    src     = trackT3mTable.src,
    mcMap   = cms.InputTag("trackT3mMCMatchForTable"),
    objName = trackT3mTable.name,
    objType = trackT3mTable.name, 
    branchName = cms.string("genPart"),
    docString = cms.string("MC matching to status==1 pions"),
)

trackT3mSequence = cms.Sequence(trackTrgSelector)
trackT3mTables = cms.Sequence(trackT3mTable)
trackT3mMC = cms.Sequence(trackT3mSequence + trackT3mMCMatchForTable + trackT3mMCMatchEmbedded + trackT3mMCTable)
