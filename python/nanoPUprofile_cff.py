from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.globals_cff import *
from PhysicsTools.NanoAOD.nano_cff import *
from PhysicsTools.NanoAOD.vertices_cff import *
from PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff import *
from PhysicsTools.Tau3muNANO.trgbits_cff import * # modified

from PhysicsTools.Tau3muNANO.genparticlesT3m_cff import * # define new



vertexTable.svSrc = cms.InputTag("slimmedSecondaryVertices")

nanoSequence = cms.Sequence(nanoMetadata + #nanoSequenceCommon + 
                            cms.Sequence(vertexTask) + 
                            cms.Sequence(vertexTablesTask) +
                            cms.Sequence(globalTablesTask) +
                            cms.Sequence(metMCTask)+ 
                            cms.Sequence(globalTablesMCTask) + # PU information here 
                            cms.Sequence(genWeightsTableTask)
                            #triggerObjectTau3MuTables +  
                            #l1bits
)


def nanoAOD_customizePU(process):
    process.nanoSequence = cms.Sequence( process.nanoSequence)
    return process
