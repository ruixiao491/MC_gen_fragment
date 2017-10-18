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
           # user_decay_file = cms.vstring('Run2Ana/lambdapkpi/data/lambdaC_deltaplusplus.dec'),
            list_forced_decays = cms.vstring('MylambdaC+','Myanti-lambdaC-'),
			user_decay_embedded= cms.vstring(
"""
Alias         MylambdaC+         Lambda_c+
Alias         Myanti-lambdaC-    anti-Lambda_c-
 ChargeConj    Myanti-lambdaC-    MylambdaC+
 Alias         MyDelta++          Delta++
Alias         Myanti-Delta--     anti-Delta--
ChargeConj    Myanti-Delta--     MyDelta++
 Decay MylambdaC+
  1.000         MyDelta++             K-       PYTHIA;
  Enddecay
  CDecay Myanti-lambdaC-
  Decay MyDelta++
  1.000         p+                    pi+      PHSP;
  Enddecay
  CDecay Myanti-Delta--
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
    DaughterIDs = cms.untracked.vint32(2224, -321),
    NumberDaughters = cms.untracked.int32(2),
    DaughterID = cms.untracked.int32(2224),
    DescendantsIDs = cms.untracked.vint32(2212,211),
    NumberDescendants = cms.untracked.int32(2),
)

lambdaCrapidityfilter = cms.EDFilter("PythiaFilter",
       ParticleID = cms.untracked.int32(4122),
                                  MinPt = cms.untracked.double(5.),
								  MaxPt = cms.untracked.double(500.),
								  MinRapidity = cms.untracked.double(-1.2),
								  MaxRapidity = cms.untracked.double(1.2),
								  )
ProductionFilterSequence = cms.Sequence(generator*lambdaCDaufilter*lambdaCrapidityfilter)
