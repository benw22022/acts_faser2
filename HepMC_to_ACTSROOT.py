""""
HepMC --> ROOT File converter
-------------------------------------------------
Copy of Olivier's script to convert HepMC to a 
ROOT file which can be parsed by ACTS
Original File: https://github.com/OlivierSalin/Faser2_acts/blob/main/Root_input_LLP/HepMC_Root_X_Events.py
"""

import ROOT
import pyhepmc.io
import numpy as np
import argparse
import glob
import os


def convert_hepmc_to_root(input_file: str, output_file: str) -> None:
    
    # Create a ROOT file and tree
    output = ROOT.TFile(output_file, "RECREATE")
    tree = ROOT.TTree("particles", "Particle information")

    # Create vectors for each branch
    event_id = np.zeros(1, dtype=np.int32)
    particle_id = ROOT.vector('unsigned long')()
    particle_type = ROOT.vector('int')()
    process = ROOT.vector('unsigned int')()
    vx = ROOT.vector('double')()
    vy = ROOT.vector('double')()
    vz = ROOT.vector('double')()
    vt = ROOT.vector('double')()
    px = ROOT.vector('double')()
    py = ROOT.vector('double')()
    pz = ROOT.vector('double')()
    m = ROOT.vector('double')()
    q = ROOT.vector('double')()
    eta = ROOT.vector('double')()
    phi = ROOT.vector('double')()
    theta = ROOT.vector('double')()
    pt = ROOT.vector('double')()
    p = ROOT.vector('double')()
    vertex_primary = ROOT.vector('unsigned int')()
    vertex_secondary = ROOT.vector('unsigned int')()
    particle = ROOT.vector('unsigned int')()
    generation = ROOT.vector('unsigned int')()
    sub_particle = ROOT.vector('unsigned int')()

    # Add the branches to the tree
    tree.Branch("event_id", event_id,"event_id/i")
    tree.Branch("particle_id", particle_id)
    tree.Branch("particle_type", particle_type)
    tree.Branch("process", process)
    tree.Branch("vx", vx)
    tree.Branch("vy", vy)
    tree.Branch("vz", vz)
    tree.Branch("vt", vt)
    tree.Branch("px", px)
    tree.Branch("py", py)
    tree.Branch("pz", pz)
    tree.Branch("m", m)
    tree.Branch("q", q)
    tree.Branch("eta", eta)
    tree.Branch("phi", phi)
    tree.Branch("theta", theta)
    tree.Branch("pt", pt)
    tree.Branch("p", p)
    tree.Branch("vertex_primary", vertex_primary)
    tree.Branch("vertex_secondary", vertex_secondary)
    tree.Branch("particle", particle)
    tree.Branch("generation", generation)
    tree.Branch("sub_particle", sub_particle)        

    # Loop over the events in the file
    ascii_reader = pyhepmc.io.ReaderAsciiHepMC2(input_file)
    for i, event in enumerate(ascii_reader):
        # Loop over the particles in each event
        for j, particle_ in enumerate(event.particles):
            if particle_.pid in [11, -11, 13, -13, 211, -211]:
                #* Calculate the particle's eta, phi, pt,p
                #! IMPORTANT1 : There was a rotation in the Axis from XYZ into Z'Y'X'(new beamline along X' and Magnetic field along Z') to make ACTS work Z-> X' and X->-Z'
                #! IMPORTANT2 Different definition ACTS and FORESEE Y->X->Z'
                px_, py_, pz_ = particle_.momentum.pz, -particle_.momentum.px, particle_.momentum.py    #! pz-> px' px->-pz'  
                pt_ = (px_**2 + py_**2)**0.5
                p_ = (px_**2 + py_**2 + pz_**2)**0.5
                eta_ = -ROOT.TMath.Log(ROOT.TMath.Tan(0.5*ROOT.TMath.ACos(pz_/p_)))
                phi_ = ROOT.TMath.ATan2(py_, px_)
                theta_=ROOT.TMath.ACos(pz_/p_)

                event_id[0]=i
                particle_id.push_back(4503599644147712 if particle_.pid > 0 else 4503599660924928)
                particle_type.push_back(particle_.pid)
                process.push_back(0)
                vx.push_back(particle_.production_vertex.position.z)        #! vertex_x' -> vertex_z *IMPORTANT1
                vy.push_back(-particle_.production_vertex.position.x)       #! vetex_y'>vertex_x'->-vertex_z  IMPORTANT2 and IMPORTANT1
                vz.push_back(particle_.production_vertex.position.y)        #! vertex_z' ->-vertex_x-> vertex_y  *IMPORTANT1 and IMPORTANT2  
                vt.push_back(particle_.production_vertex.position.t)
                px.push_back(particle_.momentum.pz)                         #! pz'->px
                py.push_back(-particle_.momentum.px)                        #! py'->px'->-pz
                pz.push_back(particle_.momentum.py)                         #! pz'->-px->py
                m.push_back(particle_.generated_mass)
                q.push_back(-1 if particle_.pid < 0 else 1)
                eta.push_back(eta_)
                phi.push_back(phi_)
                theta.push_back(theta_)
                pt.push_back(pt_)
                p.push_back(p_)
                vertex_primary.push_back(1)
                vertex_secondary.push_back(0)
                particle.push_back(2 if particle_.pid < 0 else 1)
                generation.push_back(0)
                sub_particle.push_back(0)


        tree.Fill()
        particle_id.clear()
        particle_type.clear()
        process.clear()
        vx.clear()
        vy.clear()
        vz.clear()
        vt.clear()
        px.clear()
        py.clear()
        pz.clear()
        m.clear()
        q.clear()
        eta.clear()
        phi.clear()
        theta.clear()
        pt.clear()
        p.clear()
        vertex_primary.clear()
        vertex_secondary.clear()
        particle.clear()
        generation.clear()
        sub_particle.clear()


    # Write the ROOT tree to the output file and close it
    output.Write()
    output.Close()


def main(args: argparse.Namespace) -> int:
    
    input_files = glob.glob(os.path.join(args.input, "*.hepmc"))
    
    if len(input_files) == 0:
        print(f"Error: no hepmc files found on path {args.input}")
        return 1
    
    print(f"Found {len(input_files)} hepmc files")
    
    os.makedirs(args.output, exist_ok=True)

    for i, input_file in enumerate(input_files):
        
        output_file = os.path.basename(input_file).replace(".hepmc", ".root")
        output_file = os.path.join(args.output, output_file)
        convert_hepmc_to_root(input_file, output_file)
        print(f"{i+1} / {len(input_files)}: Written {output_file}")

    return 0

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help='input file directory', type=str)
    parser.add_argument("output", help='output file directory', type=str)
    args = parser.parse_args()
    
    main(args)