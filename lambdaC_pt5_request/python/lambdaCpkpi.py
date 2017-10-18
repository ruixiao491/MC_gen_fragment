import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(5020.0),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
            operates_on_particles = cms.vint32(),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
#            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Dstar_D0_K3pi.dec'),
#            user_decay_file = cms.vstring('Run2Ana/lambdapkpi/data/lambdaC_pkpi.dec'),
            list_forced_decays = cms.vstring('MylambdaC+','Myanti-lambdaC-'),
			user_decay_embedded = cms.vstring(
"""
Alias         MylambdaC+         Lambda_c+
Alias         Myanti-lambdaC-    anti-Lambda_c-
ChargeConj    Myanti-lambdaC-    MylambdaC+
Decay MylambdaC+
1.000        p+  K-   pi+    PHSP;
Enddecay
CDecay Myanti-lambdaC-
End
"""
              )


        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(     
            'HardQCD:all = on',
            'PhaseSpace:pTHatMin = 0.', #min pthat
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
            'processParameters',
        )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

lambdaCDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(4122),
    MomMinPt = cms.untracked.double(5.),
    MomMaxPt = cms.untracked.double(500.),
    MomMinEta = cms.untracked.double(-2.4),
    MomMaxEta = cms.untracked.double(2.4),
    DaughterIDs = cms.untracked.vint32(-321, 211, 2212),
    NumberDaughters = cms.untracked.int32(3),
    NumberDescendants = cms.untracked.int32(0),
)

lambdaCrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(4122),
                                 MinPt = cms.untracked.double(5.),
								 MaxPt = cms.untracked.double(500.),
								 MinRapidity = cms.untracked.double(-1.2),
								 MaxRapidity = cms.untracked.double(1.2),
								 )
ProductionFilterSequence = cms.Sequence(generator*lambdaCDaufilter*lambdaCrapidityfilter)
