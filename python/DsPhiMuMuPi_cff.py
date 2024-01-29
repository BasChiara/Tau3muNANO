import FWCore.ParameterSet.Config as cms
from PhysicsTools.Tau3muNANO.common_cff import *
from PhysicsTools.NanoAOD.met_cff import *
from PhysicsTools.Tau3muNANO.HLTpathsT3m_cff import Path_Tau3Mu2022

########## inputs preparation ################

Path2022=["HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1","HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"]#,"HLT_DoubleMu4_3_LowMass"]
Path= Path_Tau3Mu2022

# Ds+ -> Phi(MuMu) Pi+
DsPhiMuMuPiForTau3Mu = cms.EDProducer('DsPhiMuMuPiBuilder',
    # sources muons & tracks
    muons               = cms.InputTag('triMuonTrgSelector:SelectedMuons'),
    muonsTransientTracks= cms.InputTag('triMuonTrgSelector:SelectedTransientMuons'),
    tracks              = cms.InputTag('trackTrgSelector:SelectedTracks'),
    tracksTransientTracks= cms.InputTag('trackTrgSelector:SelectedTransientTracks'),
    packedCandidatesSrc = cms.InputTag('packedPFCandidates'),
    beamSpot            = cms.InputTag("offlineBeamSpot"),
    vertices            = cms.InputTag("offlineSlimmedPrimaryVertices"),
    bits                = cms.InputTag("TriggerResults","","HLT"), 
    objects             = cms.InputTag("slimmedPatTrigger"),                                         
    # selection definition
    lep1Selection   = cms.string('isMediumMuon && ((abs(eta) <= 1.2 && pt > 3.5) || (abs(eta) > 1.2 && abs(eta) < 2.4 && pt > 2.0))'),
    lep2Selection   = cms.string('isMediumMuon && ((abs(eta) <= 1.2 && pt > 3.5) || (abs(eta) > 1.2 && abs(eta) < 2.4 && pt > 2.0))'),
    trackSelection  = cms.string('abs(eta) <= 3.0 && pt > 1.0'), 
    preVtxSelection = cms.string('mass() > 1.0 && mass() < 3.5 && abs(charge()) == 1'), # selection for Ds candidates pre-fit
    postVtxSelection= cms.string('userInt("vtx_isValid")'),
    minMuMu_mass    = cms.double(0.920), #GeV
    MaxMuMu_mass    = cms.double(1.120), #GeV
    # trigger
    HLTPaths          = cms.vstring(Path),                                                                        
    drForTriggerMatch = cms.double(0.1), 
    # isolation parameters
    isoRadius       = cms.double(0.4), # dR of the isolation cone
    isoRadiusForHLT = cms.double(0.8), # dR of the isolation cone applied at HLT level
    MaxDZForHLT     = cms.double(0.3), # dZ tau-track for isolation
    dBetaCone       = cms.double(0.8),
    dBetaValue      = cms.double(0.2), # optimised for Run2... check validity for Run3
)

# W -> Tau + MET

METfilters =[
        'Flag_goodVertices',
        'Flag_globalSuperTightHalo2016Filter',
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_BadPFMuonFilter',
        'Flag_BadPFMuonDzFilter',
        'Flag_hfNoisyHitsFilter',
        'Flag_eeBadScFilter',
        'Flag_ecalBadCalibFilter',
    ]

METforDsPhiPi = cms.EDProducer('TauPlusMETBuilder',
    src = cms.InputTag('DsPhiMuMuPiForTau3Mu', 'SelectedDs'),
    # input MET
    met = cms.InputTag('slimmedMETs'),
    PuppiMet = cms.InputTag('slimmedMETsPuppi'),
    #DeepMet = cms.InputTag('deepMetResolutionTuneTable','DeepMETResolutionTune'),
    # MET filters
    filter_bits = cms.InputTag("TriggerResults","","RECO"),
    filters     = cms.vstring(METfilters)
)


################################### Tables #####################################

