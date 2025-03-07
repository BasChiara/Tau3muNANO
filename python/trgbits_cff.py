import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

Path2022=["HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1","HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15","HLT_DoubleMu4_3_LowMass"]
#Path2022=["HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1","HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"]
Path = Path2022

trgTable = cms.EDProducer( "TrgBitTableProducer",
                          hltresults = cms.InputTag("TriggerResults::HLT"),
                          paths      = cms.vstring(Path),
)

trgTables = cms.Sequence(trgTable)



