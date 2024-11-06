// 
// mini AOD pileup profile producer
// 
//#include "FWCore/Framework/interface/global/EDAnalyzer.h"
//#include "FWCore/Framework/interface/Event.h"
//#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
//#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
//#include "FWCore/Utilities/interface/InputTag.h"
//
//#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
//
//// ----------member data ---------------------------
//
//
//// class declaration
//class PUanalyzer : public edm::global::EDAnalyzer<> {
//
//public:
//    typedef edm::EDGetTokenT<std::vector<PileupSummaryInfo>> PileupToken;
//
//
//PUanalyzer::PUanalyzer(const edm::ParameterSet& iConfig)
//{
//  edm::InputTag PileupTag("slimmedAddPileupInfo"); // "addPileupInfo" for AOD files
//  PileupToken = consumes<std::vector<PileupSummaryInfo>>(PileupTag);
//}
//
//};
//
//void PUanalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
//{
//
//  int NumTrueInts = -1;
//  int NumPUInts = -1;
//
//  edm::Handle<std::vector<PileupSummaryInfo>> PileupInfo;
//  event.getByToken(PileupToken, PileupInfo);
//
//  for(std::vector<PileupSummaryInfo>::const_iterator iPU = PileupInfo->begin(); iPU != PileupInfo->end(); iPU++){
//    int BX = iPU->getBunchCrossing();
//    if(BX == 0){ // "0" is the in-time crossing. Negative are early crossings. Positive are late.
//      NumTrueInts = PVI->getTrueNumInteractions();
//      NumPUInts = PVI->getPU_NumInteractions();
//      printf("NumTrueInts = %d, NumPUInts = %d\n", NumTrueInts, NumPUInts);
//    }
//  }
//}