DsPhiMuMuPiTable = cms.EDProducer('SimpleCompositeCandidateFlatTableProducer',
    src = cms.InputTag('DsPhiMuMuPiForTau3Mu', 'SelectedDs'),
    cut = cms.string(""),
    name = cms.string("DsPhiPi"),
    doc = cms.string("Ds+/- Variables"),
    singleton=cms.bool(False),
    extension=cms.bool(False),
    variables=cms.PSet(
        mu1_idx = uint('l1_idx'),
        mu2_idx = uint('l2_idx'),
        trk_idx = uint('trk_idx'),
        charge  = uint('charge'),
        mu1_charge = uint("mu1_charge"),
        mu2_charge = uint("mu2_charge"),
        trk_charge = uint("trk_charge"),
        
        MuMu_fitted_vtxX = ufloat("MuMu_fitted_vtxX"),
        MuMu_fitted_vtxY = ufloat("MuMu_fitted_vtxY"),
        MuMu_fitted_vtxZ = ufloat("MuMu_fitted_vtxZ"),
        MuMu_fitted_vtxEx = ufloat("MuMu_fitted_vtxEx"),
        MuMu_fitted_vtxEy = ufloat("MuMu_fitted_vtxEy"),
        MuMu_fitted_vtxEz = ufloat("MuMu_fitted_vtxEz"),
        MuMu_fitted_pt  = ufloat("MuMu_fitted_pt" ), 
        MuMu_fitted_eta = ufloat("MuMu_fitted_eta"),
        MuMu_fitted_phi = ufloat("MuMu_fitted_phi"),
        MuMu_fitted_mass = ufloat("MuMu_fitted_mass"),
        MuMu_fitted_mass_err2 = ufloat("MuMu_fitted_mass_err2"),

        vtx_prob = ufloat("vtx_prob"),
        vtx_chi2 = ufloat("vtx_chi2"),
        vtx_Ndof = ufloat("vtx_Ndof"),
        vtx_isValid = uint("vtx_isValid"),

        fitted_pt   = ufloat('fitted_pt'),
        fitted_eta  = ufloat('fitted_eta'),
        fitted_phi  = ufloat('fitted_phi'),
        fitted_mass = ufloat("fitted_mass"),
        fitted_mass_err2 = ufloat("fitted_mass_err2"),

        PV_x = ufloat('PV_x'),
        PV_y = ufloat('PV_y'),
        PV_z = ufloat('PV_z'),

        PVrefit_isValid = ufloat('PVrefit_isValid'), 
        PVrefit_chi2 = ufloat('PVrefit_chi2'), 
        PVrefit_ndof = ufloat('PVrefit_ndof'), 
        PVrefit_x = ufloat('PVrefit_x'),
        PVrefit_y = ufloat('PVrefit_y'),
        PVrefit_z = ufloat('PVrefit_z'),
        
        #diMuVtxFit_bestProb = ufloat("diMuVtxFit_bestProb"),
        #diMuVtxFit_bestMass = ufloat("diMuVtxFit_bestMass"),
        diMuVtxFit_toVeto   = uint("diMuVtxFit_toVeto"),

        iso_ptChargedFromPV = ufloat("iso_ptChargedFromPV"),
        iso_ptChargedFromPU = ufloat("iso_ptChargedFromPU"),
        iso_ptPhotons       = ufloat("iso_ptPhotons"),
        iso_ptChargedForHLT = ufloat("iso_ptChargedForHLT"),
        absIsolation        = ufloat("absIsolation"),

        iso_ptChargedFromPV_pT05 = ufloat("iso_ptChargedFromPV_pT05"),
        iso_ptChargedFromPU_pT05 = ufloat("iso_ptChargedFromPU_pT05"),
        iso_ptPhotons_pT05 = ufloat("iso_ptPhotons_pT05"),
        iso_ptChargedForHLT_pT05 = ufloat("iso_ptChargedForHLT_pT05"),
        absIsolation_pT05 = ufloat("absIsolation_pT05"),

        dZmu12 = ufloat('dZmu12'),
        #mu12_fit_mass = ufloat('mu12_fit_mass'),
        dZmu13 = ufloat('dZmu13'),
        #mu13_fit_mass = ufloat('mu13_fit_mass'),
        dZmu23 = ufloat('dZmu23'),
        #mu23_fit_mass = ufloat('mu23_fit_mass'),
        Lxy_3muVtxBS = ufloat('Lxy_3muVtxBS'),
        errLxy_3muVtxBS = ufloat('errLxy_3muVtxBS'),
        sigLxy_3muVtxBS = ufloat('sigLxy_3muVtxBS'),
        CosAlpha2D_LxyP3mu = ufloat('Cos2D_LxyP3mu'),

        fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 = uint("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1"),
        Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr = ufloat("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_dr"),
        fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 = uint("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"),
        Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr = ufloat("HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_dr"),

        mu1_pt = ufloat("mu1_pt"),
        mu1_eta = ufloat("mu1_eta"),
        mu1_phi = ufloat("mu1_phi"),
        mu1_dr = ufloat("mu1_drForHLT"),
        mu1_trackQuality = uint("mu1_trackQuality"),
        mu2_pt = ufloat("mu2_pt"),
        mu2_eta = ufloat("mu2_eta"),
        mu2_phi = ufloat("mu2_phi"),
        mu2_dr = ufloat("mu2_drForHLT"),
        mu2_trackQuality = uint("mu2_trackQuality"),
        trk_pt = ufloat("trk_pt"),
        trk_eta = ufloat("trk_eta"),
        trk_phi = ufloat("trk_phi"),
        trk_dr = ufloat("trk_drForHLT"),
        trk_trackQuality = uint("trk_trackQuality"),

        mu12_DCA   = ufloat("mu12_DCA"), 
        #mu12_vtxFitProb = ufloat("mu12_vtxFitProb"), 
        mu23_DCA   = ufloat("mu23_DCA"), 
        #mu23_vtxFitProb = ufloat("mu23_vtxFitProb"), 
        mu13_DCA   = ufloat("mu13_DCA"), 
        #mu13_vtxFitProb = ufloat("mu13_vtxFitProb"), 

        mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 = uint("mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1"),
        mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 = uint("mu1_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"),
        mu1_fired_DoubleMu4_3_LowMass = uint("mu1_fired_DoubleMu4_3_LowMass"),


        mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 = uint("mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1"),
        mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 = uint("mu2_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"),
        mu2_fired_DoubleMu4_3_LowMass = uint("mu2_fired_DoubleMu4_3_LowMass"),

        trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1 = uint("trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1"),
        trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15 = uint("trk_fired_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15"),
        trk_fired_DoubleMu4_3_LowMass = uint("trk_fired_DoubleMu4_3_LowMass"),
    )
)

