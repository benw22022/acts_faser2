#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import acts
import acts.examples

u = acts.UnitConstants


def runTruthTrackingFaser2(
    trackingGeometry: acts.TrackingGeometry,
    field: acts.MagneticFieldProvider,
    digiConfigFile: Path,
    outputDir: Path,
    inputParticlePath: Optional[Path] = None,
    inputHitsPath: Optional[Path] = None,
    decorators=[],
    directNavigation=False,
    reverseFilteringMomThreshold=0 * u.GeV,
    s: acts.examples.Sequencer = None,
):
    from acts.examples.simulation import (
        addParticleGun,
        ParticleConfig,
        EtaConfig,
        PhiConfig,
        MomentumConfig,
        ParticleSelectorConfig,
        addFatras,
        addDigitization,
    )
    from acts.examples.reconstruction import (
        addSeeding,
        SeedingAlgorithm,
        addKalmanTracks,
    )

    s = s or acts.examples.Sequencer(
        events=5000, numThreads=-1, logLevel=acts.logging.INFO
    )

    for d in decorators:
        s.addContextDecorator(d)

    rnd = acts.examples.RandomNumbers(seed=42)
    outputDir = Path(outputDir)

    logger = acts.logging.getLogger("Truth tracking example")

    if inputParticlePath is None:
        addParticleGun(
            s,
            ParticleConfig(num=2, pdg=acts.PdgParticle.eMuon, randomizeCharge=True),
            EtaConfig(-0.01, 0.01, uniform=True),
            MomentumConfig(1.0 * u.GeV, 3000.0 * u.GeV),
            PhiConfig(-0.5* u.degree, 0.5 * u.degree),
            vtxGen=acts.examples.GaussianVertexGenerator(
                stddev=acts.Vector4(
                    1300 * u.mm, 500 * u.mm, 200 * u.mm, 0 * u.ns
                ),
                mean=acts.Vector4(3750, 0, 0, 0),
            ),
            multiplicity=1,
            rnd=rnd,
            outputDirRoot=outputDir,
            #printParticles=True,
        )
    else:
        print("Particle input %s", inputParticlePath.resolve())
        logger.info("Reading particles from %s", inputParticlePath.resolve())
        assert inputParticlePath.exists()
        s.addReader(
            acts.examples.RootParticleReader(
                level=acts.logging.VERBOSE,
                filePath=str(inputParticlePath.resolve()),
                outputParticles="particles_input",
            )
        )
        s.addWhiteboardAlias("particles", "particles_input")

    if inputHitsPath is None:
        addFatras(
            s,
            trackingGeometry,
            field,
            rnd=rnd,
            enableInteractions=True,
            postSelectParticles=ParticleSelectorConfig(
                pt=(0.9 * u.GeV, None),
                measurements=(3, None),
                removeNeutral=True,
                removeSecondaries=True,
            ),
        )
    else:
        logger.info("Reading hits from %s", inputHitsPath.resolve())
        assert inputHitsPath.exists()
        s.addReader(
            acts.examples.RootSimHitReader(
                level=acts.logging.INFO,
                filePath=str(inputHitsPath.resolve()),
                outputSimHits="simhits",
            )
        )

    addDigitization(
        s,
        trackingGeometry,
        field,
        digiConfigFile=digiConfigFile,
        rnd=rnd,
    )

    addSeeding(
        s,
        trackingGeometry,
        field,
        rnd=rnd,
        inputParticles="particles_input",
        seedingAlgorithm=SeedingAlgorithm.TruthSmeared,
        particleHypothesis=acts.ParticleHypothesis.muon,
    )

    addKalmanTracks(
        s,
        trackingGeometry,
        field,
        directNavigation,
        reverseFilteringMomThreshold,
    )

    s.addAlgorithm(
        acts.examples.TrackSelectorAlgorithm(
            level=acts.logging.INFO,
            inputTracks="tracks",
            outputTracks="selected-tracks",
            selectorConfig=acts.TrackSelector.Config(
                minMeasurements=3,
            ),
        )
    )
    s.addWhiteboardAlias("tracks", "selected-tracks")

    s.addWriter(
        acts.examples.RootTrackStatesWriter(
            level=acts.logging.INFO,
            inputTracks="tracks",
            inputParticles="particles_selected",
            inputTrackParticleMatching="track_particle_matching",
            inputSimHits="simhits",
            inputMeasurementSimHitsMap="measurement_simhits_map",
            filePath=str(outputDir / "trackstates_kf.root"),
        )
    )

    s.addWriter(
        acts.examples.RootTrackSummaryWriter(
            level=acts.logging.INFO,
            inputTracks="tracks",
            inputParticles="particles_selected",
            inputTrackParticleMatching="track_particle_matching",
            filePath=str(outputDir / "tracksummary_kf.root"),
        )
    )

    s.addWriter(
        acts.examples.TrackFitterPerformanceWriter(
            level=acts.logging.INFO,
            inputTracks="tracks",
            inputParticles="particles_selected",
            inputTrackParticleMatching="track_particle_matching",
            filePath=str(outputDir / "performance_kf.root"),
        )
    )

    return s


if "__main__" == __name__:
    srcdir = Path(__file__).resolve().parent.parent.parent.parent

    ## Definition of the tracker geometry and position 
    pos = [10000, 10500, 11000, 19500, 20000, 20500]
    n_layers = len(pos)
    
    # One can specify for each layer the bounds in X and Y, the type of surface (0 for plane, 1 for cylinder)
    boundsX = [500] * n_layers # mm for the half length in X
    boundsY = [1500] * n_layers # mm for the half length in Y
    type_surface = [0] * n_layers
    stereo_layers = [0] * n_layers
    bounds_dimensions = [max(boundsX) * 1.1, max(boundsY) * 1.1]
    thickness = 4  #mm 
    # Bin value if 0 detector along x-axis, if 1 detector along y-axis, if 2 detector along z-axis
    X_axis = 0
    Z_axis = 2
    
    detector, trackingGeometry, decorators = acts.examples.Faser2TelescopeDetector.create(
        bounds=bounds_dimensions, positions=pos, binValue=X_axis, thickness=thickness, stereos=stereo_layers,
        boundsX=boundsX, boundsY=boundsY, Type_surf=type_surface
    )
    
    inputParticlePath = Path("/eos/user/o/osalin/FASER2/FASER2_ACTS_tool/HEPMC_ROOT/Root_LLP/Root_DarkHiggs_X_good/Particles_DarkHiggs_m0.8128_mu_mu.root")
    if not inputParticlePath.exists():
        print("File does not exist")
        inputParticlePath = None

    outputDir = Path(f"./Output_tracking/")
    outputDir.mkdir(parents=True, exist_ok=True)

    ## Constant Magnetic Field Option
    # field = acts.ConstantBField(acts.Vector3(0, 0, 0.2 * u.T))
    
    ## Restricted Magnetic Field Option with the dimension of Samurai magnet
    field = acts.RestrictedBField(acts.Vector3(0, 0 * u.T, 1.0 * u.T))
    
    ## Restricted Magnetic Field Option with the dimension of Industrial magnet for 3 Modules 
    # field = acts.RestrictedBField_Indu(acts.Vector3(0, 0 * u.T, 0.4 * u.T))

    runTruthTrackingFaser2(
        trackingGeometry,
        field,
        digiConfigFile=srcdir / "Examples/Algorithms/Digitization/share/default-smearing-config-telescope.json",
        outputDir=outputDir,
        inputParticlePath=inputParticlePath,
    ).run()