DsPlusMetTable = cms.EDProducer('SimpleCompositeCandidateFlatTableProducer',
    src = cms.InputTag('METforDsPhiPi', 'builtWbosons'),
    cut = cms.string(""),
    name = cms.string("DsPlusMET"),
    doc = cms.string("Tau+MET Variables"),
    singleton=cms.bool(False),
    extension=cms.bool(False),
    variables=cms.PSet(
        charge = uint("charge"),
        mass_nominal   = ufloat("mass_nominal"),
        # MET filters
        Flag_goodVertices = uint('Flag_goodVertices'),
        Flag_globalSuperTightHalo2016Filter = uint('Flag_globalSuperTightHalo2016Filter'),
        Flag_EcalDeadCellTriggerPrimitiveFilter = uint('Flag_EcalDeadCellTriggerPrimitiveFilter'),
        Flag_BadPFMuonFilter   = uint('Flag_BadPFMuonFilter'),
        Flag_BadPFMuonDzFilter = uint('Flag_BadPFMuonDzFilter'),
        Flag_hfNoisyHitsFilter = uint('Flag_hfNoisyHitsFilter'),
        Flag_eeBadScFilter = uint('Flag_eeBadScFilter'),
        # PF MET type1 correction
        MET_pt   = ufloat('MET_pt'),
        Tau_mT   = ufloat('Tau_mT'),
        pt       = ufloat("pt"),
        eta_min      = ufloat("eta_min"),
        eta_max      = ufloat("eta_max"),
        phi      = ufloat("phi"),
        mass_min = ufloat('mass_min'),
        mass_max = ufloat('mass_max'),
        METminPz = ufloat('METminPz'),
        METmaxPz = ufloat('METmaxPz'),
        # Puppi correction to MET
        PuppiMET_pt  = ufloat('PuppiMET_pt'),
        Tau_Puppi_mT = ufloat('Tau_Puppi_mT'),
        Puppi_pt     = ufloat("Puppi_pt"),
        Puppi_eta_min    = ufloat("Puppi_eta_min"),
        Puppi_eta_max    = ufloat("Puppi_eta_max"),
        Puppi_phi    = ufloat("Puppi_phi"),
        Puppi_mass_min = ufloat('Puppi_mass_min'),
        Puppi_mass_max = ufloat('Puppi_mass_max'),
        PuppiMETminPz= ufloat('PuppiMETminPz'),
        PuppiMETmaxPz= ufloat('PuppiMETmaxPz'),
        # Deep MET correction
        DeepMET_pt  = ufloat('DeepMET_pt'),
        Tau_Deep_mT = ufloat('Tau_Deep_mT'),
        Deep_pt     = ufloat("Deep_pt"),
        Deep_eta_min    = ufloat("Deep_eta_min"),
        Deep_eta_max    = ufloat("Deep_eta_max"),
        Deep_phi    = ufloat("Deep_phi"),
        DeepMETminPz= ufloat('DeepMETminPz'),
        DeepMETmaxPz= ufloat('DeepMETmaxPz'),
        Deep_mass_min = ufloat('Deep_mass_min'),
        Deep_mass_max = ufloat('Deep_mass_max'),
    
    )
)

CountDsCand = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src = cms.InputTag('DsPhiMuMuPiForTau3Mu', 'SelectedDs'),
)    

########################### Sequencies  ############################

#DsPhiMuMuPiSequence = cms.Sequence(
#    (DsPhiMuMuPiForTau3Mu * CountDsCand)
#)
DsPhiMuMuPiSequence = cms.Sequence(DsPhiMuMuPiForTau3Mu)
DsPhiMuMuPiTableSequence = cms.Sequence( DsPhiMuMuPiTable )

DsPlusMetSequence = cms.Sequence( METforDsPhiPi )
DsPlusMetTableSequence = cms.Sequence( DsPlusMetTable )
